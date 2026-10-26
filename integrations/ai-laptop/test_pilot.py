import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).with_name("pilot_check.py")
spec = importlib.util.spec_from_file_location("pilot_check", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestPilot(unittest.TestCase):
    def test_closed_port(self):
        self.assertFalse(module.listening(1))
    def test_absent_http(self):
        self.assertIsNone(module.status("http://127.0.0.1:1/health/readiness"))
    def test_missing_command(self):
        self.assertIsNone(module.cmd(["/nonexistent-hermes-test-executable"])["exit_code"])

if __name__ == "__main__":
    unittest.main()
