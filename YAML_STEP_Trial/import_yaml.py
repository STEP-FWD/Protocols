import yaml
import os
import copy

#folder= 'C:/Users/jdiez/Documents/GitHub/Protocols/YAML_STEP_Trial/docs/'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# ------------------------
# Load all YAML protocols
# ------------------------

def load_protocols(folder=DOCS_DIR):
    protocols = {}

    for file in os.listdir(folder):
        if file.endswith(".yaml"):
            with open(os.path.join(folder, file), "r") as f:
                data = yaml.safe_load(f)

                pid = data["protocol"]["id"]
                protocols[pid] = data
    return protocols


# Merge child with parent
def resolve_inheritance(protocols, proto):
    if "inherits_from" not in proto:
        return proto

    parent = protocols[proto["inherits_from"]]

    # Recursively resolve parent
    parent_resolved = resolve_inheritance(protocols, parent)

    # Deep copy parent
    merged = copy.deepcopy(parent_resolved)

    # Apply modifications
    if "modifications" in proto:
        for mod in proto["modifications"]:
            step_id = mod["step_id"]

            for section in merged["sections"]:
                for step in section["steps"]:
                    if step["id"] == step_id:
                        step.update(mod)
    if supplementary := proto.get("supplementary"):
        merged["supplementary"] = supplementary
    if references := proto.get("references"):
        merged["references"] = references        

    # Override metadata if present
    if "metadata" in proto:
        merged["metadata"] = proto["metadata"]

    # Override title if present
    if "protocol" in proto:
        merged["protocol"].update(proto["protocol"])

    return merged


# ------------------------
# Render protocol (IMPROVED UI)
# ------------------------

def _table_cell(val):
    """Single-line markdown table cell: YAML blocks often end with \\n which breaks pipe tables."""
    if val is None:
        return ""
    return " ".join(str(val).split())


def render(protocol):
    out = []
    # Title
    out.append(f"# {protocol['protocol']['title']}\n")
    # Metadata
    meta = protocol.get("metadata", {})
    if meta:
        out.append(f"**Authors:** {', '.join(meta.get('authors', []))}")
        out.append(f"**Created:** {meta.get('created', '')}")
        out.append(f"**Last modified:** {meta.get('last_modified', '')}\n")
    # Description
    if "description" in protocol:
        out.append("## Description\n")
        out.append(protocol["description"] + "\n")
    # Sections
    for section in protocol["sections"]:
        out.append(f"# {section['title']}\n")

        out.append("| Step | Task | Subtask | Materials | Parameters | Warnings | Verification |")
        out.append("|------|------|-------|------------|----------|--------------|---------|")

        for step in section["steps"]:
            row = "| {} | {} | {} | {} | {} | {} | {} |".format(
                _table_cell(step.get("id")),
                _table_cell(step.get("task")),
                _table_cell(step.get("subtask")),
                _table_cell(step.get("materials")),
                _table_cell(step.get("parameters")),
                _table_cell(step.get("warnings")),
                _table_cell(step.get("verification")),
            )
            out.append(row)

        out.append("\n")

    if "supplementary" in protocol:
        out.append("## Supplementary Material\n")
        out.append(protocol["supplementary"] + "\n")
    if "references" in protocol:
        out.append("## References\n")
        out.append(protocol["references"] + "\n")

    return "\n".join(out)

# ------------------------
# Generate all markdown files
# ------------------------

def generate_markdown(protocols):
    nav = {}
    preamble_path = os.path.join(DOCS_DIR, "preamble.md")

    if os.path.exists(preamble_path):
        with open(preamble_path, "r") as f:
            preamble = f.read()
    else:
        preamble = ""

    index_lines = [
        "# STEP Protocol Database\n",
        preamble,
        "\n---\n",
        "## Protocol Families\n"
    ]

    for pid, proto in protocols.items():
        resolved = resolve_inheritance(protocols, proto)

        category = resolved.get("category", "general")
        category_path = os.path.join(DOCS_DIR, category)
        os.makedirs(category_path, exist_ok=True)

        filename = f"{pid}.md"
        filepath = os.path.join(category_path, filename)

        # Write markdown
        with open(filepath, "w") as f:
            f.write(render(resolved))

        # Navigation structure
        if category not in nav:
            nav[category] = []

        nav[category].append((resolved["protocol"]["title"], f"{category}/{filename}"))

    # Build index.md
    for cat, items in nav.items():
        index_lines.append(f"### {cat.replace('_',' ').title()}\n")
        for title, path in items:
            index_lines.append(f"- [{title}]({path})")
        index_lines.append("")

    with open(os.path.join(DOCS_DIR, "index.md"), "w") as f:
        f.write("\n".join(index_lines))

    return nav

#OUTPUT_DIR = DOCS_DIR

# ------------------------
# Generate mkdocs.yml
# ------------------------
def generate_mkdocs(nav):
    lines = [
        "site_name: STEP Protocols",
        "site_description: A collection of standardized protocols for scientific experiments.",
        "theme:",
        "  name: material",
        "",
        "nav:",
        "  - Home: index.md",
    ]

    for cat, items in nav.items():
        lines.append(f"  - {cat.replace('_',' ').title()}:")
        for title, path in items:
            lines.append(f"      - {title}: {path}")

    with open(os.path.join(BASE_DIR, "mkdocs.yml"), "w") as f:
        f.write("\n".join(lines))

# ------------------------
# MAIN
# ------------------------
protocols = load_protocols()
nav = generate_markdown(protocols)
generate_mkdocs(nav)

'''
for pid, proto in protocols.items():
    resolved = resolve_inheritance(protocols, proto)
    content = render(resolved)

    # Save inside folder based on category (default: root)
    folder = resolved.get("category", "general")

    folder_path = os.path.join(DOCS_DIR, folder)
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{pid}.md"
    filepath = os.path.join(folder_path, filename)

    with open(filepath, "w") as f:
        f.write(content)
'''