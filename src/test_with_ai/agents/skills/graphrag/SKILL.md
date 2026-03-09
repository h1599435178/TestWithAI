--
name: graphrag
description: "Use GraphRAG to index documents and perform high-level or detailed queries on a knowledge graph. This is better than standard RAG for complex summaries and entity-relationship discovery."
metadata:
  {
    "test_with_ai":
      {
        "emoji": "🕸️",
        "requires": {
          "graphrag": ">=0.1.0"
        }
      }
  }
--

# GraphRAG Reference

GraphRAG is a powerful retrieval system that builds a knowledge graph from your documents. Use it when standard file search or RAG is insufficient, especially for:
- Summarizing entire document sets.
- Finding connections between different entities across multiple files.
- Understanding high-level themes.

## Workflow

1. **Initialization**: If the workspace is not yet initialized, call `graph_rag_init`.
2. **Add Files**: Use `graph_rag_add_file` to add the documents you want to index. Files should be text-based (txt, md).
3. **Indexing**: Call `graph_rag_index` to build the graph. This may take some time depending on the number of documents.
4. **Querying**: Use `graph_rag_query` to ask questions.
   - Use `method="global"` for broad, thematic questions or summaries.
   - Use `method="local"` for specific questions about entities or facts.

## Tool Usage

### `graph_rag_init`
Initializes the GraphRAG workspace.
```json
{}
```

### `graph_rag_add_file`
Adds a file to the input folder.
```json
{"file_path": "path/to/your/document.txt"}
```

### `graph_rag_index`
Starts the indexing process.
```json
{}
```

### `graph_rag_query`
Queries the graph.
```json
{"query": "What are the main themes in these documents?", "method": "global"}
```

## Notes
- GraphRAG requires an API key (GRAPHRAG_API_KEY or OPENAI_API_KEY) configured in the system environment.
- Indexing consumes tokens as it uses LLMs to extract entities and relationships.
- The default workspace is located at `~/.test_with_ai/graphrag`.
