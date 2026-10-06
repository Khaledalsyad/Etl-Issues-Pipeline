import pandas as pd
from datetime import datetime, timezone
from decorators.logger import logger

class GitHubTransformer:
    def __init__(self):
        pass
    

    # =====================================================
    # Helpers Finctions
    # =====================================================

    def _extract_organization(self, organization):
        if organization is None:
            return None

        return {
            "github_organization_id": organization.get("id"),
            "login": organization.get("login"),
            "name": organization.get("name"),
            "description": organization.get("description"),
            "url": organization.get("url"),
            "github_created_at": organization.get("createdAt"),
            "github_updated_at": organization.get("updatedAt"),
            "record_source": "GitHub",
        }


    def _extract_repository(self, repository):

        if repository is None:
            return None

        return {
            "github_repository_id": repository.get("id"),
            "github_organization_id": repository.get("owner", {}).get("id"),
            "name": repository.get("name"),
            "description": repository.get("description"),
            "url": repository.get("url"),
            "github_created_at": repository.get("createdAt"),
            "github_updated_at": repository.get("updatedAt"),
            "record_source": "GitHub",
        }


    def _extract_label(self, label):
        if label is None:
            return None

        return {
            "github_label_id": label.get("id"),
            "name": label.get("name"),
            "color": label.get("color"),
            "description": label.get("description"),
            "record_source": "GitHub",
        }


    def _extract_author(self, issue):
        author = issue.get("author")

        if author is None:
            return None

        return {
            "github_user_id": author.get("id"),
            "login": author.get("login"),
            "name": author.get("name"),
            "avatar_url": author.get("avatarUrl"),
            "record_source": "GitHub",
        }
    
    def _extract_issue(self, issue):

        if issue is None:
            return None

        return {
            "github_issue_id": issue.get("id"),
            "issue_number": issue.get("number"),
            "github_repository_id": issue.get("repository_id"),
            "author_id": (issue.get("author")or {}).get("id"),
            "title": issue.get("title"),
            "state": issue.get("state"),
            "github_created_at": issue.get("createdAt"),
            "github_updated_at": issue.get("updatedAt"),
            "closed_at": issue.get("closedAt"),
            "record_source": "GitHub",
        }

    def _extract_assignees(self, issue):
        assignees = issue.get("assignees", []).get("nodes", {})

        if assignees is None:
            return []

        users = []

        for assignee in assignees:
            users.append(
                {
                    "github_user_id": assignee.get("id"),
                    "login": assignee.get("login"),
                    "name": assignee.get("name"),
                    "avatar_url": assignee.get("avatarUrl"),
                    "record_source": "GitHub"
                }
            )

        return users
    
    
    def _extract_issue_labels(self, issue):

        if issue is None:
            return []

        labels = issue.get("labels", {}).get("nodes", [])

        issue_labels = []

        for label in labels:

            issue_labels.append(
                {
                    "github_issue_id": issue.get("id"),
                    "github_label_id": label.get("id"),
                }
            )

        return issue_labels


    def _extract_issue_assignees(
    self,
    issue,
    ):

        if issue is None:
            return []

        assignees = issue.get("assignees", {}).get("nodes", [])

        if not assignees:
            return []

        issue_assignees = []

        for assignee in assignees:

            issue_assignees.append(
                {
                    "github_issue_id": issue.get("id"),
                    "github_user_id": assignee.get("id"),
                }
            )

        return issue_assignees

    def _add_audit_columns(self, df, pipeline_run_id):

        runtime = datetime.now(timezone.utc)

        df["extracted_at"] = runtime
        df["loaded_at"] = runtime
        df["pipeline_run_id"] = str(pipeline_run_id)

        return df


    # =====================================================
    # Transformations
    # =====================================================

    def transform_organization(self, organization, pipeline_run_id):

        organization = self._extract_organization(organization)

        if organization is None:
            return pd.DataFrame()

        df = pd.DataFrame([organization])

        if df.empty:
            return None

        df = df.drop_duplicates(subset=["github_organization_id"])

        df = self._add_audit_columns(df, pipeline_run_id)

        logger.info(
        "Organization rows: %s",
        len(df),
        )

        return df

    def transform_repository(self, repository, pipeline_run_id):

        repo = self._extract_repository(repository)

        if repo is None:
            return None

        df = pd.DataFrame([repo])

        if df.empty:
            return None

        df = df.drop_duplicates(subset=["github_repository_id"])

        df = self._add_audit_columns(df, pipeline_run_id)

        logger.info("Repository rows: %s", len(df))

        return df

    def transform_labels(self, issues, pipeline_run_id):

        labels_data = []

        for issue in issues:

            labels = issue.get("labels", {}).get("nodes", [])

            for label in labels:

                lab = self._extract_label(label)

                if lab is None:
                    continue

                labels_data.append(lab)

        df = pd.DataFrame(labels_data)

        if df.empty:
            return df

        df = df.drop_duplicates(subset=["github_label_id"])

        df = self._add_audit_columns(df, pipeline_run_id)

        logger.info(
            "Labels rows: %s",
            len(df),
        )

        return df

    def transform_users(self, issues, pipeline_run_id):

        users_data = []

        for issue in issues:

            author = self._extract_author(issue)

            if author is not None:
                users_data.append(author)

            assignees = self._extract_assignees(issue)

            users_data.extend(assignees)

        df = pd.DataFrame(users_data)

        if df.empty:
            return None
            
        df = df.drop_duplicates(subset=["github_user_id"])

        df = self._add_audit_columns(df, pipeline_run_id)
        logger.info("users rows %s", len(df))

        return df

    def transform_issues(self, issues, pipeline_run_id):
        issues_data = []
        for issue in issues:
            issu = self._extract_issue(issue)

            if issu is None:
                continue

            issues_data.append(issu)

        df = pd.DataFrame(issues_data)

        if df.empty:
            return None  
        df = df.drop_duplicates(subset=["github_issue_id"])

        df = self._add_audit_columns(df, pipeline_run_id) 

        logger.info("the count issues is retrun is %s", len(df))

        return df
    
    def transform_issue_labels(
    self,
    issues,
    ):

        logger.info("Transforming issue labels...")

        issue_labels_data = []

        for issue in issues:

            issue_labels = self._extract_issue_labels(issue)

            issue_labels_data.extend(issue_labels)

        df = pd.DataFrame(issue_labels_data)

        if df.empty:
            return df

        df = df.drop_duplicates()

        logger.info(
            "Issue Labels rows: %s",
            len(df),
        )

        return df

    def transform_issue_assignees(
    self,
    issues,
    ):

        logger.info("Transforming issue assignees...")

        issue_assignees_data = []

        for issue in issues:

            assignees = self._extract_issue_assignees(issue)

            issue_assignees_data.extend(assignees)

        df = pd.DataFrame(issue_assignees_data)

        if df.empty:
            return df

        df = df.drop_duplicates()

        logger.info(
            "Issue Assignees rows: %s",
            len(df),
        )

        return df
    
    ############################
    ## metadata updated_at column
    ############################
    def get_max_updated_at(self, issues):

        if not issues:
            return None

        updated_dates = [
            issue.get("updatedAt")
            for issue in issues
            if issue.get("updatedAt") is not None
        ]

        if not updated_dates:
            return None

        return max(updated_dates)



    def incremental_filter(
        self,
        df,
        last_run,
    ):

        if df is None or last_run is None:
            return df

        comparable_df = df.copy()
        comparable_df["github_updated_at"] = pd.to_datetime(
            comparable_df["github_updated_at"], utc=True
        )
        last_run_at = pd.to_datetime(last_run, utc=True)
        filtered_df = comparable_df[
            comparable_df["github_updated_at"] > last_run_at
        ]

        logger.info(
            "Rows after incremental filter: %s",
            len(filtered_df),
        )

        return filtered_df


    def transform(
    self,
    raw_data: dict,
    last_run,
    ) -> dict:

        pipeline_run_id = raw_data["pipeline_run_id"]

        organization_df = self.transform_organization(
            raw_data["organization"], pipeline_run_id
        )

        repository_df = self.transform_repository(
            raw_data["repository"], pipeline_run_id
        )

        users_df = self.transform_users(
            raw_data["issues"], pipeline_run_id
        )

        issues_df = self.transform_issues(
            raw_data["issues"], pipeline_run_id
        )

        issues_df = self.incremental_filter(
            issues_df,
            last_run,
        )

        labels_df = self.transform_labels(
            raw_data["issues"], pipeline_run_id
        )

        issue_labels_df = self.transform_issue_labels(
            raw_data["issues"]
        )


        issue_assignees_df = self.transform_issue_assignees(
            raw_data["issues"]
        )


        return {
            "organizations": organization_df,
            "repositories": repository_df,
            "users": users_df,
            "issues": issues_df,
            "labels": labels_df,
            "issue_labels": issue_labels_df,
            "issue_assignees": issue_assignees_df,
        }
