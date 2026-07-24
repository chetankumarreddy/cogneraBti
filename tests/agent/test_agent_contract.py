from bti.agents.cognira_agent import CogniraBTIAgent


def test_agent_analysis_contract():
    result = CogniraBTIAgent().analyse_transaction("TXN-000421", "compliance_officer")
    assert "transaction" in result
    assert "risk" in result
    assert "rules" in result
    assert result["transaction"]["txn_id"] == "TXN-000421"


def test_agent_narrative_contract():
    result = CogniraBTIAgent().generate_narrative("TXN-000421", "fca_examiner")
    assert "text" in result
    assert "guardian" in result
    assert result["persona"] == "fca_examiner"
