from typing import Any, Optional
from github_client import GitHubGraphqlClaint
from graphql_queries import GitHubQueries
from decorators.logger import logger

class GitHubExtractor:
    def __init__(self, client: GitHubGraphqlClaint):
        self.client = client

    def _paginate(
        self,
        query: str,
        variables: dict[str, Any],
        data_path: list[str],
        post_process=None
    ):
        all_nodes = []
        while True:
            # Execute one page.
            data = self.client.execute_query(
                query=query,
                variables=variables
            )

            section = data

            for key in data_path:
                if key not in section:
                    raise RuntimeError(f"the {key} Not Found In Data Return")
                section = section[key]

            nodes = section.get("nodes", [])

            if post_process is not None:
                nodes = post_process(data, nodes)

            all_nodes.extend(nodes)

            page_info = section.get("pageInfo", {})

            if not page_info.get("hasNextPage", False):
                break
            cursor = page_info.get("endCursor")

            if cursor is None:
                break
            variables["cursor"] = cursor

        return all_nodes
        
    # extract the main entity  
    def extract_organization(self, login_organization:str):
        logger.info("start extratc organization")
        query = GitHubQueries.ORGANIZATION

        variables={
            "login": login_organization
        }

        data = self.client.execute_query(query, variables)

        organization = data.get("organization")

        if organization is None:
            raise RuntimeError(f"No {organization} Is Return From Data")

        return organization

    def extract_repository(
    self,
    login_organization: str,
    repository_name: str,
):

        logger.info("start extract repositories")

        query = GitHubQueries.REPOSITORY

        variables={
            "login": login_organization,
            "repository_name": repository_name
        } 

        data  = self.client.execute_query(query, variables)

        
        if data is None:
            raise RuntimeError(f"No {data} is return from github")
        
        return data["organization"]["repository"]

    def extract_issues(self, login_organization: str, repository_name: str, updated_at: Optional[str]):
        query = GitHubQueries.ISSUES

        variables={
            "login": login_organization,
            "repository_name": repository_name,
            "cursor": None,
            "updated_at": updated_at
        }

        return self._paginate(
            query=query,
            variables=variables,
            data_path=[
                "organization",
                "repository",
                "issues"
            ]
        )

    def _extract_issue_connection(self, issue_id: str, query: str, connection: str):
        return self._paginate(
            query=query,
            variables={"issue_id": issue_id, "cursor": None},
            data_path=["node", connection],
        )

    def extract_issue_details(self, issues: list[dict]):
        """Fetch every label and assignee page to avoid silently truncating relations."""
        for issue in issues:
            issue_id = issue["id"]
            issue["labels"] = {"nodes": self._extract_issue_connection(
                issue_id, GitHubQueries.ISSUE_LABELS, "labels"
            )}
            issue["assignees"] = {"nodes": self._extract_issue_connection(
                issue_id, GitHubQueries.ISSUE_ASSIGNEES, "assignees"
            )}


    
    # extract raw data
    def extract(self, login_organization, repository_name, updated_at):
        organization = self.extract_organization(login_organization)
        repository = self.extract_repository(login_organization, repository_name)

        repository_id = repository["id"]

        issues = self.extract_issues(
            login_organization,
            repository_name,
            updated_at,
        )

        self.extract_issue_details(issues)

        for issue in issues:
            issue["repository_id"] = repository_id

        return {
            "organization": organization,
            "repository": repository,
            "issues": issues,
        }


