#!/usr/bin/env python3
"""
List pull requests excluding auto-generated ones (from bots).

This script uses the GitHub API to fetch pull requests and filters out
those created by automated bots like renovate, dependabot, etc.
"""

import argparse
import json
import os
import sys
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# Common bot users to exclude
BOT_USERS = {
    "renovate[bot]",
    "dependabot[bot]",
    "github-actions[bot]",
    "dependabot-preview[bot]",
}


def fetch_pull_requests(
    owner: str, repo: str, state: str = "all", token: str | None = None
) -> list[dict[str, Any]]:
    """
    Fetch pull requests from GitHub API.

    Args:
        owner: Repository owner
        repo: Repository name
        state: PR state (open, closed, all)
        token: GitHub API token (optional but recommended for rate limits)

    Returns:
        List of pull request data
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state={state}&per_page=100"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PR-List-Script",
    }

    if token:
        headers["Authorization"] = f"token {token}"

    try:
        request = Request(url, headers=headers)
        with urlopen(request) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        if e.code == 401:
            print("Authentication failed. Check your GitHub token.", file=sys.stderr)
        elif e.code == 404:
            print(f"Repository not found: {owner}/{repo}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def is_bot_pr(pr: dict[str, Any], bot_users: set[str] = BOT_USERS) -> bool:
    """
    Check if a PR was created by a bot.

    Args:
        pr: Pull request data
        bot_users: Set of bot usernames to check against

    Returns:
        True if PR was created by a bot
    """
    user = pr.get("user", {})
    username = user.get("login", "")
    return username in bot_users or user.get("type") == "Bot"


def format_pr(pr: dict[str, Any], show_details: bool = False) -> str:
    """
    Format a pull request for display.

    Args:
        pr: Pull request data
        show_details: Show additional details

    Returns:
        Formatted string
    """
    number = pr["number"]
    title = pr["title"]
    state = pr["state"]
    user = pr["user"]["login"]
    url = pr["html_url"]

    result = f"#{number}: {title}"
    result += f"\n  State: {state}"
    result += f"\n  Author: {user}"
    result += f"\n  URL: {url}"

    if show_details:
        created_at = pr["created_at"]
        updated_at = pr["updated_at"]
        result += f"\n  Created: {created_at}"
        result += f"\n  Updated: {updated_at}"

        if pr.get("labels"):
            labels = ", ".join(label["name"] for label in pr["labels"])
            result += f"\n  Labels: {labels}"

    return result


def main():
    parser = argparse.ArgumentParser(
        description="List pull requests excluding auto-generated ones"
    )
    parser.add_argument(
        "--owner",
        default=os.environ.get("GITHUB_REPOSITORY_OWNER", ""),
        help="Repository owner (can also use GITHUB_REPOSITORY_OWNER env var)",
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", "").split("/")[-1],
        help="Repository name (can also use GITHUB_REPOSITORY env var)",
    )
    parser.add_argument(
        "--state",
        choices=["open", "closed", "all"],
        default="open",
        help="PR state to filter (default: open)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub API token (can also use GITHUB_TOKEN env var)",
    )
    parser.add_argument(
        "--include-bots",
        action="store_true",
        help="Include bot-generated PRs in the output",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Show additional details for each PR",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )

    args = parser.parse_args()

    if not args.owner or not args.repo:
        print(
            "Error: Repository owner and name must be provided via arguments or environment variables",
            file=sys.stderr,
        )
        print(
            "Example: python list_prs.py --owner atsphinx --repo bulma",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Fetching pull requests for {args.owner}/{args.repo}...", file=sys.stderr)
    all_prs = fetch_pull_requests(args.owner, args.repo, args.state, args.token)

    # Filter out bot PRs unless explicitly included
    if not args.include_bots:
        prs = [pr for pr in all_prs if not is_bot_pr(pr)]
        bot_count = len(all_prs) - len(prs)
        print(f"Filtered out {bot_count} bot-generated PR(s)", file=sys.stderr)
    else:
        prs = all_prs

    print(f"Found {len(prs)} pull request(s)\n", file=sys.stderr)

    if args.json:
        # Output in JSON format
        output = [
            {
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "author": pr["user"]["login"],
                "url": pr["html_url"],
                "created_at": pr["created_at"],
                "updated_at": pr["updated_at"],
            }
            for pr in prs
        ]
        print(json.dumps(output, indent=2))
    else:
        # Output in human-readable format
        for pr in prs:
            print(format_pr(pr, args.details))
            print()


if __name__ == "__main__":
    main()
