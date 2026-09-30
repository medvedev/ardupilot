#!/usr/bin/env python3
"""Compile-time validation of the custom EKF3 no-aiding noise ceiling.

AP_FLAKE8_CLEAN
"""

import pathlib
import shutil
import subprocess
import tempfile
import unittest


class TestNoAidBuildLimit(unittest.TestCase):
    def compile_limit(self, value=None, expected=None):
        compiler = shutil.which("c++")
        self.assertIsNotNone(compiler, "A C++ compiler is required")
        root = pathlib.Path(__file__).resolve().parents[3]
        source = '#include "AP_NavEKF3/AP_NavEKF3_config.h"\n'
        if expected is not None:
            source += 'static_assert(EK3_NOAID_M_NSE_MAX == %s, "Unexpected ceiling");\n' % expected
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "check.cpp"
            path.write_text(source)
            command = [compiler, "-std=c++11", "-fsyntax-only", "-I", str(root / "libraries")]
            if value is not None:
                command.append("-DEK3_NOAID_M_NSE_MAX=" + value)
            command.append(str(path))
            return subprocess.run(command, capture_output=True, text=True)

    def test_stock_ceiling(self):
        result = self.compile_limit(expected="50.0f")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_custom_ceiling_and_boundaries(self):
        for value in ("0.5f", "50.0f", "1000.0f", "10000.0f"):
            with self.subTest(value=value):
                result = self.compile_limit(value=value, expected=value)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_out_of_range_ceiling_rejected(self):
        for value in ("-1.0f", "0.0f", "0.49f", "10001.0f"):
            with self.subTest(value=value):
                result = self.compile_limit(value=value)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("must be between 0.5 and 10000 m", result.stderr)

    def test_nonfinite_ceiling_rejected(self):
        for value in ("__builtin_inff()", "__builtin_nanf(\"\")"):
            with self.subTest(value=value):
                result = self.compile_limit(value=value)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("AP_NavEKF3_config.h", result.stderr)


if __name__ == "__main__":
    unittest.main()
