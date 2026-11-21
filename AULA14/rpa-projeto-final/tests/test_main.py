import importlib.util
import unittest
from pathlib import Path


MAIN_PATH = Path(__file__).parent.parent / "src" / "main.py"
SPEC = importlib.util.spec_from_file_location("rpa_project_main", MAIN_PATH)
MAIN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MAIN)


class TestProjetoFinal(unittest.TestCase):
    def test_executar_descreve_o_projeto(self):
        self.assertIn("Projeto final RPA", MAIN.executar())


if __name__ == "__main__":
    unittest.main()
