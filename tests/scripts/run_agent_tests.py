#!/usr/bin/env python3
import json
from bti.agents.testing.golden_runner import GoldenTestRunner

if __name__ == "__main__":
    result = GoldenTestRunner().run()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["failed"] == 0 else 1)
