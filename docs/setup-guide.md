# Setup Guide — Open Brain on Supabase (Beginner-Friendly)

This guide walks you through setting up your own Open Brain instance from scratch using Supabase as the database backend. No coding experience required. Estimated time: **30–45 minutes**.

---

## Before You Start: Credential Tracker

You will generate several API keys and passwords during this process. Some **cannot be retrieved again** after you navigate away from their generation page. Before doing anything else, open a notes file, spreadsheet, or password manager and label these slots:

| Label | Value (fill as you go) |
|---|---|
| Supabase Project Ref | |
| Supabase Database Password | |
| Supabase Project URL | |
| Supabase Secret Key | |
| OpenRouter API Key | |
| MCP Access Key | |
| MCP Connection URL | |

---

## Step 1: Create Your Supabase Project

Supabase is the hosted PostgreSQL database that stores all your thoughts.

1. Go to [supabase.com](https://supabase.com) and click **Start your project**
2. Sign up (signing in with GitHub is fastest)
3. In the dashboard, click **New project**
4. Fill in:
   - **Name**: `open-brain` (or any name you like)
   - **Database Password**: click "Generate a password", copy it to your credential tracker
   - **Region**: choose the one closest to you
5. Click **Create new project** and wait 1–2 minutes for it to initialize

**Save to credential tracker:**
- **Project Ref** — the random string visible in your browser URL bar after `/project/` (e.g., `abcdefghijklmnop`)

---

## Step 2: Set Up the Database Schema

All SQL runs in the Supabase **SQL Editor**. Navigate to it via the left sidebar.

### 2.1 Enable the pgvector Extension

1. In the left sidebar, go to **Database → Extensions**
2. Search for `vector`
3. Toggle **pgvector ON**

### 2.2 Create the Thoughts Table

In the SQL Editor, click **New query**, paste the following, and click **Run**:

```sql
create table thoughts (
  id uuid default gen_random_uuid() primary key,
  content text not null,
  embedding vector(1536),
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Fast vector similarity search
create index on thoughts using hnsw (embedding vector_cosine_ops);

-- Fast metadata filtering
create index on thoughts using gin (metadata);

-- Fast date sorting
create index on thoughts (created_at desc);

-- Auto-update updated_at on any row change
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger thoughts_updated_at
  before update on thoughts
  for each row
  execute function update_updated_at();
```

### 2.3 Create the Semantic Search Function

New query, paste and run:

```sql
create or replace function match_thoughts(
  query_embedding vector(1536),
  match_threshold float default 0.7,
  match_count int default 10,
  filter jsonb default '{}'::jsonb
)
returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float,
  created_at timestamptz
)
language plpgsql as $$
begin
  return query
  select
    t.id,
    t.content,
    t.metadata,
    1 - (t.embedding <=> query_embedding) as similarity,
    t.created_at
  from thoughts t
  where 1 - (t.embedding <=> query_embedding) > match_threshold
    and (filter = '{}'::jsonb or t.metadata @> filter)
  order by t.embedding <=> query_embedding
  limit match_count;
end;
$$;
```

### 2.4 Enable Row Level Security

Prevents unauthorized direct API access to your data:

```sql
alter table thoughts enable row level security;

create policy "Service role full access"
  on thoughts for all
  using (auth.role() = 'service_role');
```

### 2.5 Grant Service Role Permissions

New Supabase projects restrict permissions by default. Run this to give the service role full table access:

```sql
grant select, insert, update, delete on table public.thoughts to service_role;
```

### 2.6 Add Deduplication

Prevents the same thought from being stored twice, even if captured through different AI clients:

```sql
ALTER TABLE thoughts ADD COLUMN content_fingerprint TEXT;

CREATE UNIQUE INDEX idx_thoughts_fingerprint
  ON thoughts (content_fingerprint)
  WHERE content_fingerprint IS NOT NULL;

CREATE OR REPLACE FUNCTION upsert_thought(
  p_content TEXT,
  p_payload JSONB DEFAULT '{}'
)
RETURNS JSONB AS $$
DECLARE
  v_fingerprint TEXT;
  v_result JSONB;
  v_id UUID;
BEGIN
  -- Normalize the content and hash it
  v_fingerprint := encode(sha256(convert_to(
    lower(trim(regexp_replace(p_content, '\s+', ' ', 'g'))),
    'UTF8'
  )), 'hex');

  INSERT INTO thoughts (content, content_fingerprint, metadata)
  VALUES (
    p_content,
    v_fingerprint,
    COALESCE(p_payload->'metadata', '{}'::jsonb)
  )
  ON CONFLICT (content_fingerprint)
    WHERE content_fingerprint IS NOT NULL
  DO UPDATE
    SET updated_at = now(),
        metadata = thoughts.metadata || COALESCE(EXCLUDED.metadata, '{}'::jsonb)
  RETURNING id INTO v_id;

  v_result := jsonb_build_object('id', v_id, 'fingerprint', v_fingerprint);
  RETURN v_result;
END;
$$ LANGUAGE plpgsql;
```

### 2.7 Verify the Schema

In the left sidebar, go to **Table Editor** — you should see the `thoughts` table with columns:

`id` · `content` · `embedding` · `metadata` · `content_fingerprint` · `created_at` · `updated_at`

Go to **Database → Functions** — you should see both `match_thoughts` and `upsert_thought`.

---

## Step 3: Copy Your Supabase Credentials

1. In the left sidebar, click the **gear icon (Settings) → API Keys**
2. Copy to your credential tracker:
   - **Project URL** — shown at the top (e.g., `https://abcdefghijklmnop.supabase.co`)
   - **Secret key** — scroll to "Secret keys", copy the `default` key (or create a new one named `open-brain`)

> **Warning**: The secret key gives full database access. Treat it like a password. Never share it or commit it to version control.

---

## Step 4: Get an OpenRouter API Key

OpenRouter is the AI gateway used for generating embeddings (the vector representations of your thoughts).

1. Go to [openrouter.ai](https://openrouter.ai) and sign up
2. Navigate to [openrouter.ai/keys](https://openrouter.ai/keys)
3. Click **Create Key**, name it `open-brain`
4. **Copy it immediately** to your credential tracker — it won't be shown again
5. Add $5 in credits (this lasts months at personal scale)

---

## Step 5: Generate Your MCP Access Key

Your MCP server will be publicly reachable on the internet. This access key is what validates every request — anyone with it can read/write your thoughts.

**Mac/Linux** (run in Terminal):
```bash
openssl rand -hex 32
```

**Windows** (run in PowerShell):
```powershell
-join ((1..32) | ForEach-Object { '{0:x2}' -f (Get-Random -Maximum 256) })
```

Copy the 64-character output to your credential tracker as **MCP Access Key**.

> This is a permanent credential. Store it in your password manager.

---

## Step 6: Deploy the MCP Server

The MCP server is a Supabase Edge Function that you deploy once. It connects the AI protocol layer to your database.

### 6.1 Create a Project Folder

Create a new folder called `open-brain` anywhere on your computer (Documents, Desktop, etc.).

**Mac/Linux** — open Terminal:
```bash
cd ~/Documents/open-brain   # adjust path as needed
mkdir -p open-brain && cd open-brain
pwd  # should show your folder path
```

**Windows** — open PowerShell:
```powershell
cd "$env:USERPROFILE\Documents"
New-Item -ItemType Directory -Name open-brain
cd open-brain
Get-Location  # verify the path
```

### 6.2 Install the Supabase CLI

**Mac/Linux with Homebrew:**
```bash
brew install supabase/tap/supabase
supabase --version  # should print a version number
```

**Mac/Linux without Homebrew:**
```bash
npm install -g supabase
supabase --version
```

**Windows with Scoop** (recommended):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase
supabase --version
```

> If you don't have Scoop, install Node.js from nodejs.org and then run `npm install -g supabase`.

### 6.3 Log In to Supabase CLI

```bash
supabase login
```

This opens a browser tab. Authorize the CLI and return to your terminal.

### 6.4 Initialize and Link to Your Project

```bash
supabase init
ls supabase/   # verify a supabase/ folder was created

supabase link --project-ref YOUR_PROJECT_REF
```

Replace `YOUR_PROJECT_REF` with the value you saved in Step 1 (the random string from your dashboard URL).

### 6.5 Set Environment Secrets

```bash
supabase secrets set MCP_ACCESS_KEY=your-access-key-from-step-5
supabase secrets set OPENROUTER_API_KEY=your-openrouter-key-from-step-4
```

> `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are automatically injected by the Supabase runtime — you do **not** need to set those.

### 6.6 Download the Server Code

Run these three commands in order:

```bash
supabase functions new open-brain-mcp

curl -o supabase/functions/open-brain-mcp/index.ts \
  https://raw.githubusercontent.com/NateBJones-Projects/OB1/main/server/index.ts

curl -o supabase/functions/open-brain-mcp/deno.json \
  https://raw.githubusercontent.com/NateBJones-Projects/OB1/main/server/deno.json
```

Verify the download worked:
```bash
head -1 supabase/functions/open-brain-mcp/index.ts
```

You should see a line starting with `import` — **not** "Hello from Functions!". If you see the Hello message, the download failed; re-run the `curl` commands.

### 6.7 Deploy

```bash
supabase functions deploy open-brain-mcp --no-verify-jwt
```

When it finishes, verify with:
```bash
supabase functions list
```

You should see `open-brain-mcp` with status `ACTIVE`.

---

## Step 7: Build Your Connection URL and Verify

Your MCP server is now live at:
```
https://YOUR_PROJECT_REF.supabase.co/functions/v1/open-brain-mcp
```

Your **MCP Connection URL** (used in AI client configuration) is:
```
https://YOUR_PROJECT_REF.supabase.co/functions/v1/open-brain-mcp?key=YOUR_ACCESS_KEY
```

Save both to your credential tracker.

**Quick smoke test** — run this in your terminal (replace the values):
```bash
curl "https://YOUR_PROJECT_REF.supabase.co/functions/v1/open-brain-mcp?key=YOUR_ACCESS_KEY"
```

A valid JSON response means your server is live.

---

## Step 8: Connect an AI Client

### Claude Code (CLI)

```bash
claude mcp add --transport http open-brain \
  "https://YOUR_PROJECT_REF.supabase.co/functions/v1/open-brain-mcp?key=YOUR_ACCESS_KEY"
```

### Claude Desktop

1. Open Claude Desktop → **Settings → Connectors**
2. Click **Add custom connector**
3. Paste your MCP Connection URL

### Cursor

In `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "open-brain": {
      "transport": "http",
      "url": "https://YOUR_PROJECT_REF.supabase.co/functions/v1/open-brain-mcp?key=YOUR_ACCESS_KEY"
    }
  }
}
```

---

## Maintenance

### Rotate the access key

```bash
openssl rand -hex 32
supabase secrets set MCP_ACCESS_KEY=<new-key>
supabase functions deploy open-brain-mcp --no-verify-jwt
# Update the key in all AI client connection URLs
```

### Rotate the OpenRouter key

```bash
supabase secrets set OPENROUTER_API_KEY=<new-key>
```

### Update to latest server code

```bash
curl -o supabase/functions/open-brain-mcp/index.ts \
  https://raw.githubusercontent.com/NateBJones-Projects/OB1/main/server/index.ts
supabase functions deploy open-brain-mcp --no-verify-jwt
```

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `curl` returns 401 | Wrong or missing access key | Check `?key=` in URL matches `MCP_ACCESS_KEY` secret |
| `curl` returns 500 | Missing secrets or DB issue | Run `supabase functions logs open-brain-mcp` to see error |
| `head -1 index.ts` shows "Hello from Functions!" | `curl` download failed | Re-run the two `curl` commands in Step 6.6 |
| `supabase link` fails | Wrong project ref | Copy the ref again from your Supabase dashboard URL |
| Thoughts not found in search | Embeddings not generated | Check OpenRouter credits and `OPENROUTER_API_KEY` secret |

---

## Cost Reference

| Service | Free tier | Typical personal cost |
|---|---|---|
| Supabase | 500 MB database, 500K Edge Function invocations/month | $0/month |
| OpenRouter | Pay-per-use | ~$0.10/month |
| **Total** | | **~$0.10/month** |

---

## Resources

- Upstream project: [github.com/NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)
- Supabase docs: [supabase.com/docs](https://supabase.com/docs)
- OpenRouter: [openrouter.ai](https://openrouter.ai)
- MCP specification: [modelcontextprotocol.io](https://modelcontextprotocol.io)
