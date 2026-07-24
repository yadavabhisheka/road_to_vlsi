# Archii — Personal AI Agent Setup (Hermes Agent, self-hosted)

## What this is
Archii is a personal AI agent built on [Hermes Agent](https://github.com/NousResearch/hermes-agent)
(Nous Research, open-source, MIT licensed), configured to act as my
daily habit tracker, VLSI/DV learning mentor, and career copilot while
I job-hunt for an entry-level VLSI Design Verification role.

Everything in this setup is free — no paid tiers, no subscriptions.

## Stack
- **Runtime**: Hermes Agent, self-hosted on my own laptop (Ubuntu, XFCE4)
- **Model**: `openrouter/free` — OpenRouter's auto-router, which picks a
  working free model automatically instead of pinning to one model name
- **Gateway**: Telegram (via BotFather bot token)
- **Search**: DuckDuckGo (`ddgs`, free, no key)
- **TTS**: Microsoft Edge TTS (free, no key)
- **Browser**: Local headless Chromium (free, no key)

## Why `openrouter/free` instead of a named model
I initially pinned Archii to `qwen/qwen3-coder:free`, then switched to
`meta-llama/llama-3.3-70b-instruct:free` after Qwen's free tier was
pulled mid-setup — and hit the exact same HTTP 404 on Llama within
minutes. Free-tier model listings on OpenRouter rotate without notice,
so pinning to one name is fragile for something meant to run for a
year. `openrouter/free` routes to whatever's actually available,
trading a small amount of control for real reliability.

## Setup steps (what I actually ran)
1. Installed via the official install script:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
   ```
2. Connected a provider: `hermes setup` → OpenRouter → pasted a free
   API key from openrouter.ai/keys (Nous Portal's own OAuth login
   asked for a card during signup, so I skipped that path)
3. Selected the model: `hermes model` → entered `openrouter/free` as a
   custom model name
4. Selected terminal backend: Local (runs directly on my machine)
5. Enabled a trimmed tool set (21 of 25 available) — disabled Image
   Generation, Vision/Image Analysis, Session Search, Browser
   Automation, Computer Use, and other tools I won't use for this
   use case, since every enabled tool's schema adds to the fixed
   per-message context cost
6. Connected Telegram: `hermes setup` → Telegram → pasted a bot token
   from @BotFather
7. Skipped image generation and paid TTS providers — kept the free
   defaults (Microsoft Edge TTS, local browser)

## Result: baseline context cost
Trimming tools before adding my persona file dropped the fixed
per-message overhead from **22k tokens (11% of 200k context)** to
**12.3k tokens (6%)** — roughly halved, just from disabling tools I
won't use. Worth doing this trimming pass before loading any persona
or project context on top.

## Archii's role (from her persona file)
Three jobs, defined in `archii_persona.md`:
1. **Habit tracker** — logs daily study check-ins, tracks streaks
2. **VLSI/DV learning mentor** — grounded in my actual roadmap (Python,
   64 LeetCode problems, HDL, SystemVerilog/UVM, AI tooling)
3. **Career copilot** — tailors resume/cover-letter bullets, tracks
   companies I mention applying to

## What's next
- Daily/weekly logs written to this repo (see below)
- Eventually: an MCP server exposing my regression/coverage data to
  her directly, once that project exists

## Credit
Built with guidance from Claude (Anthropic) — I worked through the
install, the two mid-setup model failures, the tool-trimming pass, and
the persona design interactively rather than following a fixed script.