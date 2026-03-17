"""Utility helpers for Ezlo HA Cloud integration."""

import logging
from pathlib import Path

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

TRUSTED_PROXY_BLOCK = """
# Added by Ezlo HA Cloud integration for frpc reverse proxy
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 127.0.0.1
"""

TRUSTED_PROXY_ENTRY = "    - 127.0.0.1"


def _get_config_path(hass: HomeAssistant) -> Path:
    """Return the path to configuration.yaml."""
    return Path(hass.config.config_dir) / "configuration.yaml"


def _needs_trusted_proxy(config_text: str) -> str | None:
    """Check if configuration.yaml needs trusted proxy config.

    Returns:
        None if already configured, or the updated config text if changes needed.
    """
    # Check if use_x_forwarded_for and 127.0.0.1 trusted proxy are already set
    has_forwarded = "use_x_forwarded_for: true" in config_text or "use_x_forwarded_for: True" in config_text
    has_trusted = "127.0.0.1" in config_text and "trusted_proxies" in config_text

    if has_forwarded and has_trusted:
        return None

    lines = config_text.splitlines(keepends=True)
    new_lines = []
    i = 0
    found_http = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Find top-level "http:" block (not indented, not commented)
        if stripped == "http:" and not line[0].isspace() and not stripped.startswith("#"):
            found_http = True
            new_lines.append(line)
            i += 1

            # Collect existing http block lines (indented lines)
            while i < len(lines) and (lines[i].strip() == "" or lines[i][0].isspace()):
                new_lines.append(lines[i])
                i += 1

            # Add missing entries at the end of the http block
            if not has_forwarded:
                new_lines.append("  use_x_forwarded_for: true\n")
            if not has_trusted:
                new_lines.append("  trusted_proxies:\n")
                new_lines.append("    - 127.0.0.1\n")

            continue

        new_lines.append(line)
        i += 1

    # No http: block found at all — append the whole block
    if not found_http:
        new_lines.append(TRUSTED_PROXY_BLOCK)

    return "".join(new_lines)


def ensure_trusted_proxy_config(hass: HomeAssistant) -> bool:
    """Ensure configuration.yaml has trusted proxy settings for frpc.

    Returns True if changes were made (restart needed).
    """
    config_path = _get_config_path(hass)

    if not config_path.is_file():
        _LOGGER.warning("configuration.yaml not found at %s", config_path)
        return False

    config_text = config_path.read_text(encoding="utf-8")
    updated = _needs_trusted_proxy(config_text)

    if updated is None:
        _LOGGER.debug("Trusted proxy config already present in configuration.yaml")
        return False

    # Write updated config
    config_path.write_text(updated, encoding="utf-8")
    _LOGGER.info(
        "Updated configuration.yaml with trusted proxy settings for frpc. "
        "A restart is required for changes to take effect"
    )
    return True
