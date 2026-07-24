from bti.agents.testing.golden_runner import GoldenTestRunner


def test_agent_golden_cases_pass():
    result = GoldenTestRunner().run()
    assert result["failed"] == 0, result
