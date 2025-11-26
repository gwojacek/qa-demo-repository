"""Helper functions supporting pytest configuration.

This module keeps non-fixture utilities out of ``conftest.py`` so that file
contains only hooks and fixtures.
"""

import builtins
import logging
import os
import time
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

# ---- environment helpers ---------------------------------------------------


def load_selected_env() -> str:
    """Load environment variables from an env file based on ``ENV_TYPE``.

    Returns a formatted message that can be displayed in the pytest header.
    """

    env_type = os.environ.get("ENV_TYPE", "local")
    env_file = f"localconf_{env_type}.env"
    if not os.path.exists(env_file) and env_type != "local":
        env_file = "localconf_local.env"

    load_dotenv(find_dotenv(env_file), override=True)
    return f"\n=======\n[env] Loading environment: {env_file}\n=======\n"


# ---- printing helpers ------------------------------------------------------

_ORIG_PRINT = builtins.print


def print_and_log(*args, **kwargs):
    """Forward print calls to the logger so they appear with xdist."""

    msg = " ".join(str(a) for a in args)
    logging.getLogger("PRINT").info(msg)
    _ORIG_PRINT(*args, **kwargs)


def configure_print_logging() -> None:
    """Replace built-in ``print`` with a logger-backed version."""

    builtins.print = print_and_log


def restore_print_logging() -> None:
    """Restore the original built-in ``print`` function."""

    builtins.print = _ORIG_PRINT


# ---- artifacts -------------------------------------------------------------


def make_screenshot_path(item) -> Path:
    """Build a timestamped screenshot path under ``tests/artifacts``."""

    ts = time.strftime("%Y%m%d-%H%M%S")
    safe = item.nodeid.replace("::", "_").replace("/", "_")
    path = Path(item.config.rootpath, "tests", "artifacts", f"{ts}_{safe}.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
