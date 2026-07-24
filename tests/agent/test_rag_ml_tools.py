from bti.rag.rag_corpus import RAGCorpusBuilder
from bti.rag.retriever import EvidenceRetriever
from bti.ml.model_router import MLModelRouter
from app import storage


def test_rag_index_build_and_search():
    build = RAGCorpusBuilder().build_default_index()
    assert build["indexed_records"] > 0
    matches = EvidenceRetriever().index.search("Albion Energy wallet policy", top_k=3)
    assert isinstance(matches, list)


def test_ml_router_scores_transaction():
    txn = storage.find("transaction_id", "TXN-000421")
    result = MLModelRouter().score(txn)
    assert "local_score" in result
    assert "anomaly_score" in result["local_score"]
