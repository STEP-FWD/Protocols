# STEP Protocols

**STEP (Standardized Template for Experimental Procedures)** is an open framework for developing, maintaining, and version-controlling experimental protocols. The framework was initially proposed by [Peter Bøggild et al.](https://www.nature.com/articles/s42254-025-00875-9) and is extended within the **STEP-FWD** project.

This repository contains curated STEP protocols designed to improve **reproducibility, collaboration, and continuous improvement** across experimental workflows.

## Purpose and Vision

STEP-FWD aims to enable:

* More reproducible science
* Collaborative protocol development
* Transparent evolution of experimental procedures

## Quick Start

To be filled by Jaime

## Repository Structure

```
protocols/
  techniques/
    <technique-name>/
      <protocol-name>/
        protocol.md
        protocol.yaml
        attachments/
  devices/
      <protocol-name>/
        protocol.md
        protocol.yaml
        attachments/

templates/
  protocol.yaml

scripts/

README.md
CONTRIBUTING.md
ROADMAP.md
LICENSE

```

* `protocols/techniques` → protocols organized by technique (e.g. lithography)
* `protocols/devices` → protocols organized by specific device type (e.g. twisted bilayer graphene)
* `protocol.yaml` → primary STEP protocol as source for `protocol.md`
* `protocol.md` → human-readable Markdown version generated from protocol.yaml
* `attachments/` → supplementary material referenced by the protocol, such as images or tables

## Protocol Format

Each STEP protocol follows a structured format:

* Protocol name
* Authors, ideally with ORCID
* Step-by-step procedure including:
  * Materials and equipment (ME)
  * Parameters and ranges 
  * Issues, warnings, troubleshooting, and difficulties (IWTD)
  * Validation and expected outcomes (VEO)
* References
* Supplementary information

## Governance

Protocols in the `main` branch are considered **reviewed and approved**.

Changes require:

* Pull request review
* Consistency with STEP standards
* Clear justification for modifications

## License

This repository is licensed under **Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)**.

This means:

* You may use, modify, and distribute the protocols
* You must give appropriate credit
* Any modified versions must be shared under the same license
