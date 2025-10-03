"""Top-level package for python-template.

TEMPLATE: values like project name and version will be parameterized by Copier in generated projects.
"""

__all__: list[str] = []

try:  # pragma: no cover - defensive import pattern
    from importlib.metadata import PackageNotFoundError, version  # type: ignore
    try:
        __version__ = version("python-template")  # TEMPLATE: {{ repo_name }}
    except PackageNotFoundError:  # pragma: no cover
        __version__ = "0.0.0"
except Exception:  # pragma: no cover
    __version__ = "0.0.0"
