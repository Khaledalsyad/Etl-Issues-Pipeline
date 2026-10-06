import sys
import unittest
import os
from pathlib import Path

os.environ.setdefault("GITHUB_TOKEN", "test-token")
os.environ.setdefault("DATABASE_URL", "sqlite://")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from extract import GitHubExtractor
from transform import GitHubTransformer


class FakeClient:
    def __init__(self):
        self.calls = 0

    def execute_query(self, query, variables):
        self.calls += 1
        if self.calls == 1:
            return {"root": {"items": {"nodes": [{"id": "first"}], "pageInfo": {"hasNextPage": True, "endCursor": "next"}}}}
        return {"root": {"items": {"nodes": [{"id": "second"}], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}


class PipelineTransformTests(unittest.TestCase):
    def test_pagination_returns_all_pages(self):
        client = FakeClient()
        result = GitHubExtractor(client)._paginate("query", {"cursor": None}, ["root", "items"])
        self.assertEqual([{"id": "first"}, {"id": "second"}], result)
        self.assertEqual(2, client.calls)

    def test_transform_keeps_github_ids_and_audit_columns(self):
        raw_data = {
            "pipeline_run_id": "123e4567-e89b-12d3-a456-426614174000",
            "organization": {"id": "O_1", "login": "acme", "name": "Acme", "description": "org", "url": "https://github.com/acme", "createdAt": "2026-01-01T00:00:00Z", "updatedAt": "2026-01-02T00:00:00Z"},
            "repository": {"id": "R_1", "owner": {"id": "O_1"}, "name": "repo", "description": "repo", "url": "https://github.com/acme/repo", "createdAt": "2026-01-01T00:00:00Z", "updatedAt": "2026-01-02T00:00:00Z"},
            "issues": [{"id": "I_1", "number": 1, "repository_id": "R_1", "title": "Issue", "state": "OPEN", "createdAt": "2026-01-01T00:00:00Z", "updatedAt": "2026-01-02T00:00:00Z", "closedAt": None, "author": {"id": "U_1", "login": "user", "name": "User", "avatarUrl": "https://example.test/avatar"}, "labels": {"nodes": [{"id": "L_1", "name": "bug", "color": "ff0000", "description": None}]}, "assignees": {"nodes": []}}],
        }
        result = GitHubTransformer().transform(raw_data, last_run=None)
        self.assertEqual("I_1", result["issues"].iloc[0]["github_issue_id"])
        self.assertEqual("2026-01-02T00:00:00Z", result["issues"].iloc[0]["github_updated_at"])
        self.assertEqual(raw_data["pipeline_run_id"], result["organizations"].iloc[0]["pipeline_run_id"])
        self.assertEqual("org", result["organizations"].iloc[0]["description"])


if __name__ == "__main__":
    unittest.main()
