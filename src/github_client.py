import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import GITHUB_TOKEN, GITHUB_GRAPHQL_URL


class GitHubGraphqlClaint:
    def __init__(self):
        self.session = requests.Session()
        retry = Retry(
            total=4,
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"POST"}),
            raise_on_status=False,
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

        self.session.headers.update({
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        })


    def execute_query(self, query: str, variables: dict = None):

        payload = {
            "query": query,
            "variables": variables or {}
        }

        response = self.session.post(
            GITHUB_GRAPHQL_URL, timeout=60, json=payload
        )
        response.raise_for_status()

        data = response.json()



        if data.get("errors"):
            raise ValueError(f"Error returned from GitHub API: {data['errors']}")

        return data.get("data")


