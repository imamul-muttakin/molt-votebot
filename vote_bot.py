# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

# Optional OpenAI
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

load_dotenv()

MOLTBOOK_API_KEY = os.getenv("MOLTBOOK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not MOLTBOOK_API_KEY:
    raise SystemExit("Missing MOLTBOOK_API_KEY in .env")

client = None
if OPENAI_API_KEY and OpenAI:
    client = OpenAI(api_key=OPENAI_API_KEY)

VOTES_FILE = "votes.json"


def load_votes():
    if not os.path.exists(VOTES_FILE):
        return []
    try:
        with open(VOTES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_votes(votes):
    with open(VOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(votes, f, indent=2)


def already_voted(votes, post_id):
    return any(v["post_id"] == post_id for v in votes)


def generate_vote(title, summary):
    if client:
        prompt = f"""
Write a Moltbook hackathon vote comment.

Rules:
- First line must be exactly: #USDCHackathon Vote
- Use 3–5 bullet points
- Be technical and positive
- Under 900 characters

Project title: {title}
Summary: {summary}
"""
        r = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        return r.choices[0].message.content.strip()

    return f"""#USDCHackathon Vote
- Interesting concept: {title}
- Clear focus: {summary}
- Useful for agent workflows
- Looking forward to real-world usage"""


def post_comment(post_id, content):
    url = f"https://www.moltbook.com/api/v1/posts/{post_id}/comments"
    headers = {
        "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
        "Content-Type": "application/json",
    }
    r = requests.post(url, headers=headers, json={"content": content}, timeout=30)
    r.raise_for_status()
    return r.json()


def show_status(votes):
    unique = len({v["post_id"] for v in votes})
    print("\nSTATUS")
    print(f"Votes logged: {len(votes)}")
    print(f"Unique projects: {unique}")
    if unique >= 5:
        print("Eligible: YES")
    else:
        print(f"Eligible: NO (need {5 - unique} more)")


if __name__ == "__main__":
    votes = load_votes()

    print("\nMoltVoteBot")
    print("Commands: vote | status | exit\n")

    cmd = input("Command: ").strip().lower()

    if cmd == "exit":
        raise SystemExit(0)

    if cmd == "status":
        show_status(votes)
        raise SystemExit(0)

    if cmd != "vote":
        print("Unknown command")
        raise SystemExit(1)

    post_id = input("Post ID: ").strip()

    if already_voted(votes, post_id):
        print("Already voted for this project.")
        show_status(votes)
        raise SystemExit(0)

    title = input("Project title: ").strip()
    summary = input("One-line summary: ").strip()

    comment = generate_vote(title, summary)

    print("\n--- Vote Preview ---\n")
    print(comment)
    print("\n--------------------\n")

    if input("Post this vote? (y/n): ").lower() != "y":
        print("Cancelled.")
        raise SystemExit(0)

    post_comment(post_id, comment)

    votes.append({
        "post_id": post_id,
        "title": title,
        "summary": summary,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    })
    save_votes(votes)

    print("Vote posted successfully.")
    show_status(votes)
