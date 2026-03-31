from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

PROTOCOL_HEADING_PATTERN = re.compile(r"^#\s+Protocol\s*$", re.IGNORECASE)
PLACEHOLDER_SUBSTEP_IDENTIFIER_PATTERN = re.compile(r"^[xX]\.[xX]$")


@dataclass
class TabularRow:
    identifier: str
    step_cell: str
    substep_cell: str
    materials_equipment: str
    parameters_ranges: str
    issues_warnings: str
    validation_expected: str


def _split_main_step_heading(heading_text: str) -> Tuple[str, str]:
    stripped = heading_text.strip()
    match = re.match(r"^(\d+\.)\s+(.+)$", stripped)
    if match:
        return match.group(1), match.group(2).strip()
    return "", stripped


def _split_substep_heading(heading_text: str) -> Tuple[str, str]:
    stripped = heading_text.strip()
    match = re.match(r"^(\d+\.\d+)\s+(.+)$", stripped)
    if match:
        return match.group(1), match.group(2).strip()
    match = re.match(r"^([xX]\.[xX])(?:\s+(.+))?$", stripped)
    if match:
        remainder = (match.group(2) or "").strip()
        return match.group(1), remainder
    return "", stripped


def _classify_h4_heading(line: str) -> Optional[str]:
    normalized = line.strip().lower()
    if "materials and equipment" in normalized and "(me)" in normalized:
        return "me"
    if "parameters and ranges" in normalized and "(pr)" in normalized:
        return "pr"
    if "issues, warnings, troubleshooting" in normalized and "(iwtd)" in normalized:
        return "iwtd"
    if "validation and expected outcomes" in normalized and "(veo)" in normalized:
        return "veo"
    return None


def _collect_intro_lines(lines: List[str], start_index: int) -> Tuple[str, int]:
    buffer: List[str] = []
    index = start_index
    total = len(lines)
    while index < total:
        raw = lines[index]
        stripped = raw.strip()
        if stripped == "---":
            index += 1
            continue
        if raw.startswith("#### "):
            break
        if raw.startswith("### "):
            break
        if raw.startswith("## ") and not raw.startswith("###"):
            break
        buffer.append(raw.rstrip("\n"))
        index += 1
    return "\n".join(buffer).strip(), index


def _collect_section_body(lines: List[str], start_index: int) -> Tuple[str, int]:
    buffer: List[str] = []
    index = start_index
    total = len(lines)
    while index < total:
        raw = lines[index]
        stripped = raw.strip()
        if stripped == "---":
            break
        if raw.startswith("#### "):
            break
        if raw.startswith("### "):
            break
        if raw.startswith("## ") and not raw.startswith("###"):
            break
        buffer.append(raw.rstrip("\n"))
        index += 1
    return "\n".join(buffer).strip(), index


def _parse_me_pr_iwtd_veo(lines: List[str], start_index: int) -> Tuple[dict, int]:
    fields = {"me": "", "pr": "", "iwtd": "", "veo": ""}
    index = start_index
    total = len(lines)
    while index < total:
        raw = lines[index]
        stripped = raw.strip()
        if stripped == "---":
            index += 1
            continue
        if raw.startswith("## ") and not raw.startswith("###"):
            break
        if raw.startswith("### "):
            break
        if raw.startswith("#### "):
            key = _classify_h4_heading(raw)
            if key:
                body, next_index = _collect_section_body(lines, index + 1)
                fields[key] = body
                index = next_index
                continue
        index += 1
    return fields, index


def _parse_protocol_body(protocol_lines: List[str]) -> List[TabularRow]:
    rows: List[TabularRow] = []
    index = 0
    total = len(protocol_lines)

    while index < total:
        raw = protocol_lines[index]
        stripped = raw.strip()
        if stripped == "---":
            index += 1
            continue
        if raw.startswith("## ") and not raw.startswith("###"):
            heading_text = raw[3:].strip()
            step_id, step_name = _split_main_step_heading(heading_text)
            index += 1
            intro_text, index = _collect_intro_lines(protocol_lines, index)
            fields, index = _parse_me_pr_iwtd_veo(protocol_lines, index)
            if intro_text:
                step_cell = (
                    f"{step_name}\n\n{intro_text}" if step_name else intro_text
                )
            else:
                step_cell = step_name
            rows.append(
                TabularRow(
                    identifier=step_id,
                    step_cell=step_cell,
                    substep_cell="",
                    materials_equipment=fields["me"],
                    parameters_ranges=fields["pr"],
                    issues_warnings=fields["iwtd"],
                    validation_expected=fields["veo"],
                )
            )
            continue
        if raw.startswith("### "):
            sub_title = raw[4:].strip()
            sub_id, sub_name = _split_substep_heading(sub_title)
            index += 1
            intro_text, index = _collect_intro_lines(protocol_lines, index)
            fields, index = _parse_me_pr_iwtd_veo(protocol_lines, index)
            if sub_name:
                bold_title = f"**{sub_name}**"
                if intro_text:
                    sub_cell = f"{bold_title}\n\n{intro_text}"
                else:
                    sub_cell = bold_title
            else:
                sub_cell = intro_text
            rows.append(
                TabularRow(
                    identifier=sub_id,
                    step_cell="",
                    substep_cell=sub_cell,
                    materials_equipment=fields["me"],
                    parameters_ranges=fields["pr"],
                    issues_warnings=fields["iwtd"],
                    validation_expected=fields["veo"],
                )
            )
            continue
        index += 1

    return rows


def _validate_tabular_row_identifiers(rows: List[TabularRow]) -> None:
    last_main_step_number = 0
    last_substep_number: Optional[int] = None

    for row_index, row in enumerate(rows, start=1):
        raw_id = row.identifier.strip()
        if not raw_id:
            raise ValueError(f"Row {row_index}: ID is empty (use numbered ## / ### headings)")

        if PLACEHOLDER_SUBSTEP_IDENTIFIER_PATTERN.match(raw_id):
            continue

        main_step_only = re.match(r"^(\d+)\.$", raw_id)
        if main_step_only:
            main_num = int(main_step_only.group(1))
            if last_main_step_number == 0:
                if main_num != 1:
                    raise ValueError(
                        f"Row {row_index}: first main step must be 1., not {raw_id!r}"
                    )
            elif main_num != last_main_step_number + 1:
                raise ValueError(
                    f"Row {row_index}: main step IDs must increase by 1 without gaps "
                    f"(expected {last_main_step_number + 1}., found {raw_id!r})"
                )
            last_main_step_number = main_num
            last_substep_number = None
            continue

        sub_step_match = re.match(r"^(\d+)\.(\d+)$", raw_id)
        if sub_step_match:
            parent_main = int(sub_step_match.group(1))
            sub_num = int(sub_step_match.group(2))
            if last_main_step_number == 0:
                raise ValueError(
                    f"Row {row_index}: sub-step {raw_id!r} appears before any main step (##)"
                )
            if parent_main != last_main_step_number:
                raise ValueError(
                    f"Row {row_index}: sub-step {raw_id!r} must belong to current main step "
                    f"{last_main_step_number}., not {parent_main}"
                )
            if last_substep_number is None:
                if sub_num != 1:
                    raise ValueError(
                        f"Row {row_index}: first sub-step under {last_main_step_number}. "
                        f"must be {last_main_step_number}.1, not {raw_id!r}"
                    )
            elif sub_num != last_substep_number + 1:
                raise ValueError(
                    f"Row {row_index}: sub-step IDs must increase by 1 without gaps "
                    f"(after {last_main_step_number}.{last_substep_number} expected "
                    f"{last_main_step_number}.{last_substep_number + 1}, found {raw_id!r})"
                )
            last_substep_number = sub_num
            continue

        raise ValueError(
            f"Row {row_index}: ID {raw_id!r} is not 1., 2., … or 1.1, 1.2, … (or placeholder x.x)"
        )


def _find_protocol_heading_index(lines: List[str]) -> int:
    for idx, line in enumerate(lines):
        if PROTOCOL_HEADING_PATTERN.match(line.strip()):
            return idx
    raise ValueError("No top-level '# Protocol' heading found.")


def _find_next_h1_index(lines: List[str], start_index: int) -> int:
    for idx in range(start_index, len(lines)):
        candidate = lines[idx]
        if candidate.startswith("# ") and not candidate.startswith("##"):
            return idx
    return len(lines)


def _markdown_list_markers_to_bullet_glyphs(text: str) -> str:
    converted_lines: List[str] = []
    for line in text.split("\n"):
        asterisk_match = re.match(r"^(\s*)\*\s+(.*)$", line)
        if asterisk_match:
            converted_lines.append(
                f"{asterisk_match.group(1)}• {asterisk_match.group(2)}"
            )
            continue
        dash_match = re.match(r"^(\s*)-\s+(.*)$", line)
        if dash_match:
            converted_lines.append(f"{dash_match.group(1)}• {dash_match.group(2)}")
            continue
        converted_lines.append(line)
    return "\n".join(converted_lines)


def _format_table_cell(text: str) -> str:
    if not text.strip():
        return " "
    with_visual_bullets = _markdown_list_markers_to_bullet_glyphs(text)
    return with_visual_bullets.replace("|", "\\|").replace("\n", "<br>")


def _render_markdown_table(rows: List[TabularRow]) -> str:
    header = (
        "| ID | Step | Sub-step | ME | PR | IWTD | VEO |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
    )
    body_lines: List[str] = []
    for row in rows:
        line = (
            f"| {_format_table_cell(row.identifier)} | "
            f"{_format_table_cell(row.step_cell)} | "
            f"{_format_table_cell(row.substep_cell)} | "
            f"{_format_table_cell(row.materials_equipment)} | "
            f"{_format_table_cell(row.parameters_ranges)} | "
            f"{_format_table_cell(row.issues_warnings)} | "
            f"{_format_table_cell(row.validation_expected)} |\n"
        )
        body_lines.append(line)
    return header + "".join(body_lines)


def _split_document(lines: List[str]) -> Tuple[List[str], List[str], List[str]]:
    protocol_heading_index = _find_protocol_heading_index(lines)
    body_start = protocol_heading_index + 1
    next_h1 = _find_next_h1_index(lines, body_start)
    preamble = lines[: protocol_heading_index + 1]
    protocol_body = lines[body_start:next_h1]
    remainder = lines[next_h1:]
    return preamble, protocol_body, remainder


def repository_root_path() -> Path:
    return Path(__file__).resolve().parent.parent


def protocols_category_roots(repository_root: Path) -> List[Path]:
    category_names = ("devices", "techniques")
    roots: List[Path] = []
    for category in category_names:
        candidate = repository_root / "protocols" / category
        if candidate.is_dir():
            roots.append(candidate)
    return roots


def discover_protocol_markdown_files(search_roots: List[Path]) -> List[Path]:
    paths: List[Path] = []
    for root in search_roots:
        paths.extend(root.rglob("protocol.md"))
    return sorted({path.resolve() for path in paths})


def extract_protocol_title(protocol_text: str, fallback: str) -> str:
    """First `# ...` heading in protocol.md (the protocol name); skips a lone `# Protocol`."""
    for line in protocol_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            if title.lower() == "protocol":
                continue
            return title
    return fallback


def _build_mkdocs_nav_entries(repository_root: Path) -> List[Dict[str, Any]]:
    """Nav entries for MkDocs: Home, then Technique Protocols / Device Protocols sections."""
    protocols_root = repository_root / "protocols"
    nav: List[Dict[str, Any]] = [{"Home": "index.md"}]
    for category, section_title in (
        ("techniques", "Technique Protocols"),
        ("devices", "Device Protocols"),
    ):
        category_path = protocols_root / category
        if not category_path.is_dir():
            continue
        items: List[Dict[str, str]] = []
        for protocol_path in sorted(category_path.rglob("protocol.md")):
            tabular_path = protocol_path.parent / "tabular_protocol.md"
            if not tabular_path.is_file():
                continue
            text = protocol_path.read_text(encoding="utf-8")
            title = extract_protocol_title(text, fallback=protocol_path.parent.name)
            rel = tabular_path.relative_to(protocols_root).as_posix()
            items.append({title: rel})
        if items:
            nav.append({section_title: items})
    return nav


def rebuild_mkdocs_nav(repository_root: Path) -> None:
    """Rewrite `docs/mkdocs.yml` `nav` with one entry per tabular protocol (title from protocol.md)."""
    if yaml is None:
        print(
            "Warning: PyYAML is not installed; skipping docs/mkdocs.yml nav update. "
            "Install with: pip install pyyaml",
            file=sys.stderr,
        )
        return
    mkdocs_path = repository_root / "docs" / "mkdocs.yml"
    if not mkdocs_path.is_file():
        print(f"Warning: {mkdocs_path} not found; skipping nav update.", file=sys.stderr)
        return
    raw = mkdocs_path.read_text(encoding="utf-8")
    config = yaml.safe_load(raw) or {}
    config["nav"] = _build_mkdocs_nav_entries(repository_root)
    mkdocs_path.write_text(
        yaml.safe_dump(
            config,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            indent=2,
        ),
        encoding="utf-8",
        newline="\n",
    )


def convert_sequential_protocol_to_tabular_markdown(source_text: str) -> str:
    raw_lines = source_text.splitlines()
    lines = [line.rstrip("\r") for line in raw_lines]
    preamble, protocol_body, remainder = _split_document(lines)
    rows = _parse_protocol_body(protocol_body)
    _validate_tabular_row_identifiers(rows)
    table_block = _render_markdown_table(rows)
    out_chunks: List[str] = []
    if preamble:
        out_chunks.append("\n".join(preamble))
    out_chunks.append("")
    out_chunks.append(table_block.rstrip("\n"))
    if remainder:
        out_chunks.append("")
        out_chunks.append("\n".join(remainder))
    return "\n".join(out_chunks) + "\n"


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert sequential protocol Markdown below '# Protocol' into a pipe table. "
            "With no input file, writes tabular_protocol.md next to each protocols/devices/**/protocol.md "
            "and protocols/techniques/**/protocol.md."
        ),
    )
    parser.add_argument(
        "input_path",
        nargs="?",
        type=Path,
        default=None,
        help="Single protocol.md path (optional; omit to batch-convert devices and techniques)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output path when input_path is set (default: stdout)",
    )
    return parser.parse_args(argv)


def _run_batch_conversion(repository_root: Path) -> int:
    search_roots = protocols_category_roots(repository_root)
    protocol_paths = discover_protocol_markdown_files(search_roots)
    if not protocol_paths:
        print(
            "No protocol.md files found under protocols/devices or protocols/techniques "
            "(directories may be missing or empty).",
            file=sys.stderr,
        )
        return 1
    failures: List[str] = []
    for protocol_path in protocol_paths:
        try:
            source_text = protocol_path.read_text(encoding="utf-8")
            output_text = convert_sequential_protocol_to_tabular_markdown(source_text)
            output_path = protocol_path.parent / "tabular_protocol.md"
            output_path.write_text(output_text, encoding="utf-8", newline="\n")
        except ValueError as exc:
            failures.append(f"{protocol_path}: {exc}")
    for message in failures:
        print(message, file=sys.stderr)
    try:
        rebuild_mkdocs_nav(repository_root)
    except Exception as exc:
        print(f"Warning: could not update docs/mkdocs.yml: {exc}", file=sys.stderr)
    return 1 if failures else 0


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)
    repository_root = repository_root_path()

    if args.input_path is None:
        return _run_batch_conversion(repository_root)

    input_text = args.input_path.read_text(encoding="utf-8")
    output_text = convert_sequential_protocol_to_tabular_markdown(input_text)
    if args.output is None:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(output_text)
    else:
        args.output.write_text(output_text, encoding="utf-8", newline="\n")
        try:
            rebuild_mkdocs_nav(repository_root)
        except Exception as exc:
            print(f"Warning: could not update docs/mkdocs.yml: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
