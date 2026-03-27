#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SUPPORTED_SCOPE = "pre-release"
REQUIRED_METADATA_KEYS = ("name", "displayName", "version", "url", "changelogUrl", "licensesUrl")
BOOTH_REQUIRED_FILES = (
    "BOOTH_PACKAGE/00_README_FIRST.txt",
    "BOOTH_PACKAGE/01_VCC_INSTALL.txt",
    "BOOTH_PACKAGE/02_QUICKSTART.txt",
    "BOOTH_PACKAGE/LICENSE",
)
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
INLINE_VERSION_RE = re.compile(r"(?<!\d)(v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)\b")
URL_RE = re.compile(r"https?://[^\s)`>]+")
README_TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def read_text(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict[str, Any] | None:
    text = read_text(path)
    if text is None:
        return None
    return json.loads(text)


def normalize_repo_url(url: str | None) -> str | None:
    if not url:
        return None
    value = url.strip()
    if not value:
        return None
    ssh_match = re.match(r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$", value)
    if ssh_match:
        return f"https://github.com/{ssh_match.group('owner')}/{ssh_match.group('repo')}"
    https_match = re.match(r"^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/#?]+)", value)
    if https_match:
        repo = https_match.group("repo")
        if repo.endswith(".git"):
            repo = repo[:-4]
        return f"https://github.com/{https_match.group('owner')}/{repo}"
    return value.removesuffix(".git").rstrip("/")


def git_remote_url(repo_root: Path) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "remote", "get-url", "origin"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return normalize_repo_url(completed.stdout.strip())


def extract_owner(guidelines_text: str) -> str | None:
    match = re.search(r"owner / アカウント名は `([^`]+)`", guidelines_text)
    return match.group(1) if match else None


def extract_release_urls(guidelines_text: str) -> tuple[str | None, str | None]:
    section_match = re.search(r"^### 正とする URL\s*$([\s\S]*?)(?=^### |\Z|^## )", guidelines_text, re.MULTILINE)
    if not section_match:
        return None, None
    urls = URL_RE.findall(section_match.group(1))
    index_url = next((url for url in urls if url.endswith("/index.json")), None)
    listing_url = next((url for url in urls if url.endswith("/") and not url.endswith("/index.json")), None)
    return index_url, listing_url


def extract_repo_index_urls(repo_index_text: str) -> dict[str, str]:
    repo_urls: dict[str, str] = {}
    for owner, repo_name in re.findall(r"^### `([^`]+)/([^`]+)`", repo_index_text, re.MULTILINE):
        repo_urls[repo_name] = f"https://github.com/{owner}/{repo_name}"
    return repo_urls


def normalize_name_tokens(value: str | None) -> set[str]:
    if not value:
        return set()
    tokens = re.findall(r"[a-z0-9]+", value.casefold())
    return {token for token in tokens if token not in {"sebanne", "tool"}}


def names_compatible(left: str | None, right: str | None) -> bool:
    if not left or not right:
        return False
    left_tokens = normalize_name_tokens(left)
    right_tokens = normalize_name_tokens(right)
    if not left_tokens or not right_tokens:
        return left.strip() == right.strip()
    return left_tokens.issubset(right_tokens) or right_tokens.issubset(left_tokens)


def extract_readme_title(text: str | None) -> str | None:
    if not text:
        return None
    match = README_TITLE_RE.search(text)
    return match.group(1).strip() if match else None


def extract_section(text: str | None, heading: str) -> str | None:
    if not text:
        return None
    pattern = re.compile(rf"^{re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def extract_tool_info_name(text: str | None) -> str | None:
    section = extract_section(text, "## ツール名")
    if not section:
        return None
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("-"):
            return stripped.lstrip("-").strip().strip("`")
    return None


def extract_latest_changelog_version(text: str | None) -> str | None:
    if not text:
        return None
    for match in re.finditer(r"^##\s+\[([^\]]+)\]", text, re.MULTILINE):
        version = match.group(1).strip()
        if SEMVER_RE.match(version):
            return version
    return None


def extract_version_mentions(text: str | None) -> list[str]:
    if not text:
        return []
    mentions: list[str] = []
    for line in text.splitlines():
        if not re.search(r"version|バージョン", line, re.IGNORECASE):
            continue
        for match in INLINE_VERSION_RE.finditer(line):
            mentions.append(match.group(1))
    deduped: list[str] = []
    for mention in mentions:
        if mention not in deduped:
            deduped.append(mention)
    return deduped


def contains_any_token(text: str | None, patterns: tuple[str, ...]) -> bool:
    if not text:
        return False
    lowered = text.casefold()
    return any(pattern.casefold() in lowered for pattern in patterns)


def extract_urls(text: str | None) -> list[str]:
    if not text:
        return []
    return URL_RE.findall(text)


def text_contains_url(text: str | None, url: str | None) -> bool:
    if not text or not url:
        return False
    return url in extract_urls(text)


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def issue(
    issue_id: str,
    severity: str,
    category: str,
    summary: str,
    files: list[str],
    current: Any,
    expected: Any,
    rule_source: str,
    why: str,
    patch_hint: dict[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "id": issue_id,
        "severity": severity,
        "category": category,
        "summary": summary,
        "files": files,
        "current": current,
        "expected": expected,
        "rule_source": rule_source,
        "why": why,
        "patch_hint": patch_hint,
    }


def canonical_field(value: Any, source: str) -> dict[str, Any]:
    return {"value": value, "source": source}


def load_knowledge(knowledge_root: Path) -> dict[str, Any]:
    guidelines_text = read_text(knowledge_root / "PUBLIC_RELEASE_GUIDELINES.md")
    shared_context_text = read_text(knowledge_root / "PROJECT_SHARED_CONTEXT.md")
    repo_index_text = read_text(knowledge_root / "REPO_INDEX.md")
    if guidelines_text is None or shared_context_text is None or repo_index_text is None:
        raise RuntimeError("Knowledge repo documents are incomplete for public-release-sync-check.")
    vcc_index_url, listing_page_url = extract_release_urls(guidelines_text)
    return {
        "guidelines_text": guidelines_text,
        "owner": extract_owner(guidelines_text),
        "repo_index_urls": extract_repo_index_urls(repo_index_text),
        "vcc_index_url": vcc_index_url,
        "listing_page_url": listing_page_url,
    }


def resolve_repo_url(repo_root: Path, knowledge: dict[str, Any]) -> tuple[str | None, str]:
    remote_url = git_remote_url(repo_root)
    if remote_url:
        return remote_url, "git_remote"
    indexed_url = knowledge["repo_index_urls"].get(repo_root.name)
    if indexed_url:
        return indexed_url, "repo_index"
    owner = knowledge.get("owner")
    if owner:
        return f"https://github.com/{owner}/{repo_root.name}", "repo_name_rule"
    return None, "unresolved"


def build_canonical_values(
    repo_root: Path,
    knowledge: dict[str, Any],
    package_json: dict[str, Any] | None,
    expected_version: str | None,
) -> dict[str, Any]:
    package_json = package_json or {}
    repo_url, repo_url_source = resolve_repo_url(repo_root, knowledge)
    return {
        "canonical_version": canonical_field(
            expected_version or package_json.get("version"),
            "expected_version" if expected_version else "package.json.version",
        ),
        "package_name": canonical_field(package_json.get("name"), "package.json.name"),
        "display_name": canonical_field(package_json.get("displayName"), "package.json.displayName"),
        "repo_url": canonical_field(repo_url, repo_url_source),
        "vcc_index_url": canonical_field(
            knowledge.get("vcc_index_url"),
            "knowledge.PUBLIC_RELEASE_GUIDELINES.vcc_index_url",
        ),
        "listing_page_url": canonical_field(
            knowledge.get("listing_page_url"),
            "knowledge.PUBLIC_RELEASE_GUIDELINES.listing_page_url",
        ),
    }


def add_version_issues(
    issues: list[dict[str, Any]],
    repo_root: Path,
    package_json: dict[str, Any] | None,
    canonical_values: dict[str, Any],
    expected_version: str | None,
    changelog_text: str | None,
    readme_text: str | None,
    tool_info_text: str | None,
    booth_texts: dict[str, str | None],
) -> None:
    package_json_path = relative_path(repo_root / "package.json", repo_root)
    canonical_version = canonical_values["canonical_version"]["value"]
    package_version = (package_json or {}).get("version")

    if not package_version:
        issues.append(
            issue(
                "version.package-json.missing",
                "blocking",
                "version",
                "package.json.version is missing.",
                [package_json_path],
                None,
                canonical_version,
                "PUBLIC_RELEASE_GUIDELINES.md#version 表記",
                "The release version baseline is undefined.",
                {"file": package_json_path, "direction": "Add a SemVer version string."},
            )
        )
    else:
        if package_version.startswith("v"):
            issues.append(
                issue(
                    "version.package-json.v-prefix",
                    "blocking",
                    "version",
                    "package.json.version uses a v-prefixed version.",
                    [package_json_path],
                    package_version,
                    canonical_version or "1.0.0",
                    "PUBLIC_RELEASE_GUIDELINES.md#version 表記",
                    "The shared release rule uses SemVer without a v prefix.",
                    {"file": package_json_path, "direction": "Remove the v prefix from version."},
                )
            )
        if not SEMVER_RE.match(package_version):
            issues.append(
                issue(
                    "version.package-json.invalid-semver",
                    "blocking",
                    "version",
                    "package.json.version is not valid SemVer.",
                    [package_json_path],
                    package_version,
                    "X.Y.Z",
                    "PUBLIC_RELEASE_GUIDELINES.md#version 表記",
                    "Release, tags, and changelog entries should share a SemVer value.",
                    {"file": package_json_path, "direction": "Replace version with a valid SemVer string."},
                )
            )
        if expected_version and package_version != expected_version:
            issues.append(
                issue(
                    "version.package-json.expected-mismatch",
                    "blocking",
                    "version",
                    "package.json.version does not match expected_version.",
                    [package_json_path],
                    package_version,
                    expected_version,
                    "PUBLIC_RELEASE_GUIDELINES.md#version 表記",
                    "The repo should converge on the requested public release version.",
                    {"file": package_json_path, "direction": "Align version with expected_version."},
                )
            )

    changelog_version = extract_latest_changelog_version(changelog_text)
    if canonical_version and changelog_version and changelog_version != canonical_version:
        issues.append(
            issue(
                "version.changelog.latest-mismatch",
                "blocking",
                "version",
                "CHANGELOG latest version does not match the canonical version.",
                ["CHANGELOG.md"],
                changelog_version,
                canonical_version,
                "PUBLIC_RELEASE_GUIDELINES.md#version 表記",
                "Changelog headings are part of the public release version set.",
                {"file": "CHANGELOG.md", "direction": "Update the latest changelog heading to the canonical version."},
            )
        )

    booth_versions: dict[str, list[str]] = {}
    for relative_booth_path, booth_text in booth_texts.items():
        matches = [match.lstrip("v") for match in extract_version_mentions(booth_text)]
        if matches:
            booth_versions[relative_booth_path] = matches
    if canonical_version:
        mismatched = {path: versions for path, versions in booth_versions.items() if any(version != canonical_version for version in versions)}
        if mismatched:
            issues.append(
                issue(
                    "version.booth-package.mismatch",
                    "blocking",
                    "version",
                    "BOOTH_PACKAGE contains a version that does not match the canonical version.",
                    sorted(mismatched.keys()),
                    mismatched,
                    canonical_version,
                    "PUBLIC_RELEASE_GUIDELINES.md#version 表記",
                    "BOOTH package handouts should not drift from the release version.",
                    {
                        "file": sorted(mismatched.keys())[0],
                        "direction": "Update BOOTH_PACKAGE version text to the canonical version.",
                    },
                )
            )

    for relative_path_value, text in (("README.md", readme_text), ("TOOL_INFO.md", tool_info_text)):
        explicit_versions = [match.lstrip("v") for match in extract_version_mentions(text)]
        if canonical_version and explicit_versions and any(version != canonical_version for version in explicit_versions):
            issues.append(
                issue(
                    f"version.{relative_path_value.lower().replace('.', '-')}.explicit-mismatch",
                    "warning",
                    "version",
                    f"{relative_path_value} contains an explicit version that differs from the canonical version.",
                    [relative_path_value],
                    explicit_versions,
                    canonical_version,
                    "PUBLIC_RELEASE_GUIDELINES.md#version 表記",
                    "Explicit version text can become stale even when repo metadata is correct.",
                    {"file": relative_path_value, "direction": "Update or remove the stale explicit version mention."},
                )
            )


def line_looks_like_vcc_target(line: str) -> bool:
    return any(token in line for token in ("VCC", "VPM", "Add Repository", "追加する URL", "追加します"))


def line_is_negated_reference(line: str) -> bool:
    lowered = line.casefold()
    return "ではありません" in line or "not" in lowered


def add_url_issues(
    issues: list[dict[str, Any]],
    canonical_values: dict[str, Any],
    readme_text: str | None,
    booth_texts: dict[str, str | None],
) -> None:
    repo_url = canonical_values["repo_url"]["value"]
    vcc_index_url = canonical_values["vcc_index_url"]["value"]
    listing_page_url = canonical_values["listing_page_url"]["value"]

    def check_text(text: str | None, relative_path_value: str) -> None:
        if not text:
            return
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line_looks_like_vcc_target(line):
                continue
            line_urls = extract_urls(line)
            if listing_page_url and listing_page_url in line_urls and not line_is_negated_reference(line):
                issues.append(
                    issue(
                        "url.vcc-target.uses-listing-page",
                        "blocking",
                        "url",
                        "A VCC target line points to the listing page instead of index.json.",
                        [relative_path_value],
                        listing_page_url,
                        vcc_index_url,
                        "PUBLIC_RELEASE_GUIDELINES.md#VPM / VCC 導線",
                        "Using the listing page as the VCC add target will mislead installation.",
                        {"file": relative_path_value, "direction": "Point VCC guidance to the index.json URL."},
                    )
                )
                return
            if repo_url and repo_url in line_urls and not line_is_negated_reference(line):
                issues.append(
                    issue(
                        "url.vcc-target.uses-repo-url",
                        "blocking",
                        "url",
                        "A VCC target line points to the repo URL instead of index.json.",
                        [relative_path_value],
                        repo_url,
                        vcc_index_url,
                        "PUBLIC_RELEASE_GUIDELINES.md#VPM / VCC 導線",
                        "Using the repo URL as the VCC add target will mislead installation.",
                        {"file": relative_path_value, "direction": "Point VCC guidance to the index.json URL."},
                    )
                )
                return

    check_text(readme_text, "README.md")
    for relative_booth_path, booth_text in booth_texts.items():
        check_text(booth_text, relative_booth_path)

    install_text = booth_texts.get("BOOTH_PACKAGE/01_VCC_INSTALL.txt")
    if vcc_index_url and install_text is not None and vcc_index_url not in install_text:
        issues.append(
            issue(
                "url.booth-vcc-install.index-missing",
                "blocking",
                "url",
                "01_VCC_INSTALL.txt does not contain the expected index.json URL.",
                ["BOOTH_PACKAGE/01_VCC_INSTALL.txt"],
                install_text.strip()[:120] if install_text.strip() else None,
                vcc_index_url,
                "PUBLIC_RELEASE_GUIDELINES.md#VPM / VCC 導線",
                "The BOOTH install guide should show the correct VCC add target.",
                {"file": "BOOTH_PACKAGE/01_VCC_INSTALL.txt", "direction": "Add the shared VCC index.json URL."},
            )
        )

    if readme_text is not None:
        if listing_page_url and not text_contains_url(readme_text, listing_page_url):
            issues.append(
                issue(
                    "url.readme.listing-page-missing",
                    "warning",
                    "url",
                    "README.md does not mention the listing page URL.",
                    ["README.md"],
                    None,
                    listing_page_url,
                    "PUBLIC_RELEASE_GUIDELINES.md#VPM / VCC 導線",
                    "README should separate the VCC add target from the listing page reference.",
                    {"file": "README.md", "direction": "Add the listing page as a reference URL, not the VCC target."},
                )
            )
        if repo_url and not text_contains_url(readme_text, repo_url):
            issues.append(
                issue(
                    "url.readme.repo-url-missing",
                    "warning",
                    "url",
                    "README.md does not mention the repo URL.",
                    ["README.md"],
                    None,
                    repo_url,
                    "PUBLIC_RELEASE_GUIDELINES.md#GitHub / owner / URL",
                    "README should keep a clear route back to the repo.",
                    {"file": "README.md", "direction": "Add the canonical repo URL where public links are listed."},
                )
            )

    booth_readme = booth_texts.get("BOOTH_PACKAGE/00_README_FIRST.txt")
    if booth_readme is not None:
        missing_links: list[str] = []
        if repo_url and not text_contains_url(booth_readme, repo_url):
            missing_links.append("repo_url")
        if listing_page_url and not text_contains_url(booth_readme, listing_page_url):
            missing_links.append("listing_page_url")
        if missing_links:
            issues.append(
                issue(
                    "url.booth-readme.public-links-incomplete",
                    "warning",
                    "url",
                    "00_README_FIRST.txt is missing one or more public reference URLs.",
                    ["BOOTH_PACKAGE/00_README_FIRST.txt"],
                    missing_links,
                    ["repo_url", "listing_page_url"],
                    "PUBLIC_RELEASE_GUIDELINES.md#BOOTH_PACKAGE の基本形",
                    "BOOTH handouts should include the repo and listing reference links.",
                    {"file": "BOOTH_PACKAGE/00_README_FIRST.txt", "direction": "Add the missing public reference URLs."},
                )
            )


def add_metadata_issues(
    issues: list[dict[str, Any]],
    canonical_values: dict[str, Any],
    package_json: dict[str, Any] | None,
    readme_text: str | None,
    tool_info_text: str | None,
) -> None:
    package_json = package_json or {}
    missing_keys = [key for key in REQUIRED_METADATA_KEYS if not package_json.get(key)]
    if missing_keys:
        issues.append(
            issue(
                "metadata.package-json.required-fields-missing",
                "blocking",
                "metadata",
                "package.json is missing one or more required public metadata fields.",
                ["package.json"],
                missing_keys,
                list(REQUIRED_METADATA_KEYS),
                "PUBLIC_RELEASE_GUIDELINES.md#package 公開の基本",
                "Public release metadata should include the shared minimum fields.",
                {"file": "package.json", "direction": "Add the missing required public metadata fields."},
            )
        )

    canonical_repo_url = canonical_values["repo_url"]["value"]
    package_url = normalize_repo_url(package_json.get("url"))
    if canonical_repo_url and package_url and package_url != normalize_repo_url(canonical_repo_url):
        issues.append(
            issue(
                "metadata.package-json.url-repo-mismatch",
                "blocking",
                "metadata",
                "package.json.url points to a different repo than the canonical repo URL.",
                ["package.json"],
                package_json.get("url"),
                canonical_repo_url,
                "PUBLIC_RELEASE_GUIDELINES.md#GitHub / owner / URL",
                "The package repo URL should match the canonical repo target.",
                {"file": "package.json", "direction": "Update url to the canonical repo URL."},
            )
        )

    changelog_url = package_json.get("changelogUrl")
    if changelog_url and "CHANGELOG.md" not in changelog_url:
        issues.append(
            issue(
                "metadata.package-json.changelog-url-invalid",
                "blocking",
                "metadata",
                "package.json.changelogUrl does not point to CHANGELOG.md.",
                ["package.json"],
                changelog_url,
                "*/CHANGELOG.md",
                "PUBLIC_RELEASE_GUIDELINES.md#GitHub / owner / URL",
                "The changelog URL should land on the repo changelog file.",
                {"file": "package.json", "direction": "Point changelogUrl to the repo CHANGELOG.md file."},
            )
        )

    licenses_url = package_json.get("licensesUrl")
    if licenses_url and "/LICENSE" not in licenses_url:
        issues.append(
            issue(
                "metadata.package-json.licenses-url-invalid",
                "blocking",
                "metadata",
                "package.json.licensesUrl does not point to LICENSE.",
                ["package.json"],
                licenses_url,
                "*/LICENSE",
                "PUBLIC_RELEASE_GUIDELINES.md#GitHub / owner / URL",
                "The licenses URL should land on the repo LICENSE file.",
                {"file": "package.json", "direction": "Point licensesUrl to the repo LICENSE file."},
            )
        )

    readme_title = extract_readme_title(readme_text)
    tool_info_name = extract_tool_info_name(tool_info_text)
    display_name = package_json.get("displayName")
    incompatible_names = [
        name for name in (readme_title, tool_info_name) if name and display_name and not names_compatible(display_name, name)
    ]
    if display_name and incompatible_names:
        files = []
        if readme_title in incompatible_names:
            files.append("README.md")
        if tool_info_name in incompatible_names:
            files.append("TOOL_INFO.md")
        issues.append(
            issue(
                "metadata.public-name.incompatible",
                "blocking",
                "metadata",
                "README.md or TOOL_INFO.md uses a public name that does not align with package.json.displayName.",
                files,
                {"displayName": display_name, "docs": incompatible_names},
                display_name,
                "PUBLIC_RELEASE_GUIDELINES.md#公開前チェック",
                "Public-facing names should describe the same tool.",
                {"file": files[0] if files else "README.md", "direction": "Align public names with package.json.displayName."},
            )
        )


def add_file_existence_issues(issues: list[dict[str, Any]], repo_root: Path) -> None:
    workflow_dir = repo_root / ".github" / "workflows"
    workflow_files = []
    if workflow_dir.exists() and workflow_dir.is_dir():
        workflow_files = [path for path in workflow_dir.iterdir() if path.is_file()]
    if not workflow_files:
        issues.append(
            issue(
                "file-existence.workflow.missing",
                "warning",
                "file-existence",
                "No workflow file was found under .github/workflows.",
                [".github/workflows"],
                [],
                [".github/workflows/*"],
                "PUBLIC_RELEASE_GUIDELINES.md#release workflow",
                "This is treated as standard release operation not yet in place, not an automatic release blocker.",
                {"file": ".github/workflows", "direction": "Add or confirm a release workflow if public release is intended."},
            )
        )

    missing_booth_files = [path for path in BOOTH_REQUIRED_FILES if not (repo_root / path).exists()]
    if missing_booth_files:
        issues.append(
            issue(
                "file-existence.booth-package.required-missing",
                "blocking",
                "file-existence",
                "BOOTH_PACKAGE is missing one or more required public handout files.",
                missing_booth_files,
                missing_booth_files,
                list(BOOTH_REQUIRED_FILES),
                "PUBLIC_RELEASE_GUIDELINES.md#BOOTH_PACKAGE の基本形",
                "The BOOTH handout set should include the shared minimum files.",
                {"file": "BOOTH_PACKAGE", "direction": "Add the missing BOOTH_PACKAGE base files."},
            )
        )


def add_docs_role_drift_issues(
    issues: list[dict[str, Any]],
    readme_text: str | None,
    tool_info_text: str | None,
    booth_texts: dict[str, str | None],
) -> None:
    if readme_text is None:
        issues.append(
            issue(
                "docs-role-drift.readme.missing",
                "warning",
                "docs-role-drift",
                "README.md is missing, so docs role checks were skipped.",
                ["README.md"],
                None,
                "README.md",
                "PUBLIC_RELEASE_GUIDELINES.md#公開前チェック",
                "README is part of the public release surface.",
                {"file": "README.md", "direction": "Add a public-facing README."},
            )
        )
        return

    if not contains_any_token(readme_text, ("VCC", "VPM")):
        issues.append(
            issue(
                "docs-role-drift.readme.vcc-guidance-missing",
                "warning",
                "docs-role-drift",
                "README.md does not mention VCC or VPM guidance.",
                ["README.md"],
                None,
                "VCC / VPM guidance",
                "PUBLIC_RELEASE_GUIDELINES.md#公開前チェック",
                "README should show the main installation route.",
                {"file": "README.md", "direction": "Add a short VCC / VPM installation section."},
            )
        )

    comparison_text = "\n".join(filter(None, [tool_info_text, *[text for text in booth_texts.values() if text]]))
    if contains_any_token(comparison_text, ("Dry Run", "確認だけ")) and not contains_any_token(readme_text, ("Dry Run", "確認だけ")):
        issues.append(
            issue(
                "docs-role-drift.readme.dry-run-guidance-missing",
                "warning",
                "docs-role-drift",
                "README.md does not mention Dry Run guidance that appears elsewhere in repo docs.",
                ["README.md"],
                None,
                "Dry Run guidance",
                "PUBLIC_RELEASE_GUIDELINES.md#公開前チェック",
                "Dry Run guidance is part of the repo's public operating story.",
                {"file": "README.md", "direction": "Mention Dry Run in the main usage flow."},
            )
        )

    if contains_any_token(comparison_text, ("非破壊",)) and not contains_any_token(readme_text, ("非破壊",)):
        issues.append(
            issue(
                "docs-role-drift.readme.non-destructive-guidance-missing",
                "warning",
                "docs-role-drift",
                "README.md does not mention non-destructive guidance that appears elsewhere in repo docs.",
                ["README.md"],
                None,
                "非破壊 guidance",
                "PUBLIC_RELEASE_GUIDELINES.md#BOOTH_PACKAGE の基本形",
                "Non-destructive guidance should stay consistent across the public docs when used.",
                {"file": "README.md", "direction": "Add a short non-destructive note to README."},
            )
        )


def derive_status(issues: list[dict[str, Any]], scope_supported: bool) -> str:
    if not scope_supported:
        return "unsupported-input"
    if any(item["severity"] == "blocking" for item in issues):
        return "blocking"
    if any(item["severity"] == "warning" for item in issues):
        return "warning"
    return "ok"


def suggest_next_action(status: str, issues: list[dict[str, Any]]) -> dict[str, Any] | None:
    if status == "unsupported-input":
        return {
            "mode": "fix-input",
            "reason": "Use check_scope='pre-release' for the initial implementation.",
        }
    if not issues:
        return {
            "mode": "none",
            "reason": "No follow-up action is needed.",
        }

    issue_ids = {item["id"] for item in issues}
    categories = {item["category"] for item in issues}

    if "file-existence.booth-package.required-missing" in issue_ids:
        reason = "BOOTH_PACKAGE is missing required handout files."
    elif "file-existence.workflow.missing" in issue_ids:
        reason = "Release workflow coverage looks incomplete."
    elif categories == {"docs-role-drift"}:
        reason = "The main issues are public-facing docs tone and role drift."
    elif categories & {"url", "metadata", "docs-role-drift"}:
        reason = "Public-facing metadata and docs need alignment."
    elif categories == {"version"}:
        reason = "The main issues are release version alignment tasks."
    else:
        reason = "A final pre-release pass is the most natural next step."

    return {
        "mode": "suggested-action",
        "reason": reason,
    }


def build_result(
    target_repo: Path,
    knowledge_root: Path,
    expected_version: str | None,
    check_scope: str,
) -> dict[str, Any]:
    knowledge = load_knowledge(knowledge_root)
    if check_scope != SUPPORTED_SCOPE:
        return {
            "status": "unsupported-input",
            "scope": {"requested": check_scope, "effective": None, "supported": False},
            "canonical_values": None,
            "issues": [],
            "suggested_next_action": suggest_next_action("unsupported-input", []),
        }

    package_json = read_json(target_repo / "package.json")
    readme_text = read_text(target_repo / "README.md")
    tool_info_text = read_text(target_repo / "TOOL_INFO.md")
    changelog_text = read_text(target_repo / "CHANGELOG.md")
    booth_texts = {path: read_text(target_repo / path) for path in BOOTH_REQUIRED_FILES if (target_repo / path).exists()}

    canonical_values = build_canonical_values(target_repo, knowledge, package_json, expected_version)
    issues: list[dict[str, Any]] = []

    add_version_issues(issues, target_repo, package_json, canonical_values, expected_version, changelog_text, readme_text, tool_info_text, booth_texts)
    add_url_issues(issues, canonical_values, readme_text, booth_texts)
    add_metadata_issues(issues, canonical_values, package_json, readme_text, tool_info_text)
    add_file_existence_issues(issues, target_repo)
    add_docs_role_drift_issues(issues, readme_text, tool_info_text, booth_texts)

    status = derive_status(issues, scope_supported=True)
    return {
        "status": status,
        "scope": {"requested": check_scope, "effective": SUPPORTED_SCOPE, "supported": True},
        "canonical_values": canonical_values,
        "issues": issues,
        "suggested_next_action": suggest_next_action(status, issues),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose pre-release public release sync mismatches.")
    parser.add_argument("target_repo", help="Path to the package repo to inspect.")
    parser.add_argument("--expected-version", dest="expected_version", help="Optional canonical version to compare against.")
    parser.add_argument("--check-scope", dest="check_scope", default=SUPPORTED_SCOPE, help="Initial implementation supports only pre-release.")
    parser.add_argument(
        "--knowledge-root",
        dest="knowledge_root",
        default=str(Path(__file__).resolve().parents[3]),
        help="Override knowledge repo root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_result(
        target_repo=Path(args.target_repo).resolve(),
        knowledge_root=Path(args.knowledge_root).resolve(),
        expected_version=args.expected_version,
        check_scope=args.check_scope,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
