# GitHub Action conversion test

**Authors:** CI test
**Created:** 2026-04-08
**Last modified:** 2026-04-08

## Description

This protocol exists to verify that **pushing a YAML file** under `docs/` triggers the
workflow and regenerates the matching `.md` file.


# Single test section

| Step | Task | Subtask | Materials | Parameters | Warnings | Verification |
|------|------|-------|------------|----------|--------------|---------|
| 1.0 | Push this branch to GitHub | Open Actions and confirm the workflow ran | A repository with this workflow enabled | workflow_dispatch or a push that changes *.yaml | If the job cannot push, check branch protection and contents write permission | test_ci/test_github_action_v1.md should appear or update in the repo |
| 2.0 | Test if I can modify the file online and render it real-time | Check that I can modify from GitHub | GitHub actions | workflow_dispatch or a push that changes *.yaml | How does it work? |  |

