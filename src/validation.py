from decorators.logger import logger

REQUIRED_COLUMNS = {
    "organizations": [
        "github_organization_id",
        "login",
        "name",
        "url",
        "github_created_at",
        "github_updated_at",
    ],
    "repositories": [
        "github_repository_id",
        "github_organization_id",
        "name",
        "description",
        "url",
        "github_created_at",
        "github_updated_at",
    ],

    "users": [
        "github_user_id",
        "login",
        "name",
        "avatar_url"
    ],

    "labels": [
        "github_label_id",
        "name",
    ],

    "issues": [
        "github_issue_id",
        "issue_number",
        "github_repository_id",
        "author_id",
        "title",
        "state",
        "github_created_at",
        "github_updated_at",
        "closed_at",
    ],

    "issue_labels": [
        "github_issue_id",
        "github_label_id",
    ],

    "issue_assignees": [
        "github_issue_id",
        "github_user_id",
    ],
}


PRIMARY_KEYS = {
    "organizations": ["github_organization_id"],
    "repositories": ["github_repository_id"],
    "users": ["github_user_id"],
    "labels": ["github_label_id"],
    "issues": ["github_issue_id"],
    "issue_labels": ["github_issue_id", "github_label_id"],
    "issue_assignees": ["github_issue_id", "github_user_id"],
}

NON_NULL_COLUMNS = {
    "organizations": [
        "github_organization_id",
        "login",
        "url",
    ],

    "repositories": [
        "github_repository_id",
        "github_organization_id",
        "name",
        "url",
    ],

    "users": [
        "github_user_id",
        "login",
    ],

    "labels": [
        "github_label_id",
        "name",
    ],

    "issues": [
        "github_issue_id",
        "github_repository_id",
        "title",
        "state",
    ],

    "issue_labels": [
        "github_issue_id",
        "github_label_id",
    ],

    "issue_assignees": [
        "github_issue_id",
        "github_user_id",
    ],
}


def validate_columns(df, table_name):

    required_columns = REQUIRED_COLUMNS.get(table_name)

    if required_columns is None:
        raise ValueError(f"No required columns defined for '{table_name}'.")

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns in '{table_name}': {sorted(missing_columns)}"
        )


def validate_primary_key(df, table_name):

    primary_keys = PRIMARY_KEYS.get(table_name)

    if primary_keys is None:
        raise ValueError(f"No primary key defined for '{table_name}'.")

    for column in primary_keys:

        if column not in df.columns:
            raise ValueError(
                f"Primary key column '{column}' not found in '{table_name}'."
            )

        if df[column].isnull().any():
            raise ValueError(
                f"Primary key column '{column}' contains NULL values."
            )


def validate_duplicates(df, table_name):

    primary_keys = PRIMARY_KEYS.get(table_name)

    duplicate_rows = df[df.duplicated(subset=primary_keys)]

    if not duplicate_rows.empty:
        raise ValueError(
            f"Duplicate primary keys found in '{table_name}'."
        )


def validate_null_values(df, table_name):

    non_null_columns = NON_NULL_COLUMNS.get(table_name)

    if non_null_columns is None:
        raise ValueError(
            f"No non-null columns defined for '{table_name}'."
        )

    for column in non_null_columns:

        if df[column].isnull().any():
            raise ValueError(
                f"Column '{column}' contains NULL values in '{table_name}'."
            )

def validate_dataframe(df, table_name):

    if df.empty:
        raise ValueError(f"No data found for '{table_name}'.")

    validate_columns(df, table_name)

    validate_primary_key(df, table_name)

    validate_duplicates(df, table_name)

    validate_null_values(df, table_name)
