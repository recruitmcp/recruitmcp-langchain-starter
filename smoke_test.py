"""No-LLM smoke test: lists tools, resolves a place, dry-runs a search. Spends 0 credits."""
import asyncio, json
from recruitmcp_client import make_client


def text(res):
    return res if isinstance(res, str) else json.dumps(res, default=str)[:600]


async def main():
    client = make_client()
    tools = {t.name: t for t in await client.get_tools()}
    print(f"{len(tools)} tools:", ", ".join(sorted(tools)))
    loc = await tools["resolve_location"].ainvoke({"text": "Ghent, Belgium"})
    print("resolve_location:", text(loc)[:400])
    est = await tools["search_people"].ainvoke({
        "filters": {"current_job_titles": ["Backend Developer"]},
        "limit": 10, "dry_run": True,
    })
    print("search_people dry_run:", text(est)[:600])

asyncio.run(main())
