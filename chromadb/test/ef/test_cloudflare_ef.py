import os

import pytest

from chromadb.utils.embedding_functions import CloudflareWorkersAIEmbeddingFunction


def test_cf_ef_token_and_account() -> None:
    if "CF_API_TOKEN" not in os.environ or "CF_ACCOUNT_ID" not in os.environ:
        pytest.skip("CF_API_TOKEN and CF_ACCOUNT_ID not set")
    ef = CloudflareWorkersAIEmbeddingFunction(
        api_token=os.environ.get("CF_API_TOKEN", ""),
        account_id=os.environ.get("CF_ACCOUNT_ID"),
    )
    embeddings = ef(["test doc"])
    assert embeddings is not None
    assert len(embeddings) == 1
    assert len(embeddings[0]) > 0


def test_cf_ef_gateway() -> None:
    if "CF_API_TOKEN" not in os.environ or "CF_GATEWAY_ENDPOINT" not in os.environ:
        pytest.skip("CF_API_TOKEN and CF_GATEWAY_ENDPOINT not set")
    ef = CloudflareWorkersAIEmbeddingFunction(
        api_token=os.environ.get("CF_API_TOKEN", ""),
        gateway_url=os.environ.get("CF_GATEWAY_ENDPOINT"),
    )
    embeddings = ef(["test doc"])
    assert embeddings is not None
    assert len(embeddings) == 1
    assert len(embeddings[0]) > 0


def test_cf_ef_large_batch() -> None:
    if "CF_API_TOKEN" not in os.environ:
        pytest.skip("CF_API_TOKEN not set, not going to test Cloudflare EF.")

    ef = CloudflareWorkersAIEmbeddingFunction(api_token="dummy", account_id="dummy")
    with pytest.raises(ValueError, match="Batch too large"):
        ef(["test doc"] * 101)


def test_cf_ef_missing_account_or_gateway() -> None:
    if "CF_API_TOKEN" not in os.environ:
        pytest.skip("CF_API_TOKEN not set, not going to test Cloudflare EF.")
    with pytest.raises(
        ValueError, match="Please provide either an account_id or a gateway_url"
    ):
        CloudflareWorkersAIEmbeddingFunction(api_token="dummy")


def test_cf_ef_with_account_or_gateway() -> None:
    if "CF_API_TOKEN" not in os.environ:
        pytest.skip("CF_API_TOKEN not set, not going to test Cloudflare EF.")
    with pytest.raises(
        ValueError,
        match="Please provide either an account_id or a gateway_url, not both",
    ):
        CloudflareWorkersAIEmbeddingFunction(
            api_token="dummy", account_id="dummy", gateway_url="dummy"
        )
