--
name: rerank
description: "Re-rank search results using a more accurate model to refine initial vector search or full-text search results."
metadata:
  {
    "test_with_ai":
      {
        "emoji": "🎯",
        "requires": {}
      }
  }
--

# Rerank Reference

Standard semantic search (vector search) is fast but sometimes misses the exact context or nuance. Re-ranking is a second pass that uses a more powerful "Cross-Encoder" model to compare your query against each candidate result more deeply.

Use this tool when:
- The initial `memory_search` or `file_search` results seem irrelevant.
- You have many search results and need to find the single most important one.
- You want to reduce Token consumption by only passing the absolute best context to the LLM.

## How to Use

1. **Perform initial search**: Run `memory_search` or `file_search` to get a broad set of results.
2. **Extract snippets**: Collect the text content of the results you want to refine.
3. **Call `rerank_results`**:
   ```json
   {
     "query": "What is the login timeout setting?",
     "documents": [
       "Snippet 1 from memory...",
       "Snippet 2 from docs...",
       "Snippet 3 from code..."
     ],
     "top_n": 3
   }
   ```
4. **Use refined context**: The tool will return the top snippets re-ordered by relevance score. Use these for your final answer or action.

## Notes

- Reranking uses an external API (DashScope by default).
- It is much more accurate than vector similarity because it looks at the interaction between query and document.
- Only rerank documents that are somewhat related; it cannot find missing information that wasn't in the initial search results.
