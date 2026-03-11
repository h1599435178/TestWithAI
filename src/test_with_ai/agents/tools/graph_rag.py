# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
import logging
import sys
from pathlib import Path
from typing import Literal, Optional

from agentscope.message import TextBlock
from agentscope.tool import ToolResponse

from ...constant import WORKING_DIR
from ...envs.store import load_envs

logger = logging.getLogger(__name__)

# Default GraphRAG workspace directory
GRAPHRAG_ROOT = WORKING_DIR / "graphrag"
GRAPHRAG_INPUT = GRAPHRAG_ROOT / "input"
GRAPHRAG_VENV = GRAPHRAG_ROOT / ".venv"


def _get_graphrag_python() -> str:
    """Return the path to the Python executable in the GraphRAG venv."""
    if os.name == "nt":  # Windows
        python_exe = GRAPHRAG_VENV / "Scripts" / "python.exe"
    else:  # Linux / macOS
        python_exe = GRAPHRAG_VENV / "bin" / "python"
    return str(python_exe)


def _check_graphrag_installed() -> bool:
    """Check if the graphrag package is installed in its dedicated venv."""
    python_exe = _get_graphrag_python()
    if not os.path.exists(python_exe):
        return False
    try:
        # Check if graphrag is importable in that environment
        subprocess.run(
            [python_exe, "-c", "import graphrag"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _ensure_graphrag_dirs() -> None:
    """Ensure the GraphRAG root and input directories exist."""
    GRAPHRAG_ROOT.mkdir(parents=True, exist_ok=True)
    GRAPHRAG_INPUT.mkdir(parents=True, exist_ok=True)


async def _ensure_installed() -> Optional[ToolResponse]:
    """Ensure GraphRAG is installed in its dedicated virtual environment."""
    if _check_graphrag_installed():
        return None

    _ensure_graphrag_dirs()
    logger.info("GraphRAG not found in isolated environment. Setting up venv...")

    try:
        # 1. Create venv
        subprocess.run(
            [sys.executable, "-m", "venv", str(GRAPHRAG_VENV)],
            check=True,
            capture_output=True,
        )

        # 2. Install graphrag in the venv
        python_exe = _get_graphrag_python()
        logger.info(f"Installing GraphRAG into {GRAPHRAG_VENV}...")
        
        # Use a more relaxed installation for Python 3.10 to avoid conflicts
        # Older graphrag versions work better on 3.10
        subprocess.run(
            [python_exe, "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [python_exe, "-m", "pip", "install", "graphrag"],
            check=True,
            capture_output=True,
        )
        return None
    except Exception as e:
        logger.exception("Failed to isolate GraphRAG environment")
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=(
                        "GraphRAG isolation failed. This tool requires a separate "
                        f"environment due to dependency conflicts. Error: {str(e)}"
                    ),
                ),
            ],
        )


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
    """Initialize the GraphRAG workspace."""
    if res := await _ensure_installed():
        return res
    _ensure_graphrag_dirs()
    python_exe = _get_graphrag_python()
    try:
        result = subprocess.run(
            [
                python_exe,
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


async def graph_rag_add_file(file_path: str) -> ToolResponse:
    """Add a file to the GraphRAG indexing input directory."""
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
    """Run the GraphRAG indexing process."""
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

    python_exe = _get_graphrag_python()
    try:
        result = subprocess.run(
            [python_exe, "-m", "graphrag.index", "--root", str(GRAPHRAG_ROOT)],
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
    """Query the GraphRAG index."""
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

    python_exe = _get_graphrag_python()
    try:
        result = subprocess.run(
            [
                python_exe,
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
