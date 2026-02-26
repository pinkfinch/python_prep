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
import requests
import logging
from datetime import datetime
import pandas as pd
import time

class GitData:
    def __init__(self, stars=0, issues=0, language="java", last_update_date=None, fork_count=0):
        self.stars = stars
        self.issues = issues
        self.language = language
        self.last_update_date = last_update_date
        self.fork_count = fork_count

class GitRepository:

    def __init__(self):
        self.repo_list = {}
        self.logger = logging.getLogger(__name__)

    def fetch_repos(self, repo_list, initial_delay=1):
        self.repo_list = repo_list
        git_list = {}
        delay = initial_delay
        retries = 3
        for repo in self.repo_list:
            attempt = 1
            while attempt < retries:
                try :
                    response = requests.get("https://api.github.com/search/repositories?q="+repo, timeout=5)
                    if response.status_code == 404:
                        self.logger.error(f"{repo} returned 404")
                        break

                    if response.status_code == 200:
                        json_resp = response.json()
                        items = json_resp.get('items', [])
                        if items:
                            repo_data = items[0]
                            self.logger.debug(repo_data)
                            stars = repo_data["stargazers_count"]
                            issues = repo_data["open_issues_count"]
                            primary_language = repo_data["language"]
                            last_update_date = datetime.strptime(repo_data["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
                            fork_count = repo_data["forks_count"]
                            git_list[repo] = {
                                'stars': stars,
                                'issues': issues,
                                'primary_language': primary_language,
                                'last_update_date': last_update_date,
                                'fork_count': fork_count
                            }
                        break
                    elif response.status_code == 429 or response.status_code == 403:
                        retry_after = response.headers.get('Retry-After')
                        if retry_after:
                            wait_time = int(retry_after)
                            print(f"Rate limit hit. Retrying after {wait_time} seconds.")
                            time.sleep(wait_time)
                            attempt += 1
                        else:
                            print(f"Rate limit hit. Retrying with exponential backoff in {delay} seconds.")
                            time.sleep(delay)
                            delay *= 2  # Exponential increase
                        continue
                    break
                except requests.exceptions.ReadTimeout:
                    self.logger.error("Read timeout", exc_info=True)
                    attempt += 1
                except requests.exceptions.ConnectionError:
                    self.logger.error("connection timeout", exc_info=True)
                    attempt += 1

        return git_list

    def process_git_list(self, git_response):
        df = pd.DataFrame.from_dict(git_response, orient="index")
        return df


g = GitRepository()
repo_list = ["sindresorhus/awesome", "thealgorithms/java", "MunGell/awesome-for-beginners"]
git_resp = g.fetch_repos(repo_list)
dataframe = g.process_git_list(git_resp)
print(dataframe.to_string())