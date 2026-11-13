import importlib.util
import json
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("closer_coach_test", os.path.join(HERE, "coach.py"))
coach = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coach)
EXAMPLE = os.path.join(HERE, "..", "pipeline", "pipeline.example.json")
CALL = os.path.join(HERE, "call.example.txt")


def offer():
    with open(EXAMPLE, encoding="utf-8") as fh:
        return json.load(fh)["me"]


class Detect(unittest.TestCase):
    def setUp(self):
        self.lib = coach.load_objections()

    def test_each_objection(self):
        cases = {"It looks great, but honestly, it's too expensive for us right now.": "price",
                 "That's out of our budget.": "price",
                 "It's our busy season, maybe next quarter.": "timing",
                 "Let me think about it.": "think",
                 "I need to run it by my business partner.": "authority",
                 "We already have someone who does our site.": "incumbent",
                 "How do I know this actually works?": "proof",
                 "Can you just send me some info?": "send_info"}
        for text, key in cases.items():
            self.assertEqual(coach.detect(text, self.lib), key, text)
        for text in ("Mostly word of mouth, and people calling the front desk.", "Sounds like a plan."):
            self.assertIsNone(coach.detect(text, self.lib), text)

    def test_each_objection_in_portuguese(self):
        cases = {"Ficou lindo, mas sinceramente, tá caro pra gente agora.": "price",
                 "Isso tá fora do nosso orçamento.": "price",
                 "Agora é alta temporada, quem sabe depois do carnaval.": "timing",
                 "Vou pensar e te dou um retorno.": "think",
                 "Preciso conversar com meu sócio.": "authority",
                 "Meu sobrinho já cuida do Instagram.": "incumbent",
                 "Como eu sei que isso funciona mesmo?": "proof",
                 "Me manda as informações no WhatsApp?": "send_info"}
        for text, key in cases.items():
            self.assertEqual(coach.detect(text, self.lib), key, text)
        for text in ("Mais por indicação, e gente chamando no WhatsApp da recepção.", "Parece um bom plano."):
            self.assertIsNone(coach.detect(text, self.lib), text)

    def test_the_reel_answer(self):
        card = coach.coach_line("Daniela", "Ficou lindo, mas sinceramente, tá caro pra gente agora.",
                                "Você", self.lib, offer())
        self.assertEqual(card["label"], "Objeção: preço")
        self.assertEqual(card["say"], "Faz sentido. A maioria das clínicas recupera o investimento com 2 pacientes novos "
                                      "por mês. Quer começar pelo plano mensal de R$ 399, sem taxa de implantação?")

    def test_never_invents_a_missing_offer(self):
        card = coach.coach_line("Daniela", "too expensive", "You", self.lib, {})
        self.assertIn("[seu value line]", card["say"])
        self.assertIn("[seu plan b]", card["say"])

    def test_own_lines_and_small_talk_get_no_card(self):
        self.assertIsNone(coach.coach_line("You", "Is it too expensive?", "You", self.lib, offer()))
        self.assertIsNone(coach.coach_line("Daniela", "Mostly word of mouth.", "You", self.lib, offer()))


class Call(unittest.TestCase):
    def test_listen_to_the_example_call(self):
        with open(CALL, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        cards = coach.listen(lines, "Você", coach.load_objections(), offer())
        self.assertEqual([c["kind"] for c in cards], ["objection", "buying"])
        self.assertIn("Quando a gente pode começar?", cards[1]["heard"])

    def test_caption_lines_with_timestamps(self):
        self.assertEqual(coach.parse_line("[2:14] Daniela: It's too expensive."), ("Daniela", "It's too expensive."))
        self.assertEqual(coach.parse_line("Daniela Rocha: Hello"), ("Daniela Rocha", "Hello"))

    def test_review(self):
        with open(CALL, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        r = coach.review(lines, "Você", coach.load_objections())
        self.assertEqual(r["questions_asked"], 2)
        self.assertEqual([k for k, _ in r["objections"]], ["price"])
        self.assertTrue(r["next_step_agreed"])
        self.assertGreater(r["talk_share"], 50)


if __name__ == "__main__":
    unittest.main()
