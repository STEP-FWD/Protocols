# STEP Protocols

**STEP (Standardized Template for Experimental Procedures)** is an open framework for developing, maintaining, and version-controlling experimental protocols. The framework was initially proposed by [Peter Bøggild et al.](https://www.nature.com/articles/s42254-025-00875-9) and is extended within the **STEP-FWD** project.

This repository contains curated STEP protocols designed to improve **reproducibility, collaboration, and continuous improvement** across experimental workflows.

---

# Purpose and Vision

STEP-FWD aims to enable:

* More reproducible science
* Collaborative protocol development
* Transparent evolution of experimental procedures

---

# Quick Start

The STEP protocols in this repository are organized into two categories:

* **Technique protocols** describe a general technique, such as electron-beam lithography, physical vapor deposition, or exfoliation.
* **Device protocols** describe the full fabrication workflow for a specific device, for example the process used to produce a device reported in a scientific publication.

## Naming Conventions

Each protocol should live in its own folder under either `protocols/techniques/` or `protocols/devices/`.

Use a **descriptive, unique, lowercase folder name** with hyphens as separators. For technique protocols, we recommend the format:

```text
<technique-name>-<system-identifier>-<details>
```

For example, for an electron-beam lithography protocol using the Raith Elphy Plus system with PMMA:

```text
ebl-raith-elphy-plus-pmma
```

## Option 1: Contributing with `git`
1. Fork this repository and clone your fork.
2. Create a new branch for your protocol.
3. Create a new folder in either `protocols/techniques/` or `protocols/devices/`.
4. Copy `templates/protocol.md` into your new folder as `protocol.md`.
5. If needed, add an `attachments/` folder for files referenced by the protocol to your folder.
6. Edit `protocol.md` following the template structure.
7. Review the protocol to ensure the content, naming, formatting, and referenced attachments are complete and correct.
8. Optionally, run `scripts/sequential_to_tabular.py` to generate and verify `tabular_protocol.md`.
9. Commit your changes with a clear commit message and push the branch to your fork.
10. Open a pull request to this repository and briefly describe:
  * What the protocol covers
  * Whether it is a technique or device protocol
  * Any important notes for reviewers

## Option 2: Contributing without `git`
1. Download `templates/protocol.md`.
2. Complete the template following its structure.
3. Review the protocol to ensure the content and formatting are correct.
4. Send the completed protocol to `ediz.herkert@icfo.eu` and briefly describe:
  * What the protocol covers
  * Whether it is a technique or device protocol
  * Any important notes for reviewers

---

# Repository Structure

```
protocols/
  techniques/
    <protocol-name>/
      protocol.md
      tabular_protocol.md
      attachments/
  devices/
    <protocol-name>/
      protocol.md
      tabular_protocol.md
      attachments/
  templates/
    protocol.md

scripts/
  sequential_to_tabular.py

README.md
ROADMAP.md
LICENSE

```

- `protocols/techniques/` → Technique protocols, stored in individual protocol folders (e.g. `protocols/techniques/ebl-raith-elphy-plus-pmma/`)
- `protocols/devices/` → Device-specific protocols, stored in individual protocol folders (e.g. `protocols/devices/twisted-bilayer-graphene/`)
- `protocol.md` → Sequential STEP protocol written in Markdown
- `tabular_protocol.md` → Tabular version generated from `protocol.md`
- `attachments/` → Referenced files such as images, documents, or tables
- `scripts/sequential_to_tabular.py` → Script that generates `tabular_protocol.md` from `protocol.md`

---

# Protocol Format

Each STEP protocol follows a structured format:

* Protocol name
* Authors with identifier (e.g. ORCID)
* Protocol description
* Steps and sub-steps including:
  * Materials and equipment (ME)
  * Parameters and ranges (PR)
  * Issues, warnings, troubleshooting, and difficulties (IWTD)
  * Validation and expected outcomes (VEO)
* Attachments

---

# Governance

Protocols in the `main` branch are considered **reviewed**. However, review does **not** guarantee that a protocol will work as written in every laboratory, facility, or experimental context.

Because these are complex experimental protocols, it is not feasible for the maintainers to independently validate every protocol under all relevant conditions. Performance may depend on equipment, materials, process history, operator experience, and local infrastructure.

For this reason, this repository relies on **community feedback and continued revision** to improve protocol quality and practical reliability over time. Users are strongly encouraged to report issues, suggest corrections, and share validation results through pull requests or issue discussions.

---

# License

This repository is licensed under **Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)**.

This means:

* You may use, modify, and distribute the protocols
* You must give appropriate credit
* Any modified versions must be shared under the same license
