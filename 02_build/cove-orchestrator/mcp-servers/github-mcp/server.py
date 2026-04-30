"""GitHub MCP Server — repo management, issues, PRs, code search."""

from __future__ import annotations

import json
import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

SERVICE_NAME = "github"

mcp = FastMCP(
    SERVICE_NAME,
    instructions=(
        "GitHub MCP server for Amplified Partners. "
        "Provides repository listing, issue management, PR tracking, "
        "and code search across the Amplified Partners organisation."
    ),
)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_ORG = os.environ.get("GITHUB_ORG", "amplified-partners")
GITHUB_API = "https://api.github.com"

_client: httpx.AsyncClient | None = None


async def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=GITHUB_API,
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=20.0,
        )
    return _client


def _handle_error(e: Exception) -> str:
    return json.dumps({"error": str(e), "suggestion": "Check GITHUB_TOKEN env var"})


# ─── Tool: List Repos ───────────────────────────────────────────────


class ListReposInput(BaseModel):
    org: str | None = Field(None, description=f"GitHub org (default: {GITHUB_ORG})")
    limit: int = Field(default=30, ge=1, le=100, description="Max repos to return")
    sort: str = Field(default="updated", description="Sort by: updated, created, pushed, full_name")


@mcp.tool(
    name=f"{SERVICE_NAME}_list_repos",
    description="List repositories in the organisation. PRIVACY: Repositories must never contain client data.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def list_repos(input: ListReposInput) -> str:
    client = await _get_client()
    org = input.org or GITHUB_ORG
    try:
        resp = await client.get(
            f"/orgs/{org}/repos",
            params={"sort": input.sort, "per_page": input.limit, "direction": "desc"},
        )
        resp.raise_for_status()
        repos = resp.json()

        results = []
        for r in repos:
            results.append({
                "name": r["name"],
                "full_name": r["full_name"],
                "description": r.get("description", ""),
                "language": r.get("language"),
                "updated_at": r.get("updated_at"),
                "open_issues": r.get("open_issues_count", 0),
                "private": r.get("private", True),
                "default_branch": r.get("default_branch", "main"),
                "url": r.get("html_url"),
            })

        return json.dumps({"count": len(results), "org": org, "repos": results}, indent=2)
    except Exception as e:
        return _handle_error(e)


# ─── Tool: List Issues ──────────────────────────────────────────────


class ListIssuesInput(BaseModel):
    repo: str = Field(description="Repository name (e.g. 'cove-orchestrator')")
    state: str = Field(default="open", description="Filter: open, closed, all")
    labels: str | None = Field(None, description="Comma-separated label filter")
    limit: int = Field(default=20, ge=1, le=100, description="Max issues to return")


@mcp.tool(
    name=f"{SERVICE_NAME}_list_issues",
    description="List issues in a repository. PRIVACY: If you detect client PII in an issue, flag it for redaction immediately.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def list_issues(input: ListIssuesInput) -> str:
    client = await _get_client()
    try:
        params: dict[str, Any] = {
            "state": input.state,
            "per_page": input.limit,
            "sort": "updated",
            "direction": "desc",
        }
        if input.labels:
            params["labels"] = input.labels

        resp = await client.get(f"/repos/{GITHUB_ORG}/{input.repo}/issues", params=params)
        resp.raise_for_status()
        issues = resp.json()

        results = []
        for i in issues:
            if i.get("pull_request"):
                continue  # Skip PRs in issue listing
            results.append({
                "number": i["number"],
                "title": i["title"],
                "state": i["state"],
                "author": i.get("user", {}).get("login", ""),
                "labels": [l["name"] for l in i.get("labels", [])],
                "created_at": i.get("created_at"),
                "updated_at": i.get("updated_at"),
                "comments": i.get("comments", 0),
                "url": i.get("html_url"),
            })

        return json.dumps({"count": len(results), "repo": input.repo, "issues": results}, indent=2)
    except Exception as e:
        return _handle_error(e)


# ─── Tool: Create Issue ─────────────────────────────────────────────


class CreateIssueInput(BaseModel):
    repo: str = Field(description="Repository name")
    title: str = Field(description="Issue title")
    body: str = Field(default="", description="Issue body (markdown)")
    labels: list[str] = Field(default_factory=list, description="Labels to apply")
    assignees: list[str] = Field(default_factory=list, description="GitHub usernames to assign")


@mcp.tool(
    name=f"{SERVICE_NAME}_create_issue",
    description=(
        "Create a new issue. "
        "LAYER 0 RULE: Apply Radical Attribution by citing sources. "
        "PRIVACY RULE: Never include client names, PII, or un-tokenized sensitive data in the title or body."
    ),
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def create_issue(input: CreateIssueInput) -> str:
    client = await _get_client()
    try:
        payload: dict[str, Any] = {"title": input.title, "body": input.body}
        if input.labels:
            payload["labels"] = input.labels
        if input.assignees:
            payload["assignees"] = input.assignees

        resp = await client.post(f"/repos/{GITHUB_ORG}/{input.repo}/issues", json=payload)
        resp.raise_for_status()
        issue = resp.json()

        return json.dumps({
            "number": issue["number"],
            "title": issue["title"],
            "url": issue["html_url"],
            "state": issue["state"],
        }, indent=2)
    except Exception as e:
        return _handle_error(e)


# ─── Tool: List PRs ─────────────────────────────────────────────────


class ListPRsInput(BaseModel):
    repo: str = Field(description="Repository name")
    state: str = Field(default="open", description="Filter: open, closed, all")
    limit: int = Field(default=20, ge=1, le=100, description="Max PRs to return")


@mcp.tool(
    name=f"{SERVICE_NAME}_list_prs",
    description="List pull requests. Ensure all PRs link back to Linear issues for Radical Transparency.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def list_prs(input: ListPRsInput) -> str:
    client = await _get_client()
    try:
        resp = await client.get(
            f"/repos/{GITHUB_ORG}/{input.repo}/pulls",
            params={"state": input.state, "per_page": input.limit, "sort": "updated", "direction": "desc"},
        )
        resp.raise_for_status()
        prs = resp.json()

        results = []
        for pr in prs:
            results.append({
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "author": pr.get("user", {}).get("login", ""),
                "branch": pr.get("head", {}).get("ref", ""),
                "base": pr.get("base", {}).get("ref", ""),
                "draft": pr.get("draft", False),
                "mergeable": pr.get("mergeable"),
                "created_at": pr.get("created_at"),
                "updated_at": pr.get("updated_at"),
                "url": pr.get("html_url"),
            })

        return json.dumps({"count": len(results), "repo": input.repo, "pull_requests": results}, indent=2)
    except Exception as e:
        return _handle_error(e)


# ─── Tool: Search Code ──────────────────────────────────────────────


class SearchCodeInput(BaseModel):
    query: str = Field(description="Code search query (GitHub search syntax)")
    repo: str | None = Field(None, description="Limit to specific repo")
    limit: int = Field(default=20, ge=1, le=50, description="Max results")


@mcp.tool(
    name=f"{SERVICE_NAME}_search_code",
    description="Search code across repositories. Use this to verify facts and gather context (Radical Truth).",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def search_code(input: SearchCodeInput) -> str:
    client = await _get_client()
    try:
        q = input.query
        if input.repo:
            q += f" repo:{GITHUB_ORG}/{input.repo}"
        else:
            q += f" org:{GITHUB_ORG}"

        resp = await client.get(
            "/search/code",
            params={"q": q, "per_page": input.limit},
        )
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("items", []):
            results.append({
                "name": item.get("name"),
                "path": item.get("path"),
                "repo": item.get("repository", {}).get("full_name"),
                "url": item.get("html_url"),
                "score": item.get("score"),
            })

        return json.dumps({
            "total_count": data.get("total_count", 0),
            "returned": len(results),
            "results": results,
        }, indent=2)
    except Exception as e:
        return _handle_error(e)


# ─── Entry Point ────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
