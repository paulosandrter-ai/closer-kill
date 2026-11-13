import datetime
import importlib.util
import json
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("closer_proposal_test", os.path.join(HERE, "proposal.py"))
PR = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PR)
EXAMPLE = os.path.join(HERE, "..", "pipeline", "pipeline.example.json")


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        return json.load(fh)


def options():
    with open(os.path.join(HERE, "options.example.json"), encoding="utf-8") as fh:
        return json.load(fh)


class Build(unittest.TestCase):
    def test_the_bemtevi_proposal(self):
        data = example()
        deal = PR.P.find(data["deals"], "bemtevi-anuncios")
        md = PR.build(data, deal, options(), datetime.date(2026, 10, 29))
        self.assertIn("# Proposta pra Bem-te-vi Pet Spa", md)
        self.assertIn("Válida até 12/11/2026.", md)
        self.assertIn("- Talvez! Pode me mandar os valores?", md)
        self.assertIn("| Projeto completo | R$ 2.500 de implantação | R$ 2.500 |", md)
        self.assertIn("| Plano mensal (recomendado) | R$ 399/mês | R$ 4.788 |", md)
        self.assertIn("A maioria das clínicas recupera o investimento com 2 pacientes novos por mês.", md)

    def test_bad_options_are_refused(self):
        for bad in ([], options() * 2, [{"name": "Free", "includes": ["x"]}],
                    [dict(o, recommended=True) for o in options()]):
            with self.assertRaises(PR.ProposalError):
                PR.check_options(bad)


class Record(unittest.TestCase):
    def test_record_refuses_placeholders_then_logs(self):
        tmp = tempfile.mkdtemp()
        cwd = os.getcwd()
        try:
            os.chdir(tmp)
            data = example()
            deal = PR.P.find(data["deals"], "bemtevi-anuncios")
            md = PR.build(data, deal, options(), datetime.date(2026, 10, 29))
            os.makedirs(PR.OUT_DIR)
            path = os.path.join(PR.OUT_DIR, "bem-te-vi-pet-spa.md")
            with open(path, "w") as fh:
                fh.write(md)
            self.assertFalse(PR.record(data, "bemtevi-anuncios", "yes", "2026-10-29T16:00")[0])
            with open(path, "w") as fh:
                fh.write(md.replace("- [Claude: 3 to 5 lines, what they get and by when]", "- Ads live in 7 days"))
            self.assertFalse(PR.record(data, "bemtevi-anuncios", "sure", "2026-10-29T16:00")[0])
            ok, msg = PR.record(data, "bemtevi-anuncios", "yes", "2026-10-29T16:00")
            self.assertTrue(ok, msg)
            self.assertEqual(deal["stage"], "proposal")
            self.assertIn("R$ 2.500 de implantação / R$ 399/mês", data["activities"][-1]["text"])
            self.assertEqual(PR.P.validate(data)[0], [])
        finally:
            os.chdir(cwd)
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
