import importlib.util
import json
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("closer_contract_test", os.path.join(HERE, "contract.py"))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
EXAMPLE = os.path.join(HERE, "..", "pipeline", "pipeline.example.json")

REEL = [("Serviços", "Um site com agendamento online e a gestão de uma campanha de Google Ads pra Clínica Sorriso Leve."),
        ("Valor", "R$ 399 por mês, sem taxa de implantação, pago todo mês por Pix ou boleto."),
        ("Prazo", "Mensal, sem fidelidade. Cancela quando quiser com 30 dias de aviso."),
        ("Entrega", "Site no ar em até 14 dias da assinatura.")]


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        return json.load(fh)


class Build(unittest.TestCase):
    def test_the_reel_agreement(self):
        data = example()
        deal = C.P.find(data["deals"], "sorriso-leve-site")
        md = C.build(data, deal, "29 de outubro de 2026", REEL)
        self.assertTrue(md.startswith("# Contrato de Prestação de Serviços"))
        self.assertIn("CONTRATADA: **Sua Agência**. CONTRATANTE: **Clínica Sorriso Leve**.", md)
        self.assertIn("## 2. Valor\n\nR$ 399 por mês, sem taxa de implantação", md)
        self.assertIn("Lei 13.709/2018", md)
        self.assertIn("## 9. Alterações", md)
        self.assertIn("## 10. Foro", md)
        self.assertIn("Daniela Rocha, Clínica Sorriso Leve: ______", md)
        html = C.to_html(md)
        self.assertIn("<h1>Contrato de Prestação de Serviços</h1>", html)
        self.assertIn("<strong>Sua Agência</strong>", html)

    def test_empty_sections_are_refused(self):
        data = example()
        deal = C.P.find(data["deals"], "sorriso-leve-site")
        with self.assertRaises(C.ContractError):
            C.build(data, deal, "today", [("Fee", "[fill: fee]")])

    def test_fee_is_checked_against_the_call(self):
        data = example()
        deal = C.P.find(data["deals"], "sorriso-leve-site")
        self.assertEqual(C.check_fee(data, deal, "R$ 399 por mês"), [])
        self.assertEqual(C.check_fee(data, deal, "R$ 399,00 por mês"), [])
        self.assertTrue(C.check_fee(data, deal, "R$ 349 por mês"))
        self.assertTrue(C.check_fee(data, deal, "Mensal, como combinado"))


class Record(unittest.TestCase):
    def test_record_needs_a_draft_and_a_yes(self):
        tmp = tempfile.mkdtemp()
        cwd = os.getcwd()
        try:
            os.chdir(tmp)
            data = example()
            deal = C.P.find(data["deals"], "jasmim-agendamento")
            self.assertFalse(C.record(data, "jasmim-agendamento", "yes", "2026-11-03T11:00")[0])
            md_path, html_path, _ = C.paths_for(data, deal)
            os.makedirs(C.OUT_DIR)
            with open(md_path, "w") as fh:
                fh.write("x")
            with open(html_path, "w") as fh:
                fh.write("x")
            self.assertFalse(C.record(data, "jasmim-agendamento", "yes to all", "2026-11-03T11:00")[0])
            ok, msg = C.record(data, "jasmim-agendamento", "yes", "2026-11-03T11:00")
            self.assertTrue(ok, msg)
            self.assertEqual(deal["stage"], "contract-sent")
            self.assertEqual(C.P.validate(data)[0], [])
        finally:
            os.chdir(cwd)
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
