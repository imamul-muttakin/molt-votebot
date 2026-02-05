import os, json
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MOLTBOOK_API_KEY = os.getenv("MOLTBOOK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not MOLTBOOK_API_KEY:
    raise SystemExit("Missing MOLTBOOK_API_KEY in .env")
if not OPENAI_API_KEY:
    raise SystemExit("Missing OPENAI_API_KEY in .env")

client = OpenAI(api_key=OPENAI_API_KEY)

VOTES_FILE = "votes.json"

def load_votes():
    if not os.path.exists(VOTES_FILE):
        return []
    try:
        with open(VOTES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except Exception:
        # If file corrupted, don't crash
        return []

def save_votes(votes):
    with open(VOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(votes, f, indent=2)

def already_voted(votes, post_id):
    return any(v.get("post_id") == post_id for v in votes)

def generate_vote(project_title: str, project_summary: str) -> str:
    prompt = f"""
Write a Moltbook hackathon vote comment.
Hard rules:
- First line MUST be exactly: #USDCHackathon Vote
- Then 3-5 bullet points.
- Be positive, technical, short.
- Do NOT claim you verified deployments; phrase as "I like" / "Nice approach".
Keep under 900 characters.

Project title: {project_title}
Project summary: {project_summary}
"""
    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )
    return r.choices[0].message.content.strip()

def post_comment(post_id: str, comment: str):
    url = f"https://www.moltbook.com/api/v1/posts/{post_id}/comments"
    headers = {
        "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.post(url, headers=headers, json={"content": comment}, timeout=30)
    resp.raise_for_status()
    return resp.json()

def status(votes):
    unique = len({v.get("post_id") for v in votes if v.get("post_id")})
    print(f"\nSTATUS: votes logged = {len(votes)}, unique projects = {unique}")
    if unique >= 5:
        print("✅ Eligible rule met (5 unique votes).")
    else:
        print(f"⏳ Need {5-unique} more unique vote(s).")

if __name__ == "__main__":
    votes = load_votes()

    cmd = input("Type 'vote' to post a vote, or 'status' to check progress: ").strip().lower()
    if cmd == "status":
        status(votes)
        raise SystemExit(0)
    if cmd != "vote":
        print("Unknown command. Use 'vote' or 'status'.")
        raise SystemExit(1)

    post_id = input("Post ID (from moltbook.com/post/...): ").strip()
    if already_voted(votes, post_id):
        print("⚠️ You already voted on this post_id (found in votes.json). Pick another.")
        status(votes)
        raise SystemExit(0)

    title = input("Project title: ").strip()
    summary = input("1-line summary: ").strip()

    comment = generate_vote(title, summary)

    print("\n--- Generated Vote Comment ---\n")
    print(comment)
    print("\n------------------------------\n")

    ok = input("Post this comment? (y/n): ").strip().lower()
    if ok == "y":
        out = post_comment(post_id, comment)

        votes.append({
            "post_id": post_id,
            "title": title,
            "summary": summary,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
        save_votes(votes)

        print("\n✅ Vote posted and logged to votes.json")
        status(votes)
        print("\nAPI response:")
        print(out)
    else:
        print("❌ Cancelled")

