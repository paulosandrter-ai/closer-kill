#!/usr/bin/env python3
"""Brings back the deals that went quiet. Standard library only.

  list     deals worth one more try today, and the ones it will never touch, with why
  draft    the win-back email for one deal, from why it was lost
  record   logs it AFTER it went out, with your yes word for word, and reopens the deal

    python3 winback.py list --today 2026-10-29
    python3 winback.py draft --deal serra-azul-site --today 2026-10-29
    python3 winback.py record --deal serra-azul-site --text-file /tmp/w.txt --approval "sim" --at 2026-10-29T10:00

Who it will try:
  - a lost deal whose reason was timing, budget, "thinking about it" or no decision,
    at least 60 days after it was lost, or on the deal's own "revisit" date when one was set
  - an open deal with no activity for 30 days or more after /follow-up's limit ran out
Who it never touches: anyone who said no, unsubscribed or is do not contact, a deal lost to
"went with someone else" before 180 days, and anyone who already got a win-back in the last 90 days.
One win-back email per deal per 90 days, and a second one never follows the first.
"""

import argparse
import datetime
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOST_WAIT = 60
COMPETITOR_WAIT = 180
QUIET_DAYS = 30
COOLDOWN = 90

# lost reasons are matched without accents (P.plain), in Portuguese or English
REASONS = [
    ("timing", re.compile(r"timing|busy|season|later|next (year|quarter|month)|not (the )?right time|fall|spring|summer|winter"
                          r"|momento|temporada|corrid|sem tempo|depois|mais pra frente|(mes|ano|semestre) que vem"
                          r"|proximo (mes|ano|semestre)|carnaval|natal|fim de ano|janeiro|fevereiro|marco|abril|maio"
                          r"|junho|julho|agosto|setembro|outubro|novembro|dezembro", re.I)),
    ("budget", re.compile(r"budget|price|expensive|afford|cost|orcamento|preco|caro|verba|valor|grana|dinheiro", re.I)),
    ("competitor", re.compile(r"went with|another (agency|vendor|company)|someone else|competitor|in-house|nephew"
                              r"|fechou com|fecharam com|outra (agencia|empresa)|concorrente|sobrinho|faz (aqui )?dentro", re.I)),
    ("undecided", re.compile(r"think|undecided|no decision|went quiet|ghost|no reply|stalled"
                             r"|pensar|indecis|sumiu|sem resposta|nao respondeu|parou", re.I)),
]
NEVER = re.compile(r"unsubscribe|said no|not interested|do not contact|remove|descadastr|disse nao|sem interesse"
                   r"|nao tem interesse|nao contatar|me tira", re.I)

TEMPLATES = {
    "timing": ("Voltando a falar, {first}",
               "Oi {first}, quando a gente conversou você disse que não era o momento{when}. Agora ficou melhor pra "
               "{topic}? Se não, sem problema nenhum, é só me falar que eu deixo quieto.\n\n{me}"),
    "budget": ("Um jeito menor de começar, {first}",
               "Oi {first}, da última vez o valor foi o que pegou. Agora a gente tem {plan_b}, se isso ajudar. "
               "Posso te explicar rapidinho, ou deixar por aqui mesmo.\n\n{me}"),
    "competitor": ("Como estão as coisas, {first}?",
                   "Oi {first}, espero que o projeto com a outra equipe tenha dado certo. Se ainda tiver algo na sua "
                   "lista, estou por aqui. Se não, não precisa responder.\n\n{me}"),
    "undecided": ("Ainda está nos seus planos, {first}?",
                  "Oi {first}, a gente conversou sobre {topic} um tempo atrás e eu não soube como ficou. "
                  "Ainda é algo que você quer resolver? Um sim ou não já me ajuda.\n\n{me}"),
}
MESES = ("janeiro|fevereiro|março|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro"
         "|carnaval|natal|fim de ano")


def _pipeline():
    path = os.path.join(HERE, "..", "pipeline", "deals.py")
    if not os.path.exists(path):
        sys.exit("The win-back skill needs the pipeline skill next to it (../pipeline/deals.py).")
    spec = importlib.util.spec_from_file_location("closer_deals", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = _pipeline()
D = datetime.date


class WinbackError(Exception):
    pass


def reason_kind(text):
    for key, rx in REASONS:
        if rx.search(P.plain(text)):
            return key
    return "undecided"


def lost_on(data, deal):
    for a in reversed(P.history(data, deal_id=deal["id"])):
        if a["type"] == "stage" and "-> lost" in (a.get("text") or ""):
            return D.fromisoformat(a["date"][:10])
    return D.fromisoformat(P.last_touch(data, deal))


def assess(data, deal, today):
    """(state, why, kind). state: ready, later, never, skip."""
    c = P.find(data["contacts"], deal["contact_id"]) or {}
    acts = P.history(data, contact_id=deal["contact_id"])
    if c.get("do_not_contact") or P.suppressed(data, c.get("email")):
        return "never", "do not contact", None
    if any(a.get("direction") == "in" and P.NO_RE.search(a.get("text") or "") for a in acts):
        return "never", "they said no", None
    if deal["stage"] == "won":
        return "skip", "customer", None
    winbacks = [a for a in P.history(data, deal_id=deal["id"]) if a["type"] == "winback"]
    if winbacks:
        last = D.fromisoformat(winbacks[-1]["date"][:10])
        replied = any(a.get("direction") == "in" and a["date"] > winbacks[-1]["date"] for a in acts)
        if not replied:
            return "never", "a win-back already went on %s with no reply: one is the limit" % last, None
        if (today - last).days < COOLDOWN:
            return "later", "win-back on %s; wait until %s" % (last, last + datetime.timedelta(days=COOLDOWN)), None
    if deal["stage"] == "lost":
        reason = deal.get("lost_reason") or ""
        if NEVER.search(P.plain(reason)):
            return "never", "lost: %s" % reason, None
        kind = reason_kind(reason)
        since = lost_on(data, deal)
        if deal.get("revisit"):
            rv = D.fromisoformat(deal["revisit"])
            if today < rv:
                return "later", "they asked to revisit on %s" % rv, kind
            return "ready", "revisit date %s has come (%s)" % (rv, reason), kind
        wait = COMPETITOR_WAIT if kind == "competitor" else LOST_WAIT
        if (today - since).days < wait:
            return "later", "lost %s (%s); try from %s" % (since, reason, since + datetime.timedelta(days=wait)), kind
        return "ready", "lost %d days ago: %s" % ((today - since).days, reason), kind
    quiet = (today - D.fromisoformat(P.last_touch(data, deal))).days
    followups = [a for a in acts if a["type"] == "followup"]
    if quiet >= QUIET_DAYS and len(followups) >= 3:
        return "ready", "quiet %d days after the last follow-up" % quiet, "undecided"
    return "skip", "still active", None


def candidates(data, today):
    order = {"ready": 0, "later": 1, "never": 2, "skip": 3}
    out = []
    for d in data["deals"]:
        state, why, kind = assess(data, d, today)
        out.append({"deal_id": d["id"], "title": d["title"], "state": state, "why": why, "kind": kind,
                    "value": d.get("value", 0)})
    return sorted(out, key=lambda r: (order[r["state"]], -r["value"]))


def draft(data, deal_id, today):
    deal = P.find(data["deals"], deal_id)
    if deal is None:
        raise WinbackError("No deal %s" % deal_id)
    state, why, kind = assess(data, deal, today)
    if state != "ready":
        raise WinbackError("Not today: %s." % why)
    c = P.find(data["contacts"], deal["contact_id"])
    me = data.get("me", {})
    m = re.search(r"\b(%s)\b" % MESES, deal.get("lost_reason") or "", re.I)
    fields = {"first": c["name"].split()[0], "topic": deal["title"].lower(),
              "when": " e pediu pra eu voltar em %s" % m.group(1).lower() if m else "",
              "plan_b": me.get("plan_b") or "[fill: plan_b]", "me": (me.get("name") or "").split(" ")[0]}
    subject, body = TEMPLATES[kind]
    return {"to": c.get("email") or c.get("phone"), "subject": subject.format(**fields), "body": body.format(**fields), "kind": kind}


def record(data, deal_id, text, approval, when):
    ok, why = P.parse_yes(approval)
    if not ok:
        return False, "Not recorded: %s." % why
    deal = P.find(data["deals"], deal_id)
    if deal is None:
        return False, "No deal %s" % deal_id
    state, why, _ = assess(data, deal, D.fromisoformat(when[:10]))
    if state != "ready":
        return False, "Not recorded: %s." % why
    if "[fill:" in text:
        return False, "Not recorded: the message still has a [fill: ...] in it."
    P.add_activity(data, date=when, contact_id=deal["contact_id"], deal_id=deal_id, channel="email", type="winback",
                   direction="out", subject=None, text=text, approval=approval)
    if deal["stage"] == "lost":
        deal["stage"] = "contacted"
        deal["lost_reason"] = None
    deal["next_step"] = "Esperar resposta da reconquista (sem follow-up)"
    return True, "Logged the win-back. The deal is open again; if they don't reply, that's the end of it."


def main(argv=None):
    p = argparse.ArgumentParser(description="Win back deals that went quiet.")
    p.add_argument("--file", default=P.DEFAULT_FILE)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list")
    s.add_argument("--today")
    s = sub.add_parser("draft")
    s.add_argument("--deal", required=True)
    s.add_argument("--today")
    s = sub.add_parser("record")
    s.add_argument("--deal", required=True)
    s.add_argument("--text")
    s.add_argument("--text-file")
    s.add_argument("--approval", required=True)
    s.add_argument("--at", required=True)
    a = p.parse_args(argv)
    try:
        data = P.load(a.file)
        if a.cmd == "list":
            for r in candidates(data, P.today_arg(a.today)):
                if r["state"] != "skip":
                    print("%-6s %-30s %s" % (r["state"].upper(), r["title"][:30], r["why"]))
        elif a.cmd == "draft":
            d = draft(data, a.deal, P.today_arg(a.today))
            print("To: %s\nSubject: %s\n\n%s" % (d["to"], d["subject"], d["body"]))
        else:
            text = a.text
            if a.text_file:
                with open(a.text_file, encoding="utf-8") as fh:
                    text = fh.read().strip()
            if not text:
                raise WinbackError("Give --text or --text-file: exactly what went out.")
            ok, msg = record(data, a.deal, text, a.approval, a.at)
            if ok:
                P.save(data, a.file)
            print(msg)
            return 0 if ok else 1
    except (WinbackError, P.PipelineError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
