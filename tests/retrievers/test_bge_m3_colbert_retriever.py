from typing import Generator

import pytest

from vidore_benchmark.retrievers.bge_m3_colbert_retriever import BGEM3ColbertRetriever
from vidore_benchmark.utils.testing_utils import tear_down_torch


@pytest.fixture(scope="module")
def retriever() -> Generator[BGEM3ColbertRetriever, None, None]:
    yield BGEM3ColbertRetriever()
    tear_down_torch()


@pytest.mark.slow
def test_forward_queries(retriever: BGEM3ColbertRetriever, queries_fixtures):
    embeddings_queries = retriever.forward_queries(queries_fixtures, batch_size=1)
    assert len(embeddings_queries) == len(queries_fixtures)


@pytest.mark.slow
def test_forward_documents(retriever: BGEM3ColbertRetriever, document_ocr_text_fixture):
    embeddings_docs = retriever.forward_documents(document_ocr_text_fixture, batch_size=1)
    assert len(embeddings_docs) == len(document_ocr_text_fixture)


@pytest.mark.slow
def test_get_scores(retriever: BGEM3ColbertRetriever, queries_fixtures, document_ocr_text_fixture):
    emb_query = retriever.forward_queries(queries_fixtures, batch_size=1)
    emb_doc = retriever.forward_documents(document_ocr_text_fixture, batch_size=1)
    scores = retriever.get_scores(emb_query, emb_doc)
    assert scores.shape == (len(queries_fixtures), len(document_ocr_text_fixture))
