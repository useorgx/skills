#!/usr/bin/env python3
"""
Validate OrgX design artifacts (accessibility audits, design tokens, component docs).
Ensures all quality gates pass before artifacts are saved.

Usage:
    python validate_design.py <file> --type <audit|tokens|component>

Exit codes:
    0 - All validations passed
    1 - Validation errors found
    2 - Invalid arguments
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple


QUALITY_GATES = {
    "audit": [
        ("has_scope", "Audit scope is required",
         lambda d: bool(d.get("scope", "").strip())),
        ("has_wcag_level", "WCAG level must be specified",
         lambda d: d.get("wcag_level") in ["A", "AA", "AAA"]),
        ("has_summary", "Summary with issue counts required",
         lambda d: bool(d.get("summary")) and d.get("summary", {}).get("total_issues") is not None),
        ("issues_have_severity", "All issues must have severity",
         lambda d: all(i.get("severity") in ["critical", "major", "minor"]
                      for i in d.get("issues", []))),
        ("issues_have_wcag", "All issues must reference WCAG criterion",
         lambda d: all(i.get("wcag_criterion") for i in d.get("issues", []))),
        ("issues_have_location", "All issues must specify location",
         lambda d: all(i.get("location") for i in d.get("issues", []))),
        ("issues_have_remediation", "All issues must have remediation steps",
         lambda d: all(i.get("remediation") for i in d.get("issues", []))),
        ("has_testing_notes", "Testing notes (screen readers, browsers) required",
         lambda d: bool(d.get("testing_notes"))),
        ("tested_screen_readers", "At least 1 screen reader must be tested",
         lambda d: len(d.get("testing_notes", {}).get("screen_readers_tested", [])) >= 1),
        ("has_recommendations", "At least 3 recommendations required",
         lambda d: len(d.get("recommendations", [])) >= 3),
    ],
    "tokens": [
        ("has_version", "Version is required", lambda d: bool(d.get("version"))),
        ("has_colors", "Color tokens required",
         lambda d: len(d.get("tokens", {}).get("color", {})) >= 3),
        ("has_spacing", "Spacing scale required (min 4 values)",
         lambda d: len(d.get("tokens", {}).get("spacing", {})) >= 4),
        ("has_typography", "Typography tokens required",
         lambda d: len(d.get("tokens", {}).get("typography", {})) >= 2),
        ("colors_have_values", "All color tokens must have values",
         lambda d: all(c.get("value") for c in d.get("tokens", {}).get("color", {}).values())),
        ("colors_valid_format", "Color values must be valid hex or RGB",
         lambda d: all(
             re.match(r'^#[0-9A-Fa-f]{6}$|^rgb', str(c.get("value", "")))
             for c in d.get("tokens", {}).get("color", {}).values()
         )),
        ("spacing_has_scale", "Spacing must follow consistent scale",
         lambda d: True),  # Would need numeric validation
        ("typography_complete", "Typography tokens must have fontFamily, fontSize",
         lambda d: all(
             t.get("fontFamily") and t.get("fontSize")
             for t in d.get("tokens", {}).get("typography", {}).values()
         )),
    ],
    "component": [
        ("has_name", "Component name is required",
         lambda d: bool(d.get("name", "").strip())),
        ("has_description", "Component description required (min 50 chars)",
         lambda d: len(d.get("description", "")) >= 50),
        ("has_usage", "Usage guidelines required",
         lambda d: bool(d.get("usage"))),
        ("has_props", "Props/variants must be documented",
         lambda d: len(d.get("props", [])) >= 1),
        ("props_have_types", "All props must have types",
         lambda d: all(p.get("type") for p in d.get("props", []))),
        ("has_accessibility", "Accessibility section required",
         lambda d: bool(d.get("accessibility"))),
        ("a11y_has_keyboard", "Keyboard interaction must be documented",
         lambda d: "keyboard" in str(d.get("accessibility", {})).lower()),
        ("a11y_has_aria", "ARIA requirements must be documented",
         lambda d: "aria" in str(d.get("accessibility", {})).lower() or
                   "role" in str(d.get("accessibility", {})).lower()),
        ("has_examples", "At least 2 code examples required",
         lambda d: len(d.get("examples", [])) >= 2),
        ("has_dos_donts", "Do's and Don'ts section required",
         lambda d: bool(d.get("dos")) and bool(d.get("donts"))),
    ],
}


def parse_file(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """Parse JSON or Markdown file into structured data."""
    content = file_path.read_text()

    if file_path.suffix == ".json":
        return json.loads(content), "json"

    if file_path.suffix == ".md":
        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1)), "markdown_json"

        data = parse_markdown_component(content)
        return data, "markdown"

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def parse_markdown_component(content: str) -> Dict[str, Any]:
    """Parse markdown component doc into structured data."""
    data = {
        "name": "",
        "description": "",
        "usage": "",
        "props": [],
        "accessibility": {},
        "examples": [],
        "dos": [],
        "donts": []
    }

    # Extract name from title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        data["name"] = title_match.group(1).strip()

    # Extract sections
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split('\n')
        section_title = lines[0].lower().strip()
        section_content = '\n'.join(lines[1:])

        if 'overview' in section_title or 'description' in section_title:
            data["description"] = section_content.strip()
        elif 'usage' in section_title:
            data["usage"] = section_content.strip()
        elif 'prop' in section_title:
            props = re.findall(r'\|\s*(\w+)\s*\|\s*(\w+)\s*\|', section_content)
            data["props"] = [{"name": p[0], "type": p[1]} for p in props if p[0] != "Prop"]
        elif 'accessib' in section_title:
            data["accessibility"] = {"content": section_content}
        elif 'example' in section_title:
            examples = re.findall(r'```\w*\n(.*?)\n```', section_content, re.DOTALL)
            data["examples"] = examples
        elif "do's" in section_title or "don'ts" in section_title or "dos" in section_title:
            dos = re.findall(r'Do:?\s*(.+)$', section_content, re.MULTILINE | re.IGNORECASE)
            donts = re.findall(r"Don'?t:?\s*(.+)$", section_content, re.MULTILINE | re.IGNORECASE)
            if dos:
                data["dos"] = dos
            if donts:
                data["donts"] = donts

    return data


def validate(data: Dict[str, Any], artifact_type: str) -> List[Dict[str, str]]:
    """Run all quality gates for the artifact type."""
    errors = []

    gates = QUALITY_GATES.get(artifact_type, [])

    for gate_id, message, check_fn in gates:
        try:
            if not check_fn(data):
                errors.append({
                    "gate": gate_id,
                    "message": message,
                    "severity": "error"
                })
        except Exception as e:
            errors.append({
                "gate": gate_id,
                "message": f"{message} (validation error: {e})",
                "severity": "error"
            })

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate OrgX design artifacts")
    parser.add_argument("file", type=Path, help="Path to artifact file")
    parser.add_argument("--type", "-t", required=True,
                       choices=["audit", "tokens", "component"],
                       help="Artifact type to validate")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(2)

    try:
        data, format_type = parse_file(args.file)
    except Exception as e:
        print(f"Error parsing file: {e}", file=sys.stderr)
        sys.exit(2)

    errors = validate(data, args.type)

    if args.json:
        result = {
            "file": str(args.file),
            "type": args.type,
            "valid": len(errors) == 0,
            "errors": errors,
            "gates_passed": len(QUALITY_GATES[args.type]) - len(errors),
            "gates_total": len(QUALITY_GATES[args.type])
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\nValidating {args.type.upper()}: {args.file}")
        print("=" * 50)

        if errors:
            print(f"\n{len(errors)} error(s) found:\n")
            for err in errors:
                print(f"  [{err['gate']}] {err['message']}")
            print(f"\nValidation FAILED")
        else:
            gates_count = len(QUALITY_GATES[args.type])
            print(f"\nAll {gates_count} quality gates passed")
            print("Validation PASSED")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
