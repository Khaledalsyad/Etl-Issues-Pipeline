CREATE INDEX IF NOT EXISTS idx_issue_updated_at ON issues(github_updated_at);
CREATE INDEX IF NOT EXISTS idx_issue_repository ON issues(github_repository_id);
CREATE INDEX IF NOT EXISTS idx_issue_author ON issues(author_id);
CREATE INDEX IF NOT EXISTS idx_repository_organization ON repositories(github_organization_id);
CREATE INDEX IF NOT EXISTS idx_users_login ON users(login);
CREATE INDEX IF NOT EXISTS idx_issue_state ON issues(state);
