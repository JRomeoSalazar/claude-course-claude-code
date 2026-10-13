# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

The project is managed with `uv` (Python >= 3.10).

```bash
uv venv && source .venv/bin/activate   # create and activate the virtual env
uv pip install -e .                    # install in development mode

uv run main.py                         # start the MCP server (stdio transport)

uv run pytest                          # run all tests
uv run pytest tests/test_document.py   # run one test file
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf   # run one test
uv run pytest -k docx                  # run tests matching a keyword
```

`uv run` syncs `.venv` to `uv.lock`, so locked versions win over whatever `uv pip install -e .` resolved. No linter or formatter is configured.

## Code style

- Always apply appropriate types to function arguments.

## Architecture

An MCP server (named `docs`) exposing document conversion and processing tools to AI assistants.

- `main.py` is the only entry point: it creates the `FastMCP` instance and registers every tool. It contains no tool logic.
- `tools/` holds the tool implementations as plain Python functions, one module per domain (`math.py`, `document.py`). They do not import `mcp`, so they are unit-testable without a running server.
- `tests/` calls the tool functions directly; binary fixtures live in `tests/fixtures/`.

A function in `tools/` is **not** an MCP tool until it is registered in `main.py`. `add` and `document_path_markdown` are registered. `binary_document_to_markdown` in `tools/document.py` is deliberately not registered: it is the internal helper that `document_path_markdown` delegates to, since raw bytes are impractical to pass through an MCP call.

Document conversion goes through `markitdown` (installed with the `docx` and `pdf` extras): bytes are wrapped in a `BytesIO` and the format is passed as `StreamInfo(extension=...)`.

`mcp[cli]` is pinned to exactly `1.8.0`.

## Defining MCP tools

1. Write the tool as a plain function in the appropriate `tools/` module.
2. Register it in `main.py`:

   ```python
   from tools.my_module import my_function

   mcp.tool()(my_function)
   ```

The function's docstring and parameter metadata are what the AI assistant sees when deciding whether and how to call the tool, so they are part of the tool's interface, not optional documentation.

### Tool descriptions (docstrings)

Every tool docstring should:

- Begin with a one-line summary
- Provide a detailed explanation of the functionality
- Explain when to use (and when not to use) the tool
- Include usage examples with expected input/output

### Parameter descriptions

Describe every parameter with pydantic's `Field`, and give the function full type hints including the return type:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """Comprehensive docstring here"""
    # Implementation
```

`tools/math.py::add` and `tools/document.py::document_path_markdown` are reference examples that follow all of these conventions.
