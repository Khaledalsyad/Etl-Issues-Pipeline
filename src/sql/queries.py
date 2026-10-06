from sqlalchemy import text


INSERT_ORGANIZATIONS = text("""
INSERT INTO organizations (
    github_organization_id,
    login,
    name,
    description,
    url,
    github_created_at,
    github_updated_at,
    record_source,
    extracted_at,
    loaded_at,
    pipeline_run_id
)
VALUES (
    :github_organization_id,
    :login,
    :name,
    :description,
    :url,
    :github_created_at,
    :github_updated_at,
    :record_source,
    :extracted_at,
    :loaded_at,
    :pipeline_run_id
)

ON CONFLICT (github_organization_id)
DO UPDATE SET
    login = EXCLUDED.login,
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    url = EXCLUDED.url,
    github_created_at = EXCLUDED.github_created_at,
    github_updated_at = EXCLUDED.github_updated_at,
    record_source = EXCLUDED.record_source,
    extracted_at = EXCLUDED.extracted_at,
    loaded_at = EXCLUDED.loaded_at,
    pipeline_run_id = EXCLUDED.pipeline_run_id
""")


INSERT_REPOSITORIES = text("""
INSERT INTO repositories (
    github_repository_id,
    github_organization_id,
    name,
    description,
    url,
    github_created_at,
    github_updated_at,
    record_source,
    extracted_at,
    loaded_at,
    pipeline_run_id
)
VALUES (
    :github_repository_id,
    :github_organization_id,
    :name,
    :description,
    :url,
    :github_created_at,
    :github_updated_at,
    :record_source,
    :extracted_at,
    :loaded_at,
    :pipeline_run_id
)

ON CONFLICT (github_repository_id)
DO UPDATE SET
    github_organization_id = EXCLUDED.github_organization_id,
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    url = EXCLUDED.url,
    github_created_at = EXCLUDED.github_created_at,
    github_updated_at = EXCLUDED.github_updated_at,
    record_source = EXCLUDED.record_source,
    extracted_at = EXCLUDED.extracted_at,
    loaded_at = EXCLUDED.loaded_at,
    pipeline_run_id = EXCLUDED.pipeline_run_id
""")


INSERT_USERS = text("""
INSERT INTO users (
    github_user_id,
    login,
    name,
    avatar_url,
    record_source,
    extracted_at,
    loaded_at,
    pipeline_run_id
)
VALUES (
    :github_user_id,
    :login,
    :name,
    :avatar_url,
    :record_source,
    :extracted_at,
    :loaded_at,
    :pipeline_run_id
)

ON CONFLICT (github_user_id)
DO UPDATE SET
    login = EXCLUDED.login,
    name = EXCLUDED.name,
    avatar_url = EXCLUDED.avatar_url,
    record_source = EXCLUDED.record_source,
    extracted_at = EXCLUDED.extracted_at,
    loaded_at = EXCLUDED.loaded_at,
    pipeline_run_id = EXCLUDED.pipeline_run_id
""")


INSERT_LABELS = text("""
INSERT INTO labels (
    github_label_id,
    name,
    color,
    description,
    record_source,
    extracted_at,
    loaded_at,
    pipeline_run_id
)
VALUES (
    :github_label_id,
    :name,
    :color,
    :description,
    :record_source,
    :extracted_at,
    :loaded_at,
    :pipeline_run_id
)

ON CONFLICT (github_label_id)
DO UPDATE SET
    name = EXCLUDED.name,
    color = EXCLUDED.color,
    description = EXCLUDED.description,
    record_source = EXCLUDED.record_source,
    extracted_at = EXCLUDED.extracted_at,
    loaded_at = EXCLUDED.loaded_at,
    pipeline_run_id = EXCLUDED.pipeline_run_id
""")


INSERT_ISSUES = text("""
INSERT INTO issues (
    github_issue_id,
    issue_number,
    github_repository_id,
    author_id,
    title,
    state,
    github_created_at,
    github_updated_at,
    closed_at,
    record_source,
    extracted_at,
    loaded_at,
    pipeline_run_id
)

VALUES (
    :github_issue_id,
    :issue_number,
    :github_repository_id,
    :author_id,
    :title,
    :state,
    :github_created_at,
    :github_updated_at,
    :closed_at,
    :record_source,
    :extracted_at,
    :loaded_at,
    :pipeline_run_id
)

ON CONFLICT (github_issue_id)
DO UPDATE SET
    github_repository_id = EXCLUDED.github_repository_id,
    author_id = EXCLUDED.author_id,
    title = EXCLUDED.title,
    state = EXCLUDED.state,
    github_created_at = EXCLUDED.github_created_at,
    github_updated_at = EXCLUDED.github_updated_at,
    issue_number = EXCLUDED.issue_number,
    closed_at = EXCLUDED.closed_at,
    record_source = EXCLUDED.record_source,
    extracted_at = EXCLUDED.extracted_at,
    loaded_at = EXCLUDED.loaded_at,
    pipeline_run_id = EXCLUDED.pipeline_run_id
""")


INSERT_ISSUE_LABELS = text("""
INSERT INTO issue_labels (
    github_issue_id,
    github_label_id
)
VALUES (
    :github_issue_id,
    :github_label_id
)

ON CONFLICT (github_issue_id, github_label_id)
DO NOTHING;
""")


INSERT_ISSUE_ASSIGNEES = text("""
INSERT INTO issue_assignees (
    github_issue_id,
    github_user_id
)
VALUES (
    :github_issue_id,
    :github_user_id
)

ON CONFLICT (github_issue_id, github_user_id)
DO NOTHING;
""")


# this part of code to make the load prosec is easy 
QUERIES = {
    "organizations": INSERT_ORGANIZATIONS,
    "repositories": INSERT_REPOSITORIES,
    "users": INSERT_USERS,
    "labels": INSERT_LABELS,
    "issues": INSERT_ISSUES,
    "issue_labels": INSERT_ISSUE_LABELS,
    "issue_assignees": INSERT_ISSUE_ASSIGNEES,
}
