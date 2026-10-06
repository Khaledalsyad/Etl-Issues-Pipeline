class GitHubQueries:

    ORGANIZATION = """
    query GetOrganization($login: String!) {
        organization(login: $login) {
            id
            login
            name
            description
            url
            createdAt
            updatedAt
        }
    }
    """

    REPOSITORY = """
    query GetRepository(
    $login: String!,
    $repository_name: String!
    ) {
    organization(login: $login) {
        repository(name: $repository_name) {
        id
        name
        description
        url
        createdAt
        updatedAt

        owner {
            id
        }
        }
    }
    }
"""

    ISSUES = """
    query GetRepositoryIssues(
        $login: String!,
        $repository_name: String!,
        $cursor: String,
        $updated_at: DateTime
    ) {
        organization(login: $login) {
            repository(name: $repository_name) {
                id
                issues(
                    first: 100,
                    after: $cursor,
                    orderBy: {
                        field: UPDATED_AT,
                        direction: ASC
                    },
                    filterBy: {
                        since: $updated_at
                    }
                ) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }

                    nodes {
                        id
                        number
                        title
                        state
                        createdAt
                        updatedAt
                        closedAt

                        author {
                            id
                            login
                            avatarUrl
                            ... on User { name }
                        }
                    }
                }
            }
        }
    }
    """

    ISSUE_LABELS = """
    query GetIssueLabels($issue_id: ID!, $cursor: String) {
      node(id: $issue_id) {
        ... on Issue {
          labels(first: 100, after: $cursor) {
            pageInfo { hasNextPage endCursor }
            nodes { id name color description }
          }
        }
      }
    }
    """

    ISSUE_ASSIGNEES = """
    query GetIssueAssignees($issue_id: ID!, $cursor: String) {
      node(id: $issue_id) {
        ... on Issue {
          assignees(first: 100, after: $cursor) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id
              login
              avatarUrl
              ... on User { name }
            }
          }
        }
      }
    }
    """
