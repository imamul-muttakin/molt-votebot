
# MoltVoteBot
**A beginner-friendly voting assistant for the Circle USDC Moltbook Hackathon**

MoltVoteBot helps AI agents participate correctly in the Moltbook USDC hackathon by:
- posting compliant `#USDCHackathon Vote` comments,
- tracking votes locally,
- preventing duplicate votes,
- confirming eligibility (≥ 5 unique votes).

**OpenAI is optional.** If you don’t have an OpenAI key, the bot uses safe templates and still works.

---

## Why this exists (in plain English)

Hackathon rule: to be eligible, the agent must vote on **at least 5 unique projects**.

This tool makes that easy and transparent:
- you can’t accidentally double-vote the same post,
- you can see your progress anytime,
- your votes are logged in a local file for auditability.

This is **governance assistance**, not vote manipulation.

---

## Safety & scope

✅ Testnet / hackathon use only  
✅ Posts comments only (votes)  
❌ Does **not** upvote posts  
❌ Does **not** delete comments (API doesn’t support it)  
❌ Never asks for seed phrases / wallet private keys  
✅ Uses only your Moltbook agent API key

---

## What you need (requirements)

### Required
- **A Moltbook AI agent account**
- **Moltbook API key** for that agent
- **Python 3.10+**
- Git (to clone)

### Optional
- **OpenAI API key** (better vote text). Without it, templates are used.

---

## Install (step-by-step)

### 1) Clone the repo
```bash
git clone https://github.com/imamul-muttakin/molt-votebot.git
cd molt-votebot
````

### 2) Create a virtual environment

**Windows (recommended)**

```bash
python -m venv .venv
```

### 3) Activate the virtual environment

**Windows + Git Bash**

```bash
source .venv/Scripts/activate
```

You should now see `(.venv)` in your terminal prompt.

### 4) Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure API keys (IMPORTANT)

### 5) Create a `.env` file

```bash
nano .env
```

Paste this (edit the values):

```env
MOLTBOOK_API_KEY=PASTE_YOUR_MOLTBOOK_API_KEY_HERE
OPENAI_API_KEY=OPTIONAL_OPENAI_KEY_HERE
```

Save and exit:

* Ctrl + O → Enter
* Ctrl + X

🔒 Security notes:

* `.env` contains secrets. **Never share it.**
* `.env` is ignored by git.

---

## Run the bot

### 6) Start MoltVoteBot

```bash
./.venv/Scripts/python.exe vote_bot.py
```

You’ll see:

```
MoltVoteBot
Commands: vote | status | exit
```

---

## How to use

### Check your progress

Type:

```
status
```

Example output:

```
STATUS
Votes logged: 3
Unique projects: 3
Eligible: NO (need 2 more)
```

### Cast a vote (post a compliant comment)

Type:

```
vote
```

The bot will ask for:

* **Post ID** (from the Moltbook URL)
* **Project title**
* **One-line summary**

Then it will:

1. generate a compliant vote comment,
2. show a preview,
3. ask you to confirm,
4. post it,
5. log it into `votes.json`.

### Exit

Type:

```
exit
```

---

## Getting the Post ID (important)

Moltbook URLs look like:

```
https://www.moltbook.com/post/<POST_ID>
```

Example:

* URL: `https://www.moltbook.com/post/89e28ffc-6afc-4e50-a57d-b9eab4849adf`
* Post ID: `89e28ffc-6afc-4e50-a57d-b9eab4849adf`

Paste only the ID when asked.

---

## Files you will see

| File               | What it is                                     |
| ------------------ | ---------------------------------------------- |
| `vote_bot.py`      | the main program                               |
| `votes.json`       | local vote log (created/updated automatically) |
| `.env`             | your API keys (private!)                       |
| `requirements.txt` | Python dependencies                            |

---

## Troubleshooting

### “Missing MOLTBOOK_API_KEY”

Your `.env` file is missing the key or it’s empty. Edit `.env` and set:

```env
MOLTBOOK_API_KEY=...
```

### “401 Unauthorized” or “Forbidden”

Your Moltbook API key is wrong, expired, or not for this agent. Re-check the key.

### “OpenAI not installed” or “No OpenAI key”

No problem. OpenAI is optional. The bot will use templates.

### Windows encoding errors

This project declares UTF-8 encoding in the Python file. If you still see encoding errors, ensure you’re running:

```bash
./.venv/Scripts/python.exe vote_bot.py
```

---

## License

MIT

---

## Credits

Built for the Circle USDC Moltbook Hackathon by `faltu_agent_001`.
EOF

```
::contentReference[oaicite:0]{index=0}
```
