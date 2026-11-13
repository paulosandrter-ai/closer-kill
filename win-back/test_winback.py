import datetime
import importlib.util
import json
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("closer_winback_test", os.path.join(HERE, "winback.py"))
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)
EXAMPLE = os.path.join(HERE, "..", "pipeline", "pipeline.example.json")
D = datetime.date


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        return json.load(fh)


class Assess(unittest.TestCase):
    def test_the_example_board(self):
        rows = {r["deal_id"]: r["state"] for r in W.candidates(example(), D(2026, 10, 29))}
        self.assertEqual(rows["serra-azul-site"], "ready")
        self.assertEqual(rows["mesa-verde-anuncios"], "never")
        self.assertEqual(rows["trigo-mel-pedidos"], "skip")
        self.assertEqual(rows["sorriso-leve-site"], "skip")

    def test_sixty_days_and_the_revisit_date(self):
        data = example()
        deal = W.P.find(data["deals"], "serra-azul-site")
        self.assertEqual(W.assess(data, deal, D(2026, 10, 8))[0], "later")   # 59 days after Aug 10
        self.assertEqual(W.assess(data, deal, D(2026, 10, 9))[0], "ready")
        deal["revisit"] = "2026-11-15"
        self.assertEqual(W.assess(data, deal, D(2026, 10, 29))[0], "later")
        self.assertEqual(W.assess(data, deal, D(2026, 11, 15))[0], "ready")

    def test_competitor_waits_longer(self):
        data = example()
        deal = W.P.find(data["deals"], "serra-azul-site")
        deal["lost_reason"] = "went with another agency"
        self.assertEqual(W.assess(data, deal, D(2026, 10, 29))[0], "later")
        self.assertEqual(W.assess(data, deal, D(2027, 2, 6))[0], "ready")

    def test_one_win_back_only(self):
        data = example()
        ok, msg = W.record(data, "serra-azul-site", "Hi Tomás, checking back in.", "yes", "2026-10-29T10:00")
        self.assertTrue(ok, msg)
        deal = W.P.find(data["deals"], "serra-azul-site")
        self.assertEqual(deal["stage"], "contacted")
        self.assertEqual(W.P.validate(data)[0], [])
        state, why, _ = W.assess(data, deal, D(2027, 6, 1))
        self.assertEqual(state, "never")
        self.assertIn("one is the limit", why)

    def test_record_needs_a_yes(self):
        self.assertFalse(W.record(example(), "serra-azul-site", "Hi", "ok", "2026-10-29T10:00")[0])
        self.assertFalse(W.record(example(), "mesa-verde-anuncios", "Hi", "yes", "2026-10-29T10:00")[0])


class Draft(unittest.TestCase):
    def test_the_timing_draft_keeps_the_easy_out(self):
        d = W.draft(example(), "serra-azul-site", D(2026, 10, 29))
        self.assertEqual(d["kind"], "timing")
        self.assertEqual(d["subject"], "Voltando a falar, Tomás")
        self.assertIn("pediu pra eu voltar em novembro", d["body"])
        self.assertIn("eu deixo quieto", d["body"])

    def test_budget_uses_plan_b(self):
        data = example()
        W.P.find(data["deals"], "serra-azul-site")["lost_reason"] = "budget"
        d = W.draft(data, "serra-azul-site", D(2026, 10, 29))
        self.assertIn("plano mensal de R$ 399", d["body"])

    def test_no_draft_for_never(self):
        with self.assertRaises(W.WinbackError):
            W.draft(example(), "mesa-verde-anuncios", D(2027, 1, 1))


if __name__ == "__main__":
    unittest.main()
