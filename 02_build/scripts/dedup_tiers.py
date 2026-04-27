#!/usr/bin/env python3
"""
dedup_tiers.py — Tier 1 (SHA-256 exact) + Tier 2 (ssdeep fuzzy) dedup analysis.

Read-only analysis across corpus-raw/vault and clean-build directories.
Produces JSON machine-readable outputs and a Markdown statistics report.

Signed-by: Devon (Devin) | 2026-04-27 | session 7cd95caf339c46a2896fbf6ffbda02be
"""

import argparse
import hashlib
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

try:
    import ppdeep as ssdeep_lib
except ImportError:
    print("ERROR: ppdeep not installed. Run: pip install ppdeep", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_file(path: str) -> str | None:
    """Return hex SHA-256 of file contents, or None on read error."""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return None


def fuzzy_hash_file(path: str) -> str | None:
    """Return ssdeep/ppdeep fuzzy hash string, or None on error."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        return ssdeep_lib.hash(data)
    except (OSError, PermissionError, Exception):
        return None


def file_extension(path: str) -> str:
    """Normalised lowercase extension including the dot, or '' if none."""
    _, ext = os.path.splitext(path)
    return ext.lower()


def first_n_chars(path: str, n: int = 200) -> str:
    """Return first n characters of a file for preview, replacing non-printable."""
    try:
        with open(path, "r", errors="replace") as f:
            return f.read(n)
    except (OSError, PermissionError):
        return "<unreadable>"


def human_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def dir_label(path: str, vault_path: str, clean_build_path: str) -> str:
    """Return a short label for where a file lives."""
    vp = os.path.abspath(vault_path)
    cp = os.path.abspath(clean_build_path)
    ap = os.path.abspath(path)
    if ap.startswith(vp):
        return "corpus-raw/vault" + ap[len(vp):]
    if ap.startswith(cp):
        return "clean-build" + ap[len(cp):]
    return ap


def choose_keeper(paths: list[str], vault_path: str, clean_build_path: str) -> str:
    """Pick the file in the most specific/categorised location to keep.

    Priority: clean-build/01_truth > clean-build/02_build > clean-build/03_shadow
    > clean-build/90_archive > corpus-raw/vault (non-inbox) > corpus-raw/vault/_inbox*
    """
    cp = os.path.abspath(clean_build_path)
    vp = os.path.abspath(vault_path)
    priority_prefixes = [
        os.path.join(cp, "01_truth"),
        os.path.join(cp, "02_build"),
        os.path.join(cp, "03_shadow"),
        os.path.join(cp, "90_archive"),
    ]

    def score(p: str) -> int:
        ap = os.path.abspath(p)
        for i, prefix in enumerate(priority_prefixes):
            if ap.startswith(prefix):
                return i
        # corpus-raw _inbox ranks lowest
        if ap.startswith(vp):
            rel = ap[len(vp):]
            if "/_inbox" in rel:
                return 100
            return 50
        return 75

    return min(paths, key=score)


# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------

def scan_directories(vault_path: str, clean_build_path: str) -> list[dict]:
    """Walk target dirs and collect file metadata."""
    targets = [vault_path]
    for sub in ("01_truth", "02_build", "03_shadow", "90_archive"):
        d = os.path.join(clean_build_path, sub)
        if os.path.isdir(d):
            targets.append(d)

    files = []
    for root_dir in targets:
        for dirpath, _, filenames in os.walk(root_dir):
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                if os.path.isfile(fpath):
                    try:
                        size = os.path.getsize(fpath)
                    except OSError:
                        size = 0
                    files.append({
                        "path": fpath,
                        "size": size,
                        "ext": file_extension(fpath),
                    })
    return files


# ---------------------------------------------------------------------------
# Tier 1 — SHA-256 exact dedup
# ---------------------------------------------------------------------------

def tier1_exact(files: list[dict], vault_path: str, clean_build_path: str) -> tuple[list[dict], list[dict]]:
    """Return (duplicate_sets, unique_files).

    duplicate_sets: list of dicts with hash, files, kept_path, bytes_wasted.
    unique_files: files that have no exact duplicate.
    """
    hash_map: dict[str, list[dict]] = defaultdict(list)
    skipped = 0

    for i, f in enumerate(files):
        if (i + 1) % 500 == 0:
            print(f"  Tier 1 hashing: {i + 1}/{len(files)}", file=sys.stderr)
        h = sha256_file(f["path"])
        if h is None:
            skipped += 1
            continue
        f["sha256"] = h
        hash_map[h].append(f)

    if skipped:
        print(f"  Tier 1: skipped {skipped} unreadable files", file=sys.stderr)

    duplicate_sets = []
    unique_files = []

    for h, group in hash_map.items():
        if len(group) >= 2:
            keeper = choose_keeper([g["path"] for g in group], vault_path, clean_build_path)
            duplicates_bytes = sum(g["size"] for g in group if g["path"] != keeper)
            duplicate_sets.append({
                "sha256": h,
                "count": len(group),
                "files": [
                    {
                        "path": dir_label(g["path"], vault_path, clean_build_path),
                        "size": g["size"],
                        "is_keeper": g["path"] == keeper,
                    }
                    for g in group
                ],
                "bytes_wasted": duplicates_bytes,
            })
        else:
            unique_files.append(group[0])

    duplicate_sets.sort(key=lambda s: s["count"], reverse=True)
    return duplicate_sets, unique_files


# ---------------------------------------------------------------------------
# Tier 2 — ssdeep fuzzy dedup
# ---------------------------------------------------------------------------

def tier2_fuzzy(unique_files: list[dict], vault_path: str, clean_build_path: str) -> tuple[list[dict], list[dict]]:
    """Return (near_duplicates, review_queue).

    near_duplicates: pairs with score >= 90.
    review_queue: pairs with score 60-89.
    """
    # Compute fuzzy hashes
    print(f"  Tier 2: computing fuzzy hashes for {len(unique_files)} unique files…", file=sys.stderr)
    for i, f in enumerate(unique_files):
        if (i + 1) % 500 == 0:
            print(f"  Tier 2 hashing: {i + 1}/{len(unique_files)}", file=sys.stderr)
        f["fuzzy"] = fuzzy_hash_file(f["path"])

    hashable = [f for f in unique_files if f["fuzzy"] is not None]
    print(f"  Tier 2: {len(hashable)} files with valid fuzzy hashes", file=sys.stderr)

    # Group by extension for tractable comparison
    by_ext: dict[str, list[dict]] = defaultdict(list)
    for f in hashable:
        by_ext[f["ext"]].append(f)

    near_dupes = []  # score > 90
    review = []      # score 60-90
    comparisons = 0

    for ext, group in by_ext.items():
        n = len(group)
        if n < 2:
            continue
        # Sort by size for the ±50% window optimisation
        group.sort(key=lambda f: f["size"])

        for i in range(n):
            for j in range(i + 1, n):
                # Size filter: skip if sizes differ by more than 50%
                if group[i]["size"] > 0 and group[j]["size"] > 0:
                    ratio = group[j]["size"] / group[i]["size"]
                    if ratio > 1.5:
                        break  # sorted, so all further j are even larger
                elif group[i]["size"] == 0 and group[j]["size"] == 0:
                    pass  # both empty — compare anyway
                else:
                    continue  # one is zero, other isn't

                score = ssdeep_lib.compare(group[i]["fuzzy"], group[j]["fuzzy"])
                comparisons += 1

                if comparisons % 100000 == 0:
                    print(f"  Tier 2 comparisons: {comparisons}", file=sys.stderr)

                if score >= 60:
                    pair = {
                        "score": score,
                        "file_a": {
                            "path": dir_label(group[i]["path"], vault_path, clean_build_path),
                            "size": group[i]["size"],
                            "preview": first_n_chars(group[i]["path"]),
                        },
                        "file_b": {
                            "path": dir_label(group[j]["path"], vault_path, clean_build_path),
                            "size": group[j]["size"],
                            "preview": first_n_chars(group[j]["path"]),
                        },
                    }
                    if score >= 90:
                        near_dupes.append(pair)
                    else:
                        review.append(pair)

    print(f"  Tier 2: {comparisons} total comparisons", file=sys.stderr)

    near_dupes.sort(key=lambda p: p["score"], reverse=True)
    review.sort(key=lambda p: p["score"], reverse=True)
    return near_dupes, review


# ---------------------------------------------------------------------------
# Statistics & Markdown report
# ---------------------------------------------------------------------------

def generate_statistics(
    all_files: list[dict],
    duplicate_sets: list[dict],
    near_dupes: list[dict],
    review: list[dict],
    vault_path: str,
    clean_build_path: str,
) -> str:
    """Build DEDUP-STATISTICS.md content."""

    vp = os.path.abspath(vault_path)
    cp = os.path.abspath(clean_build_path)

    total = len(all_files)

    # By directory
    dir_counts: dict[str, int] = defaultdict(int)
    for f in all_files:
        ap = os.path.abspath(f["path"])
        if ap.startswith(vp):
            rel = os.path.relpath(ap, vp)
            top = rel.split(os.sep)[0] if os.sep in rel else "(root)"
            dir_counts[f"corpus-raw/vault/{top}"] += 1
        elif ap.startswith(cp):
            rel = os.path.relpath(ap, cp)
            top = rel.split(os.sep)[0]
            dir_counts[f"clean-build/{top}"] += 1

    # By extension
    ext_counts: dict[str, int] = defaultdict(int)
    for f in all_files:
        ext_counts[f["ext"] or "(no ext)"] += 1

    # Exact dup stats
    dup_file_count = sum(s["count"] - 1 for s in duplicate_sets)
    dup_bytes_saved = sum(s["bytes_wasted"] for s in duplicate_sets)
    unique_by_sha = total - dup_file_count

    # Near-dup score bands
    band_90 = len(near_dupes)
    band_80_90 = len([p for p in review if p["score"] >= 80])
    band_70_80 = len([p for p in review if 70 <= p["score"] < 80])
    band_60_70 = len([p for p in review if 60 <= p["score"] < 70])

    # Top 20 most-duplicated
    top20 = duplicate_sets[:20]

    # Vault subdirectory duplication breakdown
    vault_dir_dupes: dict[str, int] = defaultdict(int)
    for s in duplicate_sets:
        for f in s["files"]:
            if f["path"].startswith("corpus-raw/vault/"):
                parts = f["path"].replace("corpus-raw/vault/", "").split("/")
                vault_dir_dupes[parts[0]] += 1

    # Problem area analysis
    def count_paths_containing(sets: list[dict], *substrings: str) -> int:
        count = 0
        for s in sets:
            paths = [f["path"] for f in s["files"]]
            if all(any(sub in p for p in paths) for sub in substrings):
                count += 1
        return count

    inbox_vs_research = count_paths_containing(duplicate_sets, "_inbox/", "research/")
    inbox_voice_pairs = count_paths_containing(duplicate_sets, "_inbox-voice/")
    mono_vs_full = count_paths_containing(duplicate_sets, "monologue/", "monologue-full/")

    # Cross-repo overlap
    cross_repo = 0
    for s in duplicate_sets:
        paths = [f["path"] for f in s["files"]]
        has_vault = any(p.startswith("corpus-raw/vault") for p in paths)
        has_clean = any(p.startswith("clean-build/") for p in paths)
        if has_vault and has_clean:
            cross_repo += 1

    lines = [
        "# Dedup Statistics Report",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}",
        f"Signed-by: Devon (Devin) | {time.strftime('%Y-%m-%d')} | session 7cd95caf339c46a2896fbf6ffbda02be",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total files scanned | {total:,} |",
        f"| Unique files (SHA-256) | {unique_by_sha:,} |",
        f"| Exact duplicate sets | {len(duplicate_sets):,} |",
        f"| Duplicate files (would be removed) | {dup_file_count:,} |",
        f"| Bytes that would be saved | {human_bytes(dup_bytes_saved)} |",
        f"| Near-duplicate pairs (ssdeep >90) | {band_90:,} |",
        f"| Possible near-duplicates (60-90) | {band_80_90 + band_70_80 + band_60_70:,} |",
        "",
        "---",
        "",
        "## Files by Directory",
        "",
        "| Directory | Files |",
        "|-----------|-------|",
    ]
    for d in sorted(dir_counts, key=dir_counts.get, reverse=True):
        lines.append(f"| {d} | {dir_counts[d]:,} |")

    lines += [
        "",
        "## Files by Extension",
        "",
        "| Extension | Files |",
        "|-----------|-------|",
    ]
    for ext in sorted(ext_counts, key=ext_counts.get, reverse=True):
        lines.append(f"| {ext} | {ext_counts[ext]:,} |")

    lines += [
        "",
        "---",
        "",
        "## Tier 1: Exact Duplicates (SHA-256)",
        "",
        f"- **{len(duplicate_sets):,}** duplicate sets containing **{dup_file_count + len(duplicate_sets):,}** files",
        f"- **{dup_file_count:,}** redundant copies that could be removed",
        f"- **{human_bytes(dup_bytes_saved)}** would be reclaimed",
        "",
        "### Top 20 Most-Duplicated Files",
        "",
        "| Copies | Size | Keeper | Other locations |",
        "|--------|------|--------|-----------------|",
    ]
    for s in top20:
        keeper = next((f for f in s["files"] if f["is_keeper"]), s["files"][0])
        others = [f["path"] for f in s["files"] if not f["is_keeper"]]
        others_str = "; ".join(others[:5])
        if len(others) > 5:
            others_str += f" (+{len(others) - 5} more)"
        lines.append(f"| {s['count']} | {human_bytes(keeper['size'])} | `{keeper['path']}` | {others_str} |")

    lines += [
        "",
        "### Vault Subdirectory Duplication",
        "",
        "| Vault subdirectory | Files in duplicate sets |",
        "|--------------------|------------------------|",
    ]
    for d in sorted(vault_dir_dupes, key=vault_dir_dupes.get, reverse=True):
        lines.append(f"| {d} | {vault_dir_dupes[d]:,} |")

    lines += [
        "",
        "---",
        "",
        "## Tier 2: Fuzzy Near-Duplicates (ssdeep)",
        "",
        "| Score band | Pairs |",
        "|------------|-------|",
        f"| 90+ (auto-flag) | {band_90:,} |",
        f"| 80-90 | {band_80_90:,} |",
        f"| 70-80 | {band_70_80:,} |",
        f"| 60-70 | {band_60_70:,} |",
        "",
        "---",
        "",
        "## Known Problem Areas",
        "",
        f"| Area | Duplicate sets |",
        f"|------|---------------|",
        f"| `vault/_inbox/` vs `vault/research/` overlap | {inbox_vs_research} |",
        f"| `vault/_inbox-voice/` timestamp pairs | {inbox_voice_pairs} |",
        f"| `vault/transcripts/monologue/` vs `monologue-full/` | {mono_vs_full} |",
        f"| `corpus-raw/vault/` vs `clean-build/` cross-repo | {cross_repo} |",
        "",
        "---",
        "",
        "*This is a read-only analysis. No files were deleted or moved.*",
        "",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Dedup Tier 1+2 analysis")
    parser.add_argument("--vault-path", required=True, help="Path to corpus-raw/vault")
    parser.add_argument("--clean-build-path", required=True, help="Path to clean-build root")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: clean-build/02_build/scripts/dedup-output)")
    parser.add_argument("--dry-run", action="store_true", help="Count files only, no hashing")
    args = parser.parse_args()

    vault_path = os.path.abspath(args.vault_path)
    clean_build_path = os.path.abspath(args.clean_build_path)
    output_dir = args.output_dir or os.path.join(clean_build_path, "02_build", "scripts", "dedup-output")

    if not os.path.isdir(vault_path):
        print(f"ERROR: vault path not found: {vault_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(clean_build_path):
        print(f"ERROR: clean-build path not found: {clean_build_path}", file=sys.stderr)
        sys.exit(1)

    # --- Scan ---
    print("Scanning directories…", file=sys.stderr)
    all_files = scan_directories(vault_path, clean_build_path)
    print(f"  Found {len(all_files)} files", file=sys.stderr)

    if args.dry_run:
        ext_counts: dict[str, int] = defaultdict(int)
        for f in all_files:
            ext_counts[f["ext"] or "(no ext)"] += 1
        print("\n=== DRY RUN — file counts only ===")
        print(f"Total files: {len(all_files)}")
        print("\nBy extension:")
        for ext, count in sorted(ext_counts.items(), key=lambda x: -x[1]):
            print(f"  {ext:15s}  {count:,}")
        total_bytes = sum(f["size"] for f in all_files)
        print(f"\nTotal size: {human_bytes(total_bytes)}")
        return

    # --- Tier 1 ---
    print("\nRunning Tier 1: SHA-256 exact dedup…", file=sys.stderr)
    t1_start = time.time()
    duplicate_sets, unique_files = tier1_exact(all_files, vault_path, clean_build_path)
    t1_elapsed = time.time() - t1_start
    print(f"  Tier 1 done in {t1_elapsed:.1f}s — {len(duplicate_sets)} duplicate sets found", file=sys.stderr)

    # --- Tier 2 ---
    print("\nRunning Tier 2: ssdeep fuzzy dedup…", file=sys.stderr)
    t2_start = time.time()
    near_dupes, review_queue = tier2_fuzzy(unique_files, vault_path, clean_build_path)
    t2_elapsed = time.time() - t2_start
    print(f"  Tier 2 done in {t2_elapsed:.1f}s — {len(near_dupes)} near-dupes, {len(review_queue)} review-queue", file=sys.stderr)

    # --- Output ---
    os.makedirs(output_dir, exist_ok=True)

    signature = {
        "signed_by": "Devon (Devin)",
        "session": "7cd95caf339c46a2896fbf6ffbda02be",
        "date": time.strftime("%Y-%m-%d", time.gmtime()),
        "description": "Dedup Tier 1+2 analysis output",
    }

    # Tier 1 JSON
    t1_path = os.path.join(output_dir, "tier1-exact-duplicates.json")
    with open(t1_path, "w") as f:
        json.dump({**signature, "data": duplicate_sets}, f, indent=2)
    print(f"  Wrote {t1_path}", file=sys.stderr)

    # Tier 2 near-dupes JSON
    t2_path = os.path.join(output_dir, "tier2-near-duplicates.json")
    with open(t2_path, "w") as f:
        json.dump({**signature, "data": near_dupes}, f, indent=2)
    print(f"  Wrote {t2_path}", file=sys.stderr)

    # Tier 2 review queue JSON
    rq_path = os.path.join(output_dir, "tier2-review-queue.json")
    with open(rq_path, "w") as f:
        json.dump({**signature, "data": review_queue}, f, indent=2)
    print(f"  Wrote {rq_path}", file=sys.stderr)

    # Statistics markdown
    stats_md = generate_statistics(all_files, duplicate_sets, near_dupes, review_queue, vault_path, clean_build_path)
    stats_path = os.path.join(output_dir, "DEDUP-STATISTICS.md")
    with open(stats_path, "w") as f:
        f.write(stats_md)
    print(f"  Wrote {stats_path}", file=sys.stderr)

    print(f"\nDone. All output in {output_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
