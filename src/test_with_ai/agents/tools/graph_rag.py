# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
import logging
import sys
from pathlib import Path
from typing import Literal

from agentscope.message import TextBlock
from agentscope.tool import ToolResponse

from ...constant import WORKING_DIR
from ...envs.store import load_envs

logger = logging.getLogger(__name__)

# Default GraphRAG workspace directory
GRAPHRAG_ROOT = WORKING_DIR / "graphrag"
GRAPHRAG_INPUT = GRAPHRAG_ROOT / "input"


def _check_graphrag_installed() -> bool:
    """Check if the graphrag package is installed."""
    try:
        import graphrag  # noqa: F401

        return True
    except ImportError:
        return False


def _ensure_graphrag_dirs() -> None:
    """Ensure the GraphRAG root and input directories exist."""
    GRAPHRAG_ROOT.mkdir(parents=True, exist_ok=True)
    GRAPHRAG_INPUT.mkdir(parents=True, exist_ok=True)


async def _ensure_installed() -> Optional[ToolResponse]:
    """Ensure the GraphRAG package is installed, or try to install it."""
    if not _check_graphrag_installed():
        logger.info("GraphRAG not installed, attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "graphrag"])
            return None
        except Exception as e:
            return ToolResponse(
                content=[
                    TextBlock(
                        type="text",
                        text=f"GraphRAG is not installed and failed to install: {str(e)}",
                    ),
                ],
            )
    return None


def _setup_env() -> bool:
    """Setup .env file in the GraphRAG root directory using current environment variables."""
    envs = load_envs()
    api_key = envs.get("GRAPHRAG_API_KEY") or envs.get("OPENAI_API_KEY")
    if not api_key:
        logger.warning(
            "No API key found for GraphRAG. Please set GRAPHRAG_API_KEY or OPENAI_API_KEY.",
        )
        return False

    env_path = GRAPHRAG_ROOT / ".env"
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(f"GRAPHRAG_API_KEY={api_key}\n")
    return True


async def graph_rag_init() -> ToolResponse:
    """Initialize the GraphRAG workspace.

    This creates the necessary directory structure and configuration files.
    """
    if res := await _ensure_installed():
        return res
    _ensure_graphrag_dirs()
    try:
        # Run graphrag init via CLI
        result = subprocess.run(
            [
                "python",
                "-m",
                "graphrag.index",
                "--init",
                "--root",
                str(GRAPHRAG_ROOT),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        _setup_env()
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"GraphRAG workspace initialized at {GRAPHRAG_ROOT}.\n{result.stdout}",
                ),
            ],
        )
    except subprocess.CalledProcessError as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"Failed to initialize GraphRAG: {e.stderr}",
                ),
            ],
        )
    except Exception as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"An unexpected error occurred: {str(e)}",
                ),
            ],
        )


async def graph_rag_add_file(file_path: str) -> ToolResponse:
    """Add a file to the GraphRAG indexing input directory.

    Args:
        file_path: Path to the source file to be indexed.
    """
    if res := await _ensure_installed():
        return res
    _ensure_graphrag_dirs()
    src_path = Path(file_path)
    if not src_path.is_absolute():
        src_path = WORKING_DIR / file_path

    if not src_path.exists():
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"Error: File {src_path} does not exist.",
                ),
            ],
        )

    try:
        dest_path = GRAPHRAG_INPUT / src_path.name
        shutil.copy2(src_path, dest_path)
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"File {src_path.name} added to GraphRAG input directory.",
                ),
            ],
        )
    except Exception as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"Failed to add file: {str(e)}",
                ),
            ],
        )


async def graph_rag_index() -> ToolResponse:
    """Run the GraphRAG indexing process on all files in the input directory."""
    if res := await _ensure_installed():
        return res
    _ensure_graphrag_dirs()
    if not _setup_env():
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text="Error: API key not configured for GraphRAG.",
                ),
            ],
        )

    try:
        # Run graphrag index via CLI
        # This can be time-consuming
        result = subprocess.run(
            ["python", "-m", "graphrag.index", "--root", str(GRAPHRAG_ROOT)],
            capture_output=True,
            text=True,
            check=True,
        )
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"GraphRAG indexing completed.\n{result.stdout}",
                ),
            ],
        )
    except subprocess.CalledProcessError as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"Indexing failed: {e.stderr}",
                ),
            ],
        )


async def graph_rag_query(
    query: str,
    method: Literal["global", "local"] = "global",
) -> ToolResponse:
    """Query the GraphRAG index.

    Args:
        query: The question or query to ask the knowledge graph.
        method: The query method. 'global' is better for high-level summaries,
                'local' is better for specific entity details.
    """
    if res := await _ensure_installed():
        return res
    _ensure_graphrag_dirs()
    if not _setup_env():
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text="Error: API key not configured for GraphRAG.",
                ),
            ],
        )

    try:
        # Run graphrag query via CLI
        result = subprocess.run(
            [
                "python",
                "-m",
                "graphrag.query",
                "--root",
                str(GRAPHRAG_ROOT),
                "--method",
                method,
                query,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=result.stdout,
                ),
            ],
        )
    except subprocess.CalledProcessError as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"Query failed: {e.stderr}",
                ),
            ],
        )
