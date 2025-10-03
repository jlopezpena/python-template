# Copier Template Migration Plan

## 1. Overview

This document describes the plan to migrate the current repository into a reusable and update-friendly [Copier](https://copier.readthedocs.io/) template. The objective is to allow future downstream projects created from this template to adopt updates via `copier update` with minimal conflicts.

## 2. Feasibility Assessment

Migration is highly feasible because: - Centralized configuration (`pyproject.toml`, `settings.ini`). - Opinionated tooling already curated (uv, nbdev, ruff, mypy, pytest, coverage, deptry, poe, CI). - Minimal source code: easy to parameterize package layout. - Generated artifacts (e.g. `_modidx.py`, README via nbdev) can be excluded or regenerated. - No hard-coded complex paths beyond the package structure.

## 3. Template Variables

Proposed variables (prompted unless noted as computed):

| Variable | Purpose | Default / Derivation |
|------------------|------------------|-------------------------------------|
| project_name | Human friendly project name | "My Python Project" |
| repo_name | Repository slug | slugify(project_name, dash) |
| package_namespace | Optional top-level namespace | "jlp" (allow empty) |
| package_name | Inner package/module name | repo_name with `-` -\> `_` |
| full_package_path | Computed import path | namespace + '.' + package_name |
| description | Short description | "Add your awesome description here" |
| author_name | Author | "Your Name" |
| author_email | Contact (optional) | "you\@example.com" |
| github_user | GitHub owner | sanitized author_name |
| license | Project license | MIT (choices: MIT, Apache-2.0, BSD-3-Clause, Proprietary) |
| min_python_version | Minimum Python runtime | 3.12 |
| ci_python_versions | List for CI matrix | \["3.12"\] |
| use_nbdev | Include nbdev integration | true |
| use_devcontainer | Include devcontainer setup | true |
| include_dependabot | Add Dependabot config | true |
| add_example_module | Include sample module & tests | true |
| enforce_coverage_100 | Set coverage fail_under=100 | true |
| use_namespace_pkg | Whether to nest in namespace dir | true if namespace provided |
| create_lock_on_init | Whether to include `uv.lock` | false |
| license_text | Generated from license | computed |
| current_year | Year for copyright | computed |

Computed (not prompted): - repo_url, docs_url, docs_baseurl.

## 4. Files to Template & Adjustments

### 4.1 `pyproject.toml`

-   Parameterize: name, description, URLs, requires-python.
-   Package path: `[tool.hatch.build.targets.wheel].packages` becomes dynamic.
-   Conditional dev dependencies (skip nbdev-related if `use_nbdev` is false).
-   Optionally gate certain linters/dep checkers with feature flags.

### 4.2 `settings.ini`

-   Present only if `use_nbdev`.
-   Replace repo, user, lib_path, min_python.

### 4.3 `README.md`

-   Insert Jinja variables for names and instructions.
-   Wrap nbdev-specific narrative in `{% if use_nbdev %}`.
-   Add a section describing how to update: `copier update`.

### 4.4 Source Layout

-   Dynamic path: `src/{{ package_namespace }}/{{ package_name }}/` or `src/{{ package_name }}/`.
-   Conditional example module `hello.py` & corresponding `say_hi` test.
-   `__init__.py` may include version retrieval or placeholder docstring.

### 4.5 Tests

-   Import pattern conditioned on namespace presence.
-   Example test optional via `add_example_module`.

### 4.6 CI Workflow `.github/workflows/check.yml`

-   Matrix from `ci_python_versions`.
-   Skip nbdev steps if disabled (omit notebook tests/export).

### 4.7 Devcontainer

-   Include only if `use_devcontainer`.
-   Allow future extensibility (optional features).

### 4.8 Dependabot

-   Included only if `include_dependabot`.

### 4.9 `.gitignore`

-   Mostly static; ensure excludes for nbdev build outputs remain conditional only if relevant.

### 4.10 Generated / Excluded Artifacts

-   Do NOT template: `uv.lock`, `_modidx.py`, `index_files/`.
-   Add instructions to regenerate: `uv sync`, `nbdev_export`, `nbdev_readme`.

### 4.11 Notebooks

-   Provide a minimal `index.ipynb` if `use_nbdev`.
-   Omit or replace richer assets for lean template footprint.

## 5. Copier Config (`copier.yaml`)

Key elements: - Variable prompts (see §3). - `_min_copier_version` for safety. - `_exclude` for generated/undesired files (`uv.lock`, `src/**/_modidx.py`, assets). - `_tasks` post-copy: `uv sync --all-extras --dev`; conditional nbdev tasks (`uv run nbdev_export`, `uv run nbdev_readme`). - Potential `_merge_strategies` to reduce conflict churn (e.g. replace certain files entirely).

## 6. Post-Copy Automation

Sample `_tasks` logic:

```
_tasks:
  - uv sync --all-extras --dev
  - {% if use_nbdev %}uv run nbdev_export && uv run nbdev_readme{% endif %}
```

(Exact YAML formatting will need validation.)

## 7. Update Strategy for Downstream Projects

1.  Downstream repo retains `.copier-answers.yml`.
2.  Users run `copier update` to pull template changes.
3.  Encourage minimal local edits in template-managed regions; annotate with comments: `# TEMPLATE-MANAGED`.
4.  Tag template releases (e.g. `v0.1.0`). Document changes in a CHANGELOG.

## 8. Conflict Minimization Guidelines

-   Avoid committing lockfiles in template (reduce spurious diffs).
-   Keep generated docs out of template base.
-   Restrict business logic—focus on scaffolding.
-   Use conditional blocks to prevent empty YAML arrays or malformed config.

## 9. Validation Matrix

Scenarios to test:

| Scenario | Namespace | nbdev | Devcontainer | Example Module | Expected |
|----------|-----------|-------|--------------|----------------|----------|
| Default | yes | yes | yes | yes | Full feature set builds & tests pass |
| No namespace | no | yes | yes | yes | Imports adjust correctly |
| No nbdev | yes | no | yes | yes | README hides nbdev, no nbdev deps |
| Minimal | no | no | no | no | Lean footprint, CI still green |

## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
|------------------|-----------------------|-------------------------------|
| Users edit templated sections | Update conflicts | Add comments, doc guidance |
| YAML indentation errors | Broken Copier generation | Validate locally with multiple runs |
| Conditional package path mistakes | Import failures | Automated test runs in validation matrix |
| Over-aggressive merge strategy | Loss of downstream custom work | Start conservative; document overrides |

## 11. Implementation Phases

1.  Preparation: create branch, clean generated files, decide exclusions.
2.  Add `copier.yaml` with core variables + excludes.
3.  Template `pyproject.toml`, `settings.ini`, source tree.
4.  Conditionalize README, CI, devcontainer, dependabot.
5.  Add tasks & test copy with scenarios (matrix above).
6.  Tag release & document usage.

## 12. Downstream Adoption for Existing Repos

For repos pre-dating template: 1. Manually create `.copier-answers.yml` with chosen values. 2. Align structure (namespace, paths). 3. Run `copier update`. 4. Resolve initial conflicts; subsequent updates smoother.

## 13. Future Enhancements

-   Optional doc system toggle (mkdocs vs nbdev).
-   Pre-commit hooks integration.
-   GitHub Pages deploy workflow.
-   License file templating with SPDX headers.
-   Additional linters / security scan toggles (e.g. bandit).

## 14. Acceptance Criteria

-   Copier can generate a working project for each scenario in §9 without manual fixes.
-   Running `uv sync` then `uv run pytest` passes.
-   `copier update` after a template change applies cleanly (tested on at least 2 scenarios).

## 15. Open Questions

-   Should version management (bump) be automated (e.g. via hatch version plugin)?
-   Include optional GitHub issue templates? (Could be gated variable.)
-   Provide dual licensing pattern?

## 16. Next Immediate Steps

1.  Implement `copier.yaml` (skeleton).
2.  Convert `pyproject.toml` to Jinja variables.
3.  Restructure `src` with conditional namespace.
4.  Add conditional logic to tests.
5.  Dry-run generation & fix formatting issues.

------------------------------------------------------------------------

Prepared: {{ date }}
