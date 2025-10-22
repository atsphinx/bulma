# Scripts

This directory contains utility scripts for the project.

## list_prs.py

List pull requests from GitHub, excluding auto-generated ones (created by bots).

### Usage

```bash
# List open PRs for this repository
python scripts/list_prs.py --owner atsphinx --repo bulma

# List all PRs (open and closed)
python scripts/list_prs.py --owner atsphinx --repo bulma --state all

# Include bot-generated PRs
python scripts/list_prs.py --owner atsphinx --repo bulma --include-bots

# Show detailed information
python scripts/list_prs.py --owner atsphinx --repo bulma --details

# Output in JSON format
python scripts/list_prs.py --owner atsphinx --repo bulma --json
```

### Using Environment Variables

You can also set repository information via environment variables:

```bash
export GITHUB_REPOSITORY_OWNER=atsphinx
export GITHUB_REPOSITORY=atsphinx/bulma
export GITHUB_TOKEN=your_github_token

python scripts/list_prs.py
```

### Authentication

For higher rate limits and access to private repositories, provide a GitHub token:

```bash
python scripts/list_prs.py --owner atsphinx --repo bulma --token YOUR_TOKEN
```

Or set the `GITHUB_TOKEN` environment variable.

### Bot Detection

The script automatically filters out PRs created by common bots:
- renovate[bot]
- dependabot[bot]
- github-actions[bot]
- dependabot-preview[bot]

Use `--include-bots` to show all PRs including those from bots.
