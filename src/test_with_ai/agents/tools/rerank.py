# -*- coding: utf-8 -*-
"""Rerank tool for refining search results using cross-encoders or APIs."""
import logging
import os
from typing import List, Dict, Any, Optional

import httpx
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse

logger = logging.getLogger(__name__)


async def rerank_results(
    query: str,
    documents: List[str],
    top_n: int = 5,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: str = "gte-rerank",
) -> ToolResponse:
    """
    Re-rank search results using a Rerank API (e.g., DashScope).

    This tool takes a query and a list of document snippets, and returns them
    re-ordered by relevance. This is much more accurate than standard vector
    search but more expensive. Use this to refine results from memory_search
    or file_search when the initial results are too broad or noisy.

    Args:
        query (`str`):
            The search query used to rank documents.
        documents (`List[str]`):
            A list of document snippets to be re-ranked.
        top_n (`int`, optional):
            Maximum number of re-ranked results to return. Defaults to 5.
        api_key (`str`, optional):
            API key for the Rerank service. If not provided, will look for
            DASHSCOPE_API_KEY in environment.
        base_url (`str`, optional):
            Base URL for the Rerank service. Defaults to DashScope.
        model (`str`, optional):
            The Rerank model to use. Defaults to "gte-rerank".

    Returns:
        `ToolResponse`:
            Re-ranked documents with their new scores.
    """
    if not documents:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text="No documents provided for reranking.",
                ),
            ],
        )

    api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text="Error: Rerank API key (DASHSCOPE_API_KEY) not found.",
                ),
            ],
        )

    base_url = (
        base_url
        or "https://dashscope.aliyuncs.com/api/v1/rerank"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "input": {
            "query": query,
            "documents": documents,
        },
        "parameters": {
            "top_n": top_n,
            "return_documents": True,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        results = data.get("output", {}).get("results", [])
        
        output_text = f"Re-ranked top {len(results)} results:\n\n"
        for i, res in enumerate(results):
            score = res.get("relevance_score", 0)
            doc = res.get("document", {}).get("text", "")
            output_text += f"[{i+1}] (Score: {score:.4f})\n{doc}\n\n"

        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=output_text.strip(),
                ),
            ],
        )

    except Exception as e:
        logger.exception("Rerank failed")
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"Error: Rerank failed due to {str(e)}",
                ),
            ],
        )
