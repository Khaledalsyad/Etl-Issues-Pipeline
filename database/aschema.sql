-- PostgreSQL schema. GitHub GraphQL node IDs are opaque strings, not integers.
CREATE TABLE IF NOT EXISTS organizations (
    github_organization_id TEXT PRIMARY KEY,
    login VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    description TEXT,
    url TEXT NOT NULL,
    github_created_at TIMESTAMPTZ,
    github_updated_at TIMESTAMPTZ,
    record_source VARCHAR(50) NOT NULL,
    pipeline_run_id UUID NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS repositories (
    github_repository_id TEXT PRIMARY KEY,
    github_organization_id TEXT NOT NULL REFERENCES organizations(github_organization_id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    url TEXT NOT NULL,
    github_created_at TIMESTAMPTZ,
    github_updated_at TIMESTAMPTZ,
    record_source VARCHAR(50) NOT NULL,
    pipeline_run_id UUID NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    github_user_id TEXT PRIMARY KEY,
    login VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    record_source VARCHAR(50) NOT NULL,
    pipeline_run_id UUID NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS labels (
    github_label_id TEXT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    color VARCHAR(20),
    description TEXT,
    record_source VARCHAR(50) NOT NULL,
    pipeline_run_id UUID NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS issues (
    github_issue_id TEXT PRIMARY KEY,
    issue_number INTEGER NOT NULL,
    github_repository_id TEXT NOT NULL REFERENCES repositories(github_repository_id),
    author_id TEXT REFERENCES users(github_user_id),
    title TEXT NOT NULL,
    state VARCHAR(20) NOT NULL,
    github_created_at TIMESTAMPTZ NOT NULL,
    github_updated_at TIMESTAMPTZ NOT NULL,
    closed_at TIMESTAMPTZ,
    record_source VARCHAR(50) NOT NULL,
    pipeline_run_id UUID NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL,
    UNIQUE (github_repository_id, issue_number)
);

CREATE TABLE IF NOT EXISTS issue_labels (
    github_issue_id TEXT NOT NULL REFERENCES issues(github_issue_id) ON DELETE CASCADE,
    github_label_id TEXT NOT NULL REFERENCES labels(github_label_id),
    PRIMARY KEY (github_issue_id, github_label_id)
);

CREATE TABLE IF NOT EXISTS issue_assignees (
    github_issue_id TEXT NOT NULL REFERENCES issues(github_issue_id) ON DELETE CASCADE,
    github_user_id TEXT NOT NULL REFERENCES users(github_user_id),
    PRIMARY KEY (github_issue_id, github_user_id)
);

CREATE TABLE IF NOT EXISTS metadata_pipeline (
    pipeline_name VARCHAR(255) PRIMARY KEY,
    last_run TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO metadata_pipeline (pipeline_name, last_run)
VALUES ('issue_pipeline', NULL)
ON CONFLICT (pipeline_name) DO NOTHING;
