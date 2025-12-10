"""
Use GitHub API to analyze repository statistics.
API: https://api.github.com/repos/{owner}/{repo}

Task: Given a list of repositories, fetch and compare:
1. Number of stars
2. Number of open issues
3. Primary language
4. Last update date
5. Fork count

Handle:
- API rate limits (GitHub allows 60 requests/hour without auth)
- Repositories that don't exist (404 errors)
- Network failures

No API key needed for public repos.
"""