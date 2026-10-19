# Quickstart: RecruitMCP in Claude Desktop, Cursor and Claude Code

Connect RecruitMCP to your AI client and make your first MCP calls: resolve a place, preview a search for free, then run it.

MCP endpoint: `https://mcp.recruitmcp.com/mcp`

## 1. Get your free API key

Go to [recruitmcp.com/signup](https://recruitmcp.com/signup) (or click **Get your free API key** on [recruitmcp.com](https://recruitmcp.com)). Enter a workspace name and your email, then click **Create workspace**.

The next screen shows your API key once, with a **Copy** button. Copy it now: it is not emailed. Your free credits are added after you confirm your email.

The same screen shows one first call. It is a search preview (`dry_run=true`), so it spends nothing:

```bash
curl -sS -X POST 'https://api.recruitmcp.com/v1/people/search?dry_run=true' \
  -H "Authorization: Bearer $RECRUITMCP_KEY" \
  -H 'content-type: application/json' \
  -d '{"filters":{"current_job_titles":["Backend Engineer"],"geo_ids":["90009596"]},"limit":10}'
```

Keep the key out of your code and version control. Put it in an environment variable:

```bash
export RECRUITMCP_KEY=rmcp_live_...
```

Then click **Connect MCP**, or follow the next step.

Prefer the API? `POST /v1/workspaces` creates a workspace without the web page. See [recruitmcp.com/docs](https://recruitmcp.com/docs).

## 2. Connect your client

### Claude Desktop

Claude Desktop runs remote servers through `mcp-remote` (needs Node.js / `npx`). Add this to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "recruitmcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://mcp.recruitmcp.com/mcp",
        "--header",
        "Authorization: Bearer ${RECRUITMCP_KEY}"
      ],
      "env": {
        "RECRUITMCP_KEY": "rmcp_live_..."
      }
    }
  }
}
```

`mcp-remote` replaces `${RECRUITMCP_KEY}` with the value from `env`. Restart Claude Desktop after saving.

### Cursor

Add to `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):

```json
{
  "mcpServers": {
    "recruitmcp": {
      "url": "https://mcp.recruitmcp.com/mcp",
      "headers": {
        "Authorization": "Bearer ${env:RECRUITMCP_KEY}"
      }
    }
  }
}
```

Cursor uses `${env:NAME}`. A plain `$RECRUITMCP_KEY` is sent as literal text and will not authenticate.

### Claude Code

Add a `.mcp.json` to your project root:

```json
{
  "mcpServers": {
    "recruitmcp": {
      "type": "http",
      "url": "https://mcp.recruitmcp.com/mcp",
      "headers": {
        "Authorization": "Bearer ${RECRUITMCP_KEY}"
      }
    }
  }
}
```

Or from the command line (your shell expands the variable, so the key value itself is stored in your local Claude Code config):

```bash
claude mcp add --transport http recruitmcp https://mcp.recruitmcp.com/mcp \
  --header "Authorization: Bearer $RECRUITMCP_KEY"
```

Check the connection with `/mcp` inside Claude Code.

## 3. Your first MCP calls

Ask your client in plain language, for example *"Find backend engineers in Ghent, Belgium"*. Under the hood it makes these three calls.

### a. `resolve_location` (free)

Location filters take ids, not free text, so resolve the place first:

```json
{ "text": "Ghent, Belgium" }
```

Use the **Ghent metro area**, id `90009596`.

### b. `search_people` with `dry_run: true` (free)

```json
{
  "filters": {
    "current_job_titles": ["Backend Engineer"],
    "geo_ids": ["90009596"]
  },
  "limit": 10,
  "dry_run": true
}
```

A dry run charges nothing. It returns an estimate (the maximum is the `limit`), `requires_confirm`, and `cost.credits: 0`.

### c. Live search

Run the same call without `dry_run`. Search costs 1 credit per returned profile, charged once per workspace (seeing the same profile again is free). The response shows what you paid in `cost.credits`.

Results are profile stubs: name, title, company, location and profile id. To get the full profile, call `enrich_profiles` (2 credits per profile). Set `wait_seconds` to 25 or lower (25 is the maximum); if the job is still running, poll `get_people_job` until `status` is `completed` or `failed`. Stop on `failed` (it charges nothing) and on any error response.

## Good to know

- **Approval:** on MCP, a call above the key's approval threshold (500 credits when unset) returns `approval_required` with an estimate and a `confirm_token`, and charges nothing. Resend the call with `confirm_token` to run it.
- **REST:** paid REST calls need an `Idempotency-Key` header (not needed for `dry_run`), and return `X-Credits-Charged`.
- **Rate limit:** 120 requests per minute per key.
- **Contacts:** contact lookups return the full `emails` and `phones` lists plus `best_email` and `best_phone`, the suggested pick.
- **Tools you see** depend on your key's scopes; `tools/list` only shows tools the key may use.

Full reference: [recruitmcp.com/docs/mcp](https://recruitmcp.com/docs/mcp)
