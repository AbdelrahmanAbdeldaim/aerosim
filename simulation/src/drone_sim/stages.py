"""Helpers for finding USD simulation stages."""

from pathlib import Path


def available_stages(stages_directory: Path) -> list[str]:
    """Return the names of the USD stages in a directory."""
    return sorted(path.stem for path in stages_directory.glob("*.usd"))


def resolve_stage_path(stages_directory: Path, stage_name: str) -> Path:
    """Resolve and validate a stage name within the stages directory."""
    normalized_name = stage_name.removesuffix(".usd")
    stage_path = stages_directory / f"{normalized_name}.usd"

    if not stage_path.is_file():
        choices = ", ".join(available_stages(stages_directory)) or "none"
        raise FileNotFoundError(
            f"Stage '{normalized_name}' does not exist in {stages_directory}. "
            f"Available stages: {choices}"
        )

    return stage_path
