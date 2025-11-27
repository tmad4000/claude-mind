#!/usr/bin/env python3
"""
Generate Markdown views from the research database JSON.

Usage:
    python tools/generate_research_views.py

This reads data/research_db.json and generates:
    - public/IDEA_BANK.md (all ideas, organized by status)
    - public/FAILED_ATTEMPTS.md (all failed attempts and falsified hypotheses)
    - public/PUBLISHABLE_FINDINGS.md (confirmed findings marked publishable)
    - knowledge/HYPOTHESIS_LIST.md (all hypotheses by category)
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DB_PATH = PROJECT_ROOT / "data" / "research_db.json"

def load_db():
    with open(DB_PATH) as f:
        return json.load(f)

def rating_stars(rating):
    """Convert numeric rating to star string."""
    return "⭐" * rating if rating else ""

def generate_idea_bank(db):
    """Generate IDEA_BANK.md from ideas."""

    ideas = db["ideas"]

    # Group by status
    promising = [i for i in ideas if i["status"] == "promising"]
    open_ideas = [i for i in ideas if i["status"] == "open"]
    failed = [i for i in ideas if i["status"] == "failed"]

    lines = [
        "# Research Idea Bank",
        "",
        "*Auto-generated from `data/research_db.json`*",
        "",
        f"**Last updated**: {db['meta']['last_updated']}",
        "",
        "---",
        "",
    ]

    # Promising ideas
    if promising:
        lines.append("## Promising Ideas (Ready for Action)")
        lines.append("")
        for idea in promising:
            lines.append(f"### {rating_stars(idea.get('rating', 0))} {idea['id']}: {idea['title']}")
            lines.append("")
            lines.append(f"**Status**: {idea['status'].upper()} | **Feasibility**: {idea.get('feasibility', 'unknown')} | **Impact**: {idea.get('impact', 'unknown')}")
            lines.append("")
            lines.append(idea["summary"])
            lines.append("")
            if idea.get("key_insight"):
                lines.append(f"**Key Insight**: {idea['key_insight']}")
                lines.append("")
            if idea.get("next_steps"):
                lines.append("**Next Steps**:")
                for step in idea["next_steps"]:
                    lines.append(f"- {step}")
                lines.append("")
            if idea.get("recommended_contacts"):
                lines.append("**Recommended Contacts**:")
                for contact in idea["recommended_contacts"]:
                    lines.append(f"- {contact}")
                lines.append("")
            if idea.get("references"):
                lines.append("**References**:")
                for ref in idea["references"]:
                    lines.append(f"- {ref}")
                lines.append("")
            lines.append("---")
            lines.append("")

    # Open ideas
    if open_ideas:
        lines.append("## Open Ideas (Need More Work)")
        lines.append("")
        for idea in open_ideas:
            lines.append(f"### {rating_stars(idea.get('rating', 0))} {idea['id']}: {idea['title']}")
            lines.append("")
            lines.append(f"**Status**: {idea['status']} | **Feasibility**: {idea.get('feasibility', 'unknown')} | **Impact**: {idea.get('impact', 'unknown')}")
            lines.append("")
            lines.append(idea["summary"])
            lines.append("")
            lines.append("---")
            lines.append("")

    # Failed ideas (brief)
    if failed:
        lines.append("## Failed/Rejected Ideas")
        lines.append("")
        lines.append("*See `public/FAILED_ATTEMPTS.md` for details.*")
        lines.append("")
        for idea in failed:
            lines.append(f"- **{idea['id']}**: {idea['title']} - {idea.get('failure_reason', 'No reason recorded')[:100]}...")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*This file is auto-generated. Edit `data/research_db.json` and run `python tools/generate_research_views.py`*")

    return "\n".join(lines)

def generate_failed_attempts(db):
    """Generate FAILED_ATTEMPTS.md from failed_attempts and falsified hypotheses."""

    failed_attempts = db.get("failed_attempts", [])
    falsified_hypotheses = [h for h in db.get("hypotheses", []) if h["status"] == "falsified"]
    failed_ideas = [i for i in db.get("ideas", []) if i["status"] == "failed"]

    lines = [
        "# Failed Attempts & Negative Results",
        "",
        "*A record of what didn't work and why. Negative results are valuable.*",
        "",
        "*Auto-generated from `data/research_db.json`*",
        "",
        f"**Last updated**: {db['meta']['last_updated']}",
        "",
        "---",
        "",
        "## Why This File Exists",
        "",
        "Science has a publication bias toward positive results. Failed experiments and falsified hypotheses",
        "rarely get documented, leading to wasted effort when others try the same thing.",
        "",
        "This file records our failures so we (and others) don't repeat them.",
        "",
        "---",
        "",
    ]

    # Failed synthesis/experimental attempts
    if failed_attempts:
        lines.append("## Failed Experimental Attempts")
        lines.append("")
        for attempt in failed_attempts:
            lines.append(f"### {attempt['id']}: {attempt['title']}")
            lines.append("")
            lines.append(f"**Category**: {attempt.get('category', 'unknown')}")
            if attempt.get('who_tried'):
                lines.append(f"**Who tried**: {attempt['who_tried']}")
            if attempt.get('date_recognized'):
                lines.append(f"**Date**: {attempt['date_recognized']}")
            lines.append("")
            lines.append(f"**What was tried**: {attempt['what_was_tried']}")
            lines.append("")
            lines.append(f"**Why it failed**: {attempt['why_it_failed']}")
            lines.append("")
            lines.append(f"**Lesson learned**: {attempt['lesson_learned']}")
            lines.append("")
            if attempt.get('original_reference'):
                lines.append(f"**Reference**: {attempt['original_reference']}")
                lines.append("")
            lines.append("---")
            lines.append("")

    # Falsified hypotheses
    if falsified_hypotheses:
        lines.append("## Falsified Hypotheses")
        lines.append("")
        for hyp in falsified_hypotheses:
            lines.append(f"### {hyp['id']}: {hyp['title']}")
            lines.append("")
            lines.append(f"**Category**: {hyp.get('category', 'unknown')}")
            if hyp.get('date_tested'):
                lines.append(f"**Date tested**: {hyp['date_tested']}")
            if hyp.get('tested_by'):
                lines.append(f"**Tested by**: {hyp['tested_by']}")
            lines.append("")
            lines.append(f"**Test**: {hyp['test_description']}")
            lines.append("")
            lines.append(f"**Result**: {hyp['result']}")
            lines.append("")
            if hyp.get('lessons_learned'):
                lines.append(f"**Lesson**: {hyp['lessons_learned']}")
                lines.append("")
            lines.append("---")
            lines.append("")

    # Failed ideas (that were evaluated and rejected)
    if failed_ideas:
        lines.append("## Rejected Research Ideas")
        lines.append("")
        for idea in failed_ideas:
            lines.append(f"### {idea['id']}: {idea['title']}")
            lines.append("")
            lines.append(idea["summary"])
            lines.append("")
            lines.append(f"**Why rejected**: {idea.get('failure_reason', 'No reason recorded')}")
            lines.append("")
            lines.append("---")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*This file is auto-generated. Edit `data/research_db.json` and run `python tools/generate_research_views.py`*")

    return "\n".join(lines)

def generate_findings(db):
    """Generate PUBLISHABLE_FINDINGS.md from confirmed findings."""

    findings = db.get("findings", [])
    publishable = [f for f in findings if "publishable" in f.get("tags", [])]
    other = [f for f in findings if "publishable" not in f.get("tags", [])]

    lines = [
        "# Publishable Findings",
        "",
        "*Discoveries that appear novel and potentially worth publishing.*",
        "",
        "*Auto-generated from `data/research_db.json`*",
        "",
        f"**Last updated**: {db['meta']['last_updated']}",
        "",
        "---",
        "",
    ]

    if publishable:
        lines.append("## High-Confidence Publishable Findings")
        lines.append("")
        for f in publishable:
            lines.append(f"### {f['id']}: {f['title']}")
            lines.append("")
            lines.append(f"**Status**: {f['status']} | **Confidence**: {f.get('confidence', 'unknown')}")
            lines.append("")
            lines.append(f"**Summary**: {f['summary']}")
            lines.append("")
            if f.get('implications'):
                lines.append(f"**Implications**: {f['implications']}")
                lines.append("")
            if f.get('novelty_assessment'):
                lines.append(f"**Novelty**: {f['novelty_assessment']}")
                lines.append("")
            lines.append("---")
            lines.append("")

    if other:
        lines.append("## Other Findings (Lower Confidence)")
        lines.append("")
        for f in other:
            lines.append(f"### {f['id']}: {f['title']}")
            lines.append("")
            lines.append(f"**Status**: {f['status']} | **Confidence**: {f.get('confidence', 'unknown')}")
            lines.append("")
            lines.append(f"{f['summary']}")
            lines.append("")
            if f.get('caveats'):
                lines.append(f"**Caveats**: {f['caveats']}")
                lines.append("")
            lines.append("---")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*This file is auto-generated. Edit `data/research_db.json` and run `python tools/generate_research_views.py`*")

    return "\n".join(lines)

def generate_hypothesis_list(db):
    """Generate HYPOTHESIS_LIST.md from hypotheses."""

    hypotheses = db.get("hypotheses", [])

    # Group by category
    by_category = {}
    for h in hypotheses:
        cat = h.get("category", "uncategorized")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(h)

    lines = [
        "# Hypothesis List",
        "",
        "*All hypotheses tested during exploration, organized by category.*",
        "",
        "*Auto-generated from `data/research_db.json`*",
        "",
        f"**Last updated**: {db['meta']['last_updated']}",
        "",
        "---",
        "",
        "## Summary Statistics",
        "",
    ]

    # Count by status
    confirmed = len([h for h in hypotheses if h["status"] == "confirmed"])
    falsified = len([h for h in hypotheses if h["status"] == "falsified"])
    partial = len([h for h in hypotheses if h["status"] == "partially-confirmed"])
    total = len(hypotheses)

    lines.append(f"| Status | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Confirmed | {confirmed} |")
    lines.append(f"| Partially Confirmed | {partial} |")
    lines.append(f"| Falsified | {falsified} |")
    lines.append(f"| **Total** | **{total}** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # By category
    for cat, hyps in sorted(by_category.items()):
        lines.append(f"## {cat.replace('-', ' ').title()}")
        lines.append("")
        for h in hyps:
            status_emoji = {"confirmed": "✓", "falsified": "✗", "partially-confirmed": "~"}.get(h["status"], "?")
            lines.append(f"### {status_emoji} {h['id']}: {h['title']}")
            lines.append("")
            lines.append(f"**Status**: {h['status'].upper()}")
            lines.append("")
            lines.append(f"**Test**: {h['test_description']}")
            lines.append("")
            lines.append(f"**Result**: {h['result']}")
            lines.append("")
            if h.get('lessons_learned'):
                lines.append(f"**Lesson**: {h['lessons_learned']}")
                lines.append("")
            lines.append("---")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*This file is auto-generated. Edit `data/research_db.json` and run `python tools/generate_research_views.py`*")

    return "\n".join(lines)

def main():
    print("Loading database...")
    db = load_db()

    print("Generating IDEA_BANK.md...")
    idea_bank = generate_idea_bank(db)
    (PROJECT_ROOT / "public" / "IDEA_BANK_generated.md").write_text(idea_bank)

    print("Generating FAILED_ATTEMPTS.md...")
    failed = generate_failed_attempts(db)
    (PROJECT_ROOT / "public" / "FAILED_ATTEMPTS.md").write_text(failed)

    print("Generating PUBLISHABLE_FINDINGS_generated.md...")
    findings = generate_findings(db)
    (PROJECT_ROOT / "public" / "PUBLISHABLE_FINDINGS_generated.md").write_text(findings)

    print("Generating HYPOTHESIS_LIST_generated.md...")
    hyp_list = generate_hypothesis_list(db)
    (PROJECT_ROOT / "knowledge" / "HYPOTHESIS_LIST_generated.md").write_text(hyp_list)

    print("Done! Generated files:")
    print("  - public/IDEA_BANK_generated.md")
    print("  - public/FAILED_ATTEMPTS.md")
    print("  - public/PUBLISHABLE_FINDINGS_generated.md")
    print("  - knowledge/HYPOTHESIS_LIST_generated.md")
    print("")
    print("Note: Generated files have '_generated' suffix to avoid overwriting manually curated files.")
    print("Once verified, you can rename them to replace the originals.")

if __name__ == "__main__":
    main()
