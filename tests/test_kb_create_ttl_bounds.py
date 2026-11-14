"""Regression tests for ephemeral KB TTL validation (#1407)."""

import pytest
from click import unstyle


@pytest.mark.cli
@pytest.mark.parametrize("ttl", [-1, -5])
def test_kb_create_rejects_negative_ephemeral_ttl(cli_world, ttl):
    world = cli_world()
    name = f"negative-ttl-{abs(ttl)}"

    result = world.cli(
        "kb", "create", "--ephemeral", "--name", name, "--ttl", str(ttl)
    )
    output = unstyle(result.output)

    assert result.exit_code == 2, result.output
    assert "Invalid value for '--ttl'" in output
    assert not (world.config.settings.workspace_path / "ephemeral" / name).exists()


@pytest.mark.cli
def test_kb_create_ttl_zero_still_never_expires(cli_world):
    world = cli_world()
    name = "never-expires"
    path = world.config.settings.workspace_path / "ephemeral" / name

    result = world.cli(
        "kb", "create", "--ephemeral", "--name", name, "--ttl", "0"
    )
    assert result.exit_code == 0, result.output
    assert path.is_dir()

    gc_result = world.cli("kb", "gc")
    assert gc_result.exit_code == 0, gc_result.output
    assert path.is_dir()
