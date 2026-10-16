# RecruitMCP LangChain starter

A minimal Python LangChain agent that sources candidates through the
[RecruitMCP](https://recruitmcp.com) MCP server (`https://mcp.recruitmcp.com/mcp`)
using [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters).

## 5-minute quickstart

1. **Get a key.** Go to [recruitmcp.com/signup](https://recruitmcp.com/signup), enter a workspace name and email, and copy the key (it starts with `rmcp_live_` and is shown once). See [quickstart.md](quickstart.md) for Claude Desktop, Cursor and Claude Code.
2. **Install** (Python 3.10+):
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env   # then fill in RECRUITMCP_KEY and OPENAI_API_KEY
   ```
3. **Smoke test (0 credits, no LLM):**
   ```bash
   python smoke_test.py
   ```
   Lists the tools, resolves "Ghent, Belgium" and dry-runs a search.
4. **Run the agent:**
   ```bash
   python agent.py "Find 10 backend developers in Ghent, Belgium"
   ```
   The agent resolves the location, calls `search_people` with `dry_run=true`,
   and shows the estimate before anything is spent.

## How it works

- **Auth:** `Authorization: Bearer $RECRUITMCP_KEY`, read from the environment. Never
  put the key in browser code or version control.
- **Tools:** this starter keeps only sourcing tools (`resolve_location`, `search_people`, `enrich_profiles`, …;
  see `ALLOWED_TOOLS` in `recruitmcp_client.py`). `tools/list` only shows the
  tools your key has scopes for.
- **Cost:** 1 credit per profile returned (once per workspace), 2 per live enrich.
  `dry_run=true` previews the cost and charges nothing.
- **Approval:** above the key's approval threshold (500 credits on MCP when unset)
  a call returns `approval_required` with an estimate and a `confirm_token`, and
  charges nothing. Resend the same call with `confirm_token` to run it.
- **Enrich jobs:** `enrich_profiles` waits at most `wait_seconds` (0–25). If the job
  is still running, poll `get_people_job`.
- **Filters:** never pass free text as a location or company; resolve it to ids first.

## License

MIT. Copyright (c) 2026 RecruitMCP. See [LICENSE](LICENSE).
