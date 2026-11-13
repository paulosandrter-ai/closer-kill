import datetime
import importlib.util
import json
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("closer_slots_test", os.path.join(HERE, "slots.py"))
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
EXAMPLE = os.path.join(HERE, "..", "pipeline", "pipeline.example.json")
DT = datetime.datetime
TUE = datetime.date(2026, 10, 27)


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        return json.load(fh)


class Parse(unittest.TestCase):
    def test_the_reel_reply(self):
        self.assertEqual(S.parse_when("Sorry, crazy week! Thursday at 2 works.", TUE), DT(2026, 10, 29, 14, 0))

    def test_other_ways_people_say_it(self):
        cases = {"tomorrow at 10am": DT(2026, 10, 28, 10, 0),
                 "Oct 30 at 2:30pm": DT(2026, 10, 30, 14, 30),
                 "How about noon Friday?": DT(2026, 10, 30, 12, 0),
                 "Monday at 9 works": DT(2026, 11, 2, 9, 0),
                 "next Monday at 9": DT(2026, 11, 2, 9, 0),
                 "Tuesday 3pm?": DT(2026, 11, 3, 15, 0),
                 "jan 5 at 11": DT(2027, 1, 5, 11, 0)}
        for text, want in cases.items():
            self.assertEqual(S.parse_when(text, TUE), want, text)

    def test_portuguese(self):
        cases = {"Desculpa, semana corrida! Quinta às 14h pode ser.": DT(2026, 10, 29, 14, 0),
                 "amanhã 10h30": DT(2026, 10, 28, 10, 30),
                 "30/10 às 15:00": DT(2026, 10, 30, 15, 0),
                 "sexta ao meio-dia": DT(2026, 10, 30, 12, 0),
                 "segunda que vem às 9": DT(2026, 11, 2, 9, 0),
                 "terça às 3 da tarde": DT(2026, 11, 3, 15, 0),
                 "5 de janeiro às 11h": DT(2027, 1, 5, 11, 0)}
        for text, want in cases.items():
            self.assertEqual(S.parse_when(text, TUE), want, text)
        for text in ("Vamos falar em breve", "Terça pode ser", "Fechado!", "Tenho 2 filhos"):
            self.assertIsNone(S.parse_when(text, TUE), text)

    def test_no_clear_time_is_none(self):
        for text in ("Let's talk soon", "Tuesday works", "Sounds good!", "I have 2 kids"):
            self.assertIsNone(S.parse_when(text, TUE), text)


class Slots(unittest.TestCase):
    def test_free_slots_skip_busy_and_weekends(self):
        busy = [(DT(2026, 10, 29, 9, 0), DT(2026, 10, 29, 12, 0))]
        slots = S.free_slots(busy, datetime.date(2026, 10, 29), days=1, minutes=30, limit=3)
        self.assertEqual(slots[0], DT(2026, 10, 29, 12, 0))
        sat = S.free_slots([], datetime.date(2026, 10, 31), days=2, limit=3)
        self.assertEqual(sat, [])

    def test_ics_has_both_people(self):
        data = example()
        c = S.P.find(data["contacts"], "dani-sorriso-leve")
        text = S.ics(data["me"], c, DT(2026, 10, 29, 14, 0), 30, S.title_for(data, c))
        self.assertIn("DTSTART;TZID=America/Fortaleza:20261029T140000", text)
        self.assertIn("DTEND;TZID=America/Fortaleza:20261029T143000", text)
        self.assertIn("SUMMARY:Clínica Sorriso Leve x Sua Agência", text)
        self.assertIn("mailto:daniela@sorrisoleve.com.br", text)


class Book(unittest.TestCase):
    def test_book_needs_a_yes_and_a_free_slot(self):
        data = example()
        start = DT(2026, 11, 4, 11, 0)
        self.assertFalse(S.book(data, "priscila-bemtevi", start, 30, "ok")[0])
        busy = [(DT(2026, 11, 4, 10, 30), DT(2026, 11, 4, 11, 15))]
        self.assertFalse(S.book(data, "priscila-bemtevi", start, 30, "yes", busy)[0])
        ok, msg = S.book(data, "priscila-bemtevi", start, 30, "yes", [])
        self.assertTrue(ok, msg)
        self.assertEqual(S.P.find(data["deals"], "bemtevi-anuncios")["stage"], "call-booked")
        self.assertEqual(data["activities"][-1]["when"], "2026-11-04T11:00")
        self.assertEqual(S.P.validate(data)[0], [])

    def test_never_books_do_not_contact(self):
        self.assertFalse(S.book(example(), "elena-mesa-verde", DT(2026, 11, 4, 11, 0), 30, "yes")[0])


if __name__ == "__main__":
    unittest.main()
