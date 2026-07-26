import os
import re
from github import Github, Auth

def _extract_limit(user_query: str, default_limit: int = 5) -> int:
    """Extracts requested numeric limit from query if specified (e.g. 'show 10 commits' -> 10)."""
    match = re.search(r'\b(\d+)\b', user_query)
    if match:
        num = int(match.group(1))
        return min(max(num, 1), 30) # cap between 1 and 30
    return default_limit

def query_github_api(user_query: str = ""):
    """
    Queries GitHub API using the account PAT token from .env.
    Dynamically returns Repositories, Commits, Pull Requests, Issues, or Branches
    based on the user's explicit request and requested limit.
    """
    token = os.getenv("GITHUB_TOKEN", os.getenv("GITHUB_PAT", ""))
    if not token:
        return "GitHub PAT token not found in .env. Please configure GITHUB_TOKEN or GITHUB_PAT."

    limit = _extract_limit(user_query, default_limit=5)
    q_lower = user_query.lower()

    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
        user = g.get_user()
        username = user.login

        # --- MODE 1: REPOSITORIES LIST ---
        if any(w in q_lower for w in ["repositories", "repos", "my projects", "list repo"]):
            repos = list(user.get_repos(sort="pushed", direction="desc"))[:limit]
            return {
                "type": "repositories",
                "user": username,
                "count": len(repos),
                "data": [
                    {
                        "name": r.name,
                        "full_name": r.full_name,
                        "private": r.private,
                        "language": r.language or "Unknown",
                        "stars": r.stargazers_count,
                        "pushed_at": r.pushed_at.strftime("%Y-%m-%d %H:%M:%S") if r.pushed_at else ""
                    }
                    for r in repos
                ]
            }

        # --- MODE 2: PULL REQUESTS ---
        if any(w in q_lower for w in ["pull request", "pr", "prs"]):
            prs_data = []
            recent_repos = list(user.get_repos(sort="pushed", direction="desc"))[:3]
            for r in recent_repos:
                for pr in r.get_pulls(state="all")[:limit]:
                    prs_data.append({
                        "repo": r.name,
                        "number": pr.number,
                        "title": pr.title,
                        "state": pr.state,
                        "author": pr.user.login if pr.user else "",
                        "created_at": pr.created_at.strftime("%Y-%m-%d") if pr.created_at else ""
                    })
                    if len(prs_data) >= limit:
                        break
                if len(prs_data) >= limit:
                    break
            return {"type": "pull_requests", "user": username, "data": prs_data}

        # --- MODE 3: ISSUES ---
        if any(w in q_lower for w in ["issue", "issues", "bug", "tickets"]):
            issues_data = []
            recent_repos = list(user.get_repos(sort="pushed", direction="desc"))[:3]
            for r in recent_repos:
                for issue in r.get_issues(state="all")[:limit]:
                    if not issue.pull_request: # skip PRs returned in issue endpoint
                        issues_data.append({
                            "repo": r.name,
                            "number": issue.number,
                            "title": issue.title,
                            "state": issue.state,
                            "author": issue.user.login if issue.user else "",
                            "created_at": issue.created_at.strftime("%Y-%m-%d") if issue.created_at else ""
                        })
                        if len(issues_data) >= limit:
                            break
                if len(issues_data) >= limit:
                    break
            return {"type": "issues", "user": username, "data": issues_data}

        # --- MODE 4: BRANCHES ---
        if "branch" in q_lower:
            recent_repos = list(user.get_repos(sort="pushed", direction="desc"))
            target_repo = recent_repos[0] if recent_repos else None
            if target_repo:
                branches = list(target_repo.get_branches())[:limit]
                return {
                    "type": "branches",
                    "repo": target_repo.name,
                    "data": [b.name for b in branches]
                }

        # --- MODE 5: COMMITS (DEFAULT) ---
        recent_repos = list(user.get_repos(sort="pushed", direction="desc"))
        target_repo = recent_repos[0] if recent_repos else None
        if not target_repo:
            return "No repositories found for user."

        commits = target_repo.get_commits()[:limit]
        return {
            "type": "commits",
            "user": username,
            "repo": target_repo.name,
            "limit": limit,
            "data": [
                {
                    "sha": c.sha[:7],
                    "author": c.commit.author.name if (c.commit and c.commit.author) else username,
                    "message": c.commit.message.split("\n")[0],
                    "date": c.commit.author.date.strftime("%Y-%m-%d %H:%M:%S") if (c.commit and c.commit.author) else ""
                }
                for c in commits
            ]
        }

    except Exception as e:
        return f"GitHub API Error using PAT token: {e}"

# Backward compatibility alias
def get_github_commits(repo_name=None, limit=5):
    res = query_github_api(f"commits {limit}")
    if isinstance(res, dict) and "data" in res:
        return res["data"]
    return res
