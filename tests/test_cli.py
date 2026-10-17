"""Test de la interfaz de línea de comandos."""

import io
import unittest
from contextlib import redirect_stdout

from bg_pricing.cli import main


class CliTests(unittest.TestCase):
    def test_main_prints_interval(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["--steps", "2", "--branches", "3", "--replications", "10", "--seed", "1"])
        self.assertEqual(code, 0)
        output = buffer.getvalue()
        self.assertIn("intervalo", output)
        self.assertIn("estimador bajo", output)
        self.assertIn("estimador alto", output)


if __name__ == "__main__":
    unittest.main()
