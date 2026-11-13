import importlib.util
import json
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("closer_brief_test", os.path.join(HERE, "brief.py"))
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)
EXAMPLE = os.path.join(HERE, "..", "pipeline", "pipeline.example.json")

HOME = """<html><head><title>Clínica Sorriso Leve | Family Dentist in Austin</title>
<meta name="description" content="Gentle family dentistry on Sorriso Leve since 2009."></head>
<body><h1>Family dentistry in Austin</h1><h2>Cleanings &amp; checkups</h2>
<a href="/about">About us</a><a href="/services">Our services</a><a href="https://other.example/x">Partner</a>
<a href="/blog/1">Blog</a><p>Serving Austin since 2009. Call (512) 555-0142 or email frontdesk@sorrisoleve.com.br</p>
<a href="https://www.instagram.com/harborlanedental">Instagram</a>
<script type="application/ld+json">{"aggregateRating": {"ratingValue": "4.8", "reviewCount": "212"}}</script>
</body></html>"""
ABOUT = "<html><body><h2>Meet Dr. Ortiz</h2><p>Our team</p></body></html>"


class Facts(unittest.TestCase):
    def test_pick_pages_stays_on_site(self):
        picked = B.pick_pages("https://sorrisoleve.com.br", HOME)
        self.assertEqual(picked, ["https://sorrisoleve.com.br/about", "https://sorrisoleve.com.br/services"])

    def test_facts(self):
        f = B.facts({"https://sorrisoleve.com.br": HOME, "https://sorrisoleve.com.br/about": ABOUT})
        self.assertEqual(f["title"], "Clínica Sorriso Leve | Family Dentist in Austin")
        self.assertEqual(f["since"], 2009)
        self.assertEqual(f["rating"]["count"], 212)
        self.assertEqual(f["phones"], ["(512) 555-0142"])
        self.assertEqual(f["emails"], ["frontdesk@sorrisoleve.com.br"])
        self.assertIn("Cleanings & checkups", f["headings"])
        self.assertIn("Meet Dr. Ortiz", f["headings"])
        self.assertIn("agendamento online", f["tools_missing"])
        self.assertIn("botão de WhatsApp", f["tools_missing"])
        self.assertEqual(f["socials"], ["https://www.instagram.com/harborlanedental"])

    def test_brief_cites_sources_and_leaves_slots_for_claude(self):
        with open(EXAMPLE, encoding="utf-8") as fh:
            data = json.load(fh)
        c = B.P.find(data["contacts"], "dani-sorriso-leve")
        f = B.facts({"https://sorrisoleve.com.br": HOME})
        md = B.brief(c, None, f)
        self.assertTrue(md.startswith("# Briefing: Clínica Sorriso Leve"))
        self.assertIn("- No mercado desde 2009", md)
        self.assertIn("## Fontes\n\n- https://sorrisoleve.com.br", md)
        self.assertIn("[Claude:", md)
        self.assertIn("uma pista, não prova", md)


class Portugues(unittest.TestCase):
    def test_a_brazilian_site(self):
        page = ('<html><head><title>Clínica Sorriso Leve | Dentista em Fortaleza</title></head><body>'
                '<a href="/quem-somos">Quem somos</a><a href="/tratamentos">Tratamentos</a>'
                '<p>Atendendo na Aldeota desde 2009. Ligue (85) 99999-0000.</p>'
                '<a href="https://wa.me/5585999990000">WhatsApp</a></body></html>')
        self.assertEqual(B.pick_pages("https://sorrisoleve.com.br", page),
                         ["https://sorrisoleve.com.br/quem-somos", "https://sorrisoleve.com.br/tratamentos"])
        f = B.facts({"https://sorrisoleve.com.br": page})
        self.assertEqual(f["since"], 2009)
        self.assertEqual(f["phones"], ["(85) 99999-0000"])
        self.assertIn("botão de WhatsApp", f["tools_seen"])
        self.assertIn("agendamento online", f["tools_missing"])

if __name__ == "__main__":
    unittest.main()
