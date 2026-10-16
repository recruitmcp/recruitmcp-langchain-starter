"""Shared RecruitMCP MCP client setup."""
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

MCP_URL = os.getenv("RECRUITMCP_MCP_URL", "https://mcp.recruitmcp.com/mcp")

# Tools the starter agent may use. Outreach tools are deliberately left out:
# this starter only sources and previews. Add more names only on purpose.
ALLOWED_TOOLS = {
    "resolve_location", "resolve_area", "resolve_companies", "list_filter_values",
    "search_people", "enrich_profiles", "get_people_job", "get_account_overview",
    "get_guide",
}


def make_client() -> MultiServerMCPClient:
    key = os.environ.get("RECRUITMCP_KEY")
    if not key:
        raise SystemExit("Set RECRUITMCP_KEY (see .env.example).")
    return MultiServerMCPClient({
        "recruitmcp": {
            "transport": "streamable_http",
            "url": MCP_URL,
            "headers": {"Authorization": f"Bearer {key}"},
        }
    })


async def load_tools(client: MultiServerMCPClient):
    tools = await client.get_tools()
    return [t for t in tools if t.name in ALLOWED_TOOLS]
