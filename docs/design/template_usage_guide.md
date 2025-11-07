# Copier Template Usage Guide

This document consolidates the operational details for the `python-template` Copier template. Share it with maintainers and contributors so template updates stay consistent and reproducible.

## Rendering the template

1. Install Copier (`pip install copier` or `uv tool install copier`).
2. Provide answers either interactively or via an answers file (see `.copier-answers.sample.yml`).
3. Generate a new project:
   ```sh
   copier copy gh:jlopezpena/python-template my-new-project
   ```
4. Inside the generated project, run the post-copy sync (already part of `_tasks`):
   ```sh
   uv sync --group dev
   ```
   Add `--group nbdev` if the project enables nbdev.

To update an existing project, run `copier update` within the destination repository. Copier will reapply template changes and re-run the `_tasks` block.

## Template variables

| Variable | Description |
| --- | --- |
| `project_name` | Display name for docs and README |
| `repo_name` | GitHub repository slug |
| `package_namespace` | Optional namespace package (leave blank for flat layout) |
| `package_name` | Module name under the namespace or project |
| `description` | Short project summary |
| `author_name`, `author_email` | Used in LICENSE, metadata, docs |
| `github_user` | GitHub owner used in URLs |
| `license` | One of MIT, Apache-2.0, BSD-3-Clause, Proprietary |
| `min_python_version` | Lower bound for runtime and tooling |
| `ci_python_versions` | List of Python versions for CI matrix |
| `use_nbdev` | Adds nbdev assets, notebooks, and tasks |
| `use_devcontainer` | Adds `.devcontainer` folder |
| `include_dependabot` | Adds `.github/dependabot.yml` |
| `add_example_module` | Controls example module/tests (future work) |
| `enforce_coverage_100` | Sets coverage threshold to 100 or 85 |

## Optional assets controlled by tasks

- `use_nbdev=false` → removes `settings.ini`, `nbs/index.ipynb`, and strips nbdev-specific Poe tasks.
- `use_devcontainer=false` → removes `.devcontainer/` after rendering.
- `include_dependabot=false` → removes `.github/dependabot.yml` from the output.

These cleanups live in `_tasks`, so they run automatically after each `copier update`.

## Templated files overview

- `pyproject.toml.jinja` – project metadata, dependency groups, Poe tasks.
- `settings.ini.jinja` – nbdev settings, only rendered when enabled.
- `.github/workflows/check.yml.jinja` – CI matrix derived from `ci_python_versions` and nbdev toggle.
- `.github/dependabot.yml.jinja` – Dependabot configuration (optional).
- `.devcontainer/*` – Dev Container configuration (optional).
- `README.md.jinja` and `template_parts/readme_common.md.jinja` – shared README content.
- `nbs/index.ipynb.jinja` – notebook content consuming the README partial.
- `LICENSE.jinja` – license text based on the `license` variable.

Placeholder counterparts (without `.jinja`) remain in the repository so local tooling works but they are excluded for generated projects via `_exclude`.

## Maintaining the template

1. Keep runtime files free of complex Jinja control flow. Prefer simple `{{ variable }}` expressions or dedicated partials.
2. Run the smoke test workflow (`Template Smoke` CI) or locally:
   ```sh
   copier copy --answers-file .copier-answers.sample.yml --trust . /tmp/template-smoke
   cd /tmp/template-smoke
   uv sync --group dev --group nbdev
   uv run poe check
   uv run poe test
   ```
3. Sync README edits through `template_parts/readme_common.md.jinja` to avoid divergence between README and nbdev notebook.
4. Update `.copier-answers.sample.yml` when introducing new variables so CI remains aligned.
5. Bump `_version` in `copier.yaml` when shipping a backwards-incompatible change.

## Release checklist

- [ ] Run lint/tests in the template repo (`uv run poe check`).
- [ ] Run the Copier smoke test locally or rely on the CI workflow.
- [ ] Update design docs (`docs/design/`) with any new decisions.
- [ ] Tag the repository (e.g., `git tag template-vX.Y.Z`).
- [ ] Communicate upgrade guidance to downstream consumers.
