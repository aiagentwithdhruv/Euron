# Sprint 1 Day 1: Claude Code + MCP — Live Class Notes

> **Date:** March 1, 2026 (Evening)
> **Duration:** ~2 hours
> **Format:** Live coding + demo (no slides, build live)
> **Audience:** Euron bootcamp students (developers, students, AI enthusiasts)

---

## Pre-Class Checklist

- [ ] Claude Desktop open with MCP servers connected (Gmail + Sheets at minimum)
- [ ] VS Code / Cursor open with Claude Code extension
- [ ] Terminal ready with `claude` CLI working
- [ ] Demo Gmail account ready (not personal — use test account)
- [ ] Google Sheets with test data open in browser tab
- [ ] `Euron/Gen-AI-2.O/MCP/` folder ready to show
- [ ] This CLASS-NOTES.md open as reference (second screen / split)
- [ ] Internet stable, phone on DND

---

## ACT 1 — HOOK (5 min)

### The Demo-First Opening

> **Don't say:** "Today we'll learn about MCP..."
> **Do this:** Open Claude Desktop and type live in front of everyone:

```
"Read my last 3 emails and summarize them"
```

Wait for it to actually pull real emails.

Then:

```
"Create a Google Sheet called 'Class Demo' with columns: Name, Email, Score. Add 3 sample rows."
```

Wait for it to create the sheet. Show it in the browser.

Then say:

> "That just happened. No code. No API. No Postman. Just a chat message. By the end of this class, YOUR Claude will be able to do this too. Let's set it up."

### Why This Works
- Students see the end result FIRST (creates desire)
- It's real, not a screenshot (builds trust)
- Simple enough to understand, powerful enough to impress

---

## ACT 2 — CONTEXT (10 min)

### What is MCP? (Simple Version)

> "Think of MCP like a USB port for AI."
>
> Your phone has a charging port. You can plug in a charger, a data cable, headphones — anything that fits. The port doesn't care what device it is, it just connects.
>
> MCP is the same thing for AI. It's a standard port. Any tool that speaks MCP can plug into any AI that supports MCP.
>
> - Gmail? Plug it in.
> - Database? Plug it in.
> - Your CRM? Plug it in.
> - Your own custom script? Plug it in.
>
> One protocol. Infinite tools.

### The Architecture (Draw This / Show Mermaid)

```
YOU (Natural Language)
    |
    v
CLAUDE (Desktop / Code / Cursor)
    |
    v  [MCP Protocol — stdio]
+----------------------------------+
|         MCP SERVERS              |
|                                  |
|  Gmail    Calendar    Sheets     |
|  Supabase MongoDB     S3        |
|  Your own custom scripts...     |
+----------------------------------+
    |           |           |
    v           v           v
  Google     Database    Cloud
   APIs       APIs      Storage
```

### Key Point to Emphasize

> "Without MCP, AI can only talk. With MCP, AI can DO."
>
> - Without MCP: "Here's how you would send an email..." (gives instructions)
> - With MCP: Actually sends the email. Done.

### 3 Ways to Use MCP

| Method | Where | Best For |
|--------|-------|----------|
| **Claude Desktop** | Desktop app | Quick tasks, non-developers |
| **Claude Code (CLI)** | Terminal | Developers, automation |
| **Cursor / VS Code** | IDE | Coding projects, building |

> "Today we'll set up all three. You pick which one fits your workflow."

---

## ACT 3 — BUILD (60-70 min)

### Part 1: Understanding the MCP Server (15 min)

> "An MCP server is just a Python file. Let me show you how simple it is."

Open `Euron/Gen-AI-2.O/MCP/email_mcp.py` and walk through:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Gmail")

@mcp.tool()
def send_email(to_email: str, subject: str, body: str) -> str:
    """Send an email via Gmail"""
    # ... sends email using Google API
    return "Email sent successfully"

@mcp.tool()
def read_recent_emails(limit: int = 5) -> str:
    """Read recent emails from inbox"""
    # ... fetches emails
    return formatted_emails

mcp.run(transport="stdio")
```

**Key points to narrate:**

1. **`FastMCP("Gmail")`** — gives your server a name
2. **`@mcp.tool()`** — this decorator makes any function available to AI
3. **Type hints** (`str`, `int`) — AI reads these to know what to pass
4. **Docstring** — AI reads this to decide WHEN to use the tool
5. **`mcp.run(transport="stdio")`** — connects via standard input/output (no ports, no HTTP)

> "That's it. 5 lines of boilerplate + your actual function logic = an MCP server."

### Part 2: Setup — Step by Step (20 min)

#### Step 1: Install FastMCP

```bash
pip install "mcp[cli]"
```

> "This installs the FastMCP library. One command."

#### Step 2: Create Your First MCP Server (LIVE CODING)

> "Let's build one from scratch. Right now. Together."

Create a new file `hello_mcp.py`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("HelloWorld")

@mcp.tool()
def greet(name: str) -> str:
    """Say hello to someone by name"""
    return f"Hello, {name}! Welcome to MCP. You're connected!"

@mcp.tool()
def add_numbers(a: int, b: int) -> str:
    """Add two numbers together"""
    return f"{a} + {b} = {a + b}"

@mcp.tool()
def current_time() -> str:
    """Get the current date and time"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

mcp.run(transport="stdio")
```

> "3 tools. 20 lines. That's a complete MCP server."

#### Step 3: Connect to Claude Desktop

Show where the config file lives:

```
macOS:  ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
```

Add the server:

```json
{
  "mcpServers": {
    "HelloWorld": {
      "command": "python3",
      "args": ["/full/path/to/hello_mcp.py"]
    }
  }
}
```

> "Save. Restart Claude Desktop. That's it."

**CHECKPOINT:** Show Claude Desktop recognizing the new server. Type "Say hello to the class" — it should use the greet tool.

#### Step 4: Connect to Cursor / VS Code

Show `.cursor/mcp.json` or VS Code settings:

```json
{
  "mcpServers": {
    "HelloWorld": {
      "command": "python3",
      "args": ["/full/path/to/hello_mcp.py"]
    }
  }
}
```

> "Same config format. Same server. Works everywhere."

#### Step 5: Connect to Claude Code (CLI)

Show project-level config:

```bash
# In your project root
cat .claude/settings.local.json
```

```json
{
  "mcpServers": {
    "HelloWorld": {
      "command": "python3",
      "args": ["/full/path/to/hello_mcp.py"]
    }
  }
}
```

> "Claude Code reads this automatically when you open the project."

**CHECKPOINT:** "We just connected the SAME server to 3 different AI tools. One server, three clients. That's the power of a standard protocol."

---

### Part 2B: Real MCP Server — Gmail (15 min)

> "Now let's go from hello world to real tools."

Show the Gmail MCP server setup:

#### Google Cloud Setup (Show, Don't Code)

1. Go to console.cloud.google.com
2. Create project → Enable Gmail API
3. Create OAuth credentials → Download `credentials.json`
4. Run `python authenticate.py` → Browser opens → Authorize → `token.json` saved

> "This is a one-time setup. 5 minutes. After this, your AI can read and send emails forever."

#### Connect Gmail to Claude Desktop

```json
{
  "mcpServers": {
    "Gmail": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/email_mcp.py"]
    }
  }
}
```

**LIVE DEMO:** Open Claude Desktop → "Read my last 3 emails" → Show real emails appearing.

> "This is the same thing you saw at the start. Now you know how it works."

---

### Part 3: Using Claude Code (15 min)

> "Claude Desktop is great for quick tasks. But for BUILDING things — Claude Code is the real power."

#### What is Claude Code?

```bash
# Install
npm install -g @anthropic-ai/claude-code

# Run
claude
```

> "Claude Code is Claude in your terminal. It can read files, write code, run commands, and now — with MCP — talk to external tools."

#### Demo: Claude Code + MCP

Open terminal in a project folder:

```bash
cd my-project
claude
```

Then type:

```
"Create an MCP server that connects to a SQLite database.
It should have tools to: list tables, query any table, insert a row.
Save it as db_mcp.py"
```

Watch Claude Code **write the entire MCP server** for you.

> "You just told AI to build an MCP server. It did. In 30 seconds. That's AI building its own tools."

#### Claude Code in Cursor / VS Code

> "You can also use Claude Code inside your IDE."

Show the Claude Code extension in VS Code sidebar. Same commands, same MCP access, but inside your editor.

**CHECKPOINT:** "So now you've seen 3 levels:
1. Claude Desktop — chat with tools
2. Claude Code CLI — build from terminal
3. Claude Code in IDE — build inside your editor"

---

## ACT 4 — DEPLOY / ADVANCED (15 min)

### Connecting Multiple Servers

> "The real magic is when you connect MULTIPLE servers and let AI orchestrate."

Show a config with 3+ servers:

```json
{
  "mcpServers": {
    "Gmail": { "command": "python3", "args": ["email_mcp.py"] },
    "Sheets": { "command": "python3", "args": ["sheets/sheets_mcp.py"] },
    "Supabase": {
      "command": "python3",
      "args": ["supabase/supabase_mcp.py"],
      "env": { "SUPABASE_URL": "...", "SUPABASE_KEY": "..." }
    }
  }
}
```

**LIVE DEMO — The Chain:**

```
"Read my last 5 emails, extract the sender names and subjects,
and save them to a new Google Sheet called 'Email Log'"
```

Watch Claude:
1. Use Gmail tool to read emails
2. Use Sheets tool to create spreadsheet
3. Use Sheets tool to write the data

> "One instruction. Three tools. Zero code. AI figured out the chain by itself."

### Environment Variables for Secrets

> "Never put passwords in your code."

```json
{
  "mcpServers": {
    "MyDB": {
      "command": "python3",
      "args": ["db_mcp.py"],
      "env": {
        "DATABASE_URL": "postgres://user:pass@host/db"
      }
    }
  }
}
```

> "Env vars go in the config. The MCP server reads them with `os.environ`. Credentials never touch your code."

---

## ACT 5 — EXERCISE + WRAP (10 min)

### Student Exercise

> "Your turn. Here's what I want you to build:"

**Exercise: Build Your First MCP Server**

1. Install FastMCP: `pip install "mcp[cli]"`
2. Create `my_first_mcp.py` with at least 2 tools:
   - Option A: A calculator (add, multiply, divide)
   - Option B: A file reader (read file, list files in directory)
   - Option C: A weather tool (using free API like open-meteo.com)
3. Connect it to Claude Desktop OR Cursor
4. Test it by chatting with Claude and asking it to use your tools
5. Share a screenshot in the WhatsApp group

**Bonus:** Connect the Gmail MCP server from `Euron/Gen-AI-2.O/MCP/` and send yourself an email through Claude.

### Wrap Up

> "What you learned today:"
> 1. MCP = USB port for AI (any tool plugs in)
> 2. An MCP server = a Python file with decorated functions
> 3. Same server works in Claude Desktop, Claude Code, and Cursor
> 4. You can chain multiple servers — AI figures out the orchestration
> 5. Claude Code can BUILD MCP servers for you (AI building its own tools)

### Preview Next Session

> "Day 2 (next session): We take what we built today and DEPLOY it. GitHub → production. Plus: triggers, webhooks, error handling — making automation run 24/7 without you."

---

## Quick Reference — Share With Students

### Config File Locations

| Platform | Config File Path |
|----------|-----------------|
| **Claude Desktop (Mac)** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Desktop (Win)** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Cursor** | `.cursor/mcp.json` (in project root) |
| **VS Code** | `.vscode/settings.json` or `.claude/settings.local.json` |
| **Claude Code CLI** | `.claude/settings.local.json` (in project root) |

### Minimal MCP Server Template

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool()
def my_tool(param: str) -> str:
    """What this tool does — AI reads this to decide when to use it"""
    # Your logic here
    return "result"

mcp.run(transport="stdio")
```

### Config Template

```json
{
  "mcpServers": {
    "ServerName": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

---

## Talking Points If Students Ask

**Q: "Is MCP only for Claude?"**
> "No. MCP is an open protocol. Cursor supports it. VS Code supports it. OpenAI's Codex supports it. Anyone can build an MCP client. Think of it like HTTP — it's a standard, not a product."

**Q: "Can I use it with ChatGPT?"**
> "Not directly yet. But MCP servers are just Python — you can wrap them as API endpoints for any LLM. The protocol itself is open source."

**Q: "Is it free?"**
> "The protocol is free. The servers you build are free. Claude Desktop is free. Claude Code requires an API key. Cursor has a free tier."

**Q: "How is this different from function calling / tool use?"**
> "Function calling = you define tools IN your API call. MCP = tools live OUTSIDE as independent servers. MCP servers are reusable — write once, plug into any AI. Function calling is per-request."

**Q: "Can I build an MCP server in JavaScript / Node?"**
> "Yes. There's a TypeScript SDK too. We use Python because it's simpler for beginners, but the protocol supports any language."

**Q: "What about security?"**
> "MCP runs locally on YOUR machine. Tools only have access to what you give them. Use env vars for credentials. Never commit tokens to Git."

---

*Last updated: 2026-03-01 | For: Euron Live Class Sprint 1 Day 1*
