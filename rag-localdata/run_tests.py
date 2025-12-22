#!/usr/bin/env python3
"""
Test runner script for the RAG implementation tests.
"""
import sys
import subprocess

def run_tests() -> bool:
    """Run the comprehensive test suite."""
    try:
        # Run pytest with verbose output and coverage
        result = subprocess.run([  # nosec
            sys.executable, "-m", "pytest",
            "test_ownData_comprehensive.py",
            "-v",
            "--tb=short",
            "--durations=10",
        ], cwd="rag-localdata")
    except (subprocess.SubprocessError, OSError) as e:
        print(f"Error running tests: {e}")
        return False
    else:
        return result.returncode == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)