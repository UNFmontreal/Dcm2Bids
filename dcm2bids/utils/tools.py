# -*- coding: utf-8 -*-

"""This module checks whether a software is in PATH, for version, and for updates."""

import logging
import json
import time
from pathlib import Path
from urllib import error, request
from subprocess import getoutput
from shutil import which

from dcm2bids.version import __version__
from dcm2bids.utils.io import load_json, save_json

logger = logging.getLogger(__name__)

# How long a cached "latest version" is considered valid (seconds)
LATEST_VERSION_CACHE_TTL = 24 * 60 * 60  # 24 hours


def _version_cache_path(log_dir):
    """
    Return the path to the JSON file used to cache version check results
    inside the given log directory.
    """
    log_dir = Path(log_dir)
    return log_dir / "version_check.json"


def _load_version_cache(log_dir):
    """
    Load the JSON cache of previous version checks from the given log directory.
    """
    path = _version_cache_path(log_dir)
    if not path.exists():
        return {}
    try:
        return load_json(path)
    except Exception:
        logger.debug(
            "Failed to read version cache; ignoring corrupted cache.",
            exc_info=True,
        )
        return {}


def _save_version_cache(cache, log_dir) -> None:
    """
    Save the JSON cache of previous version checks to the given log directory.
    """
    path = _version_cache_path(log_dir)
    try:
        save_json(filename=path, data=cache)
    except Exception:
        logger.debug("Failed to write version cache; ignoring.", exc_info=True)


def _normalize_version(value):
    """
    Normalize a version string into a tuple of integer parts, when possible.

    - Strips a leading 'v' (e.g. 'v1.11.0' -> '1.11.0')
    - Splits on '.'
    - Converts each part to int if possible
    - Returns the original value if it cannot be parsed in a simple numeric form
    """
    if not isinstance(value, str):
        return value

    s = value.strip()
    if not s:
        return value

    # BIDS tag style: v1.2.3
    s = s.lstrip("v")

    parts = s.split(".")
    normalized = []
    for p in parts:
        p = p.strip()
        if not p:
            # Empty segment; treat as zero
            normalized.append(0)
            continue
        try:
            normalized.append(int(p))
        except ValueError:
            # If any part is not numeric, bail return the original string
            return value

    return tuple(normalized)


def _version_newer(latest, current):
    """
    Compare two versions, preferring normalized numeric comparison
    and falling back to string comparison.

    Returns True if `latest` is considered newer than `current`.
    """
    norm_latest = _normalize_version(latest)
    norm_current = _normalize_version(current)

    if isinstance(norm_latest, tuple) and isinstance(norm_current, tuple):
        # Padding to compare same length
        max_len = max(len(norm_latest), len(norm_current))
        norm_latest += (0,) * (max_len - len(norm_latest))
        norm_current += (0,) * (max_len - len(norm_current))
        return norm_latest > norm_current

    # Fallback: string comparison as before
    return str(latest) > str(current)


def is_tool(name):
    """ Check if a program is in PATH

    Args:
        name (string): program name
    Returns:
        boolean
    """
    return which(name) is not None


def has_internet(timeout=3):
    """
    Check if the machine appears to have internet access by trying to reach api.github.com.

    Returns:
        bool: True if an external host can be reached, False otherwise.
    """
    req = request.Request("https://api.github.com", method="HEAD")
    try:
        response = request.urlopen(req, timeout=timeout)
        status_ok = 200 <= response.getcode() < 400
        # Log at debug level to not spam
        logger.debug("has_internet status: %s", response.getcode())
        return status_ok

    except error.URLError as e:
        logger.warning(
            "No access to internet, GitHub or Read the Docs API. "
            "Check if there is an issue with your network/proxy/DNS. "
            "Skipping version check."
        )
        logger.debug("URLError: %s", e)
    except TimeoutError as e:
        logger.warning(
            "Timeout error, no access to internet or to GitHub or Read the Docs API: %s. "
            "Check if there is an issue with your network/proxy.",
            e,
        )
    return False


def check_github_latest(github_repo, timeout=3):
    """
    Check the latest version of a GitHub repository. Returns error if host can't be reached.
    Since has_internet() is used upstream, it would mean that host is unreachable but
    internet is ok.

    Args:
        github_repo (str): a GitHub repository ("username/repository")
        timeout (int): time in seconds

    Returns:
        str: latest release tag, or "unavailable" if the check could not be performed
    """
    req = request.Request(
        url=f"https://api.github.com/repos/{github_repo}/releases/latest"
    )
    try:
        response = request.urlopen(req, timeout=timeout)
    except error.HTTPError as e:
        logger.debug(
            "Could not reach GitHub to verify latest version of %s. "
            "Skipping version check. (HTTPError: %s)",
            github_repo,
            e,
        )
        return "unavailable"
    except Exception:
        # Any other unexpected error in this specific request.
        logger.debug(
            "Checking latest version of %s was not possible due to an unexpected error.",
            github_repo,
        )
        logger.debug(
            "Unexpected exception while querying GitHub latest release",
            exc_info=True,
        )
        return "unavailable"

    content = json.loads(response.read())
    return content.get("tag_name", "unavailable")


def check_latest(name="dcm2bids", log_dir=None):
    """Check if a new version of a software exists and log some details.
    Implemented for dcm2bids and dcm2niix.

    Args:
        name (str): name of the software
        log_dir (str or Path, optional): directory where logs are written.
            If provided, a small JSON cache of version checks is stored there.
    """
    data = {
        "dcm2bids": {
            "repo": "UNFmontreal/Dcm2Bids",
            "host": "https://github.com",
            "current": __version__,
        },
        "dcm2niix": {
            "repo": "rordenlab/dcm2niix",
            "host": "https://github.com",
            "current": dcm2niix_version,
        },
    }

    info = data.get(name)
    if info is None:
        logger.debug("Version check: unknown software name '%s'; skipping.", name)
        return

    repo = info["repo"]
    host = info["host"]
    current = info["current"]
    if callable(current):
        current = current()

    logger.debug(
        "Version check: name=%s, current=%s, repo=%s, log_dir=%s",
        name,
        current,
        repo,
        log_dir,
    )

    latest = None

    if log_dir is not None:
        # Try cache first
        cache = _load_version_cache(log_dir)
        cache_key = repo  # one entry per GitHub repo
        now = time.time()
        cached_entry = cache.get(cache_key)

        if isinstance(cached_entry, dict):
            ts = cached_entry.get("timestamp", 0)
            age = now - ts
            logger.debug(
                "Version check: found cached entry for %s (age=%.1fs, ttl=%ds)",
                cache_key,
                age,
                LATEST_VERSION_CACHE_TTL,
            )
            if age < LATEST_VERSION_CACHE_TTL:
                latest = cached_entry.get("latest", "unavailable")
                logger.debug(
                    "Version check: using cached latest=%s for %s", latest, name
                )
        else:
            logger.debug(
                "Version check: no cached entry for %s in %s", cache_key, log_dir
            )

        # If cache is missing/expired/unavailable, we may need to query GitHub.
        if latest is None or latest == "unavailable":
            logger.debug(
                "Version check: cache miss or unavailable for %s; checking internet.",
                name,
            )
            if not has_internet():
                logger.info(
                    "Skipping version check for %s (no internet and no valid cache).",
                    name,
                )
                return
            logger.debug(
                "Version check: internet OK; querying GitHub latest for %s", repo
            )
            latest = check_github_latest(repo)
            cache[cache_key] = {"latest": latest, "timestamp": now}
            _save_version_cache(cache, log_dir)
            logger.debug(
                "Version check: updated cache for %s with latest=%s", cache_key, latest
            )
    else:
        # No caching: one-off.
        logger.debug(
            "Version check: no log_dir provided for %s; performing one-off check.",
            name,
        )
        if not has_internet():
            logger.info("Skipping version check for %s (no internet).", name)
            return
        logger.debug(
            "Version check: internet OK; querying GitHub latest for %s", repo
        )
        latest = check_github_latest(repo)

    if latest == "unavailable":
        logger.info("Could not determine latest version of %s (unavailable).", name)
        return

    if _version_newer(latest, current):
        logger.warning("A newer version exists for %s: %s", name, latest)
        logger.warning("Consider updating it -> %s/%s.", host, repo)
    else:
        logger.info("Currently using the latest version of %s.", name)


def dcm2niix_version(name="dcm2niix"):
    """
    Check and raises an error if dcm2niix is not in PATH.
    Then check for the version installed.

    Returns:
        A string of the version of dcm2niix install on the system
    """
    if not is_tool(name):
        logger.error(f"{name} is not in your PATH or not installed.")
        logger.error("https://github.com/rordenlab/dcm2niix to troubleshoot.")
        raise FileNotFoundError(f"{name} is not in your PATH or not installed."
                                " -> https://github.com/rordenlab/dcm2niix"
                                " to troubleshoot.")

    try:
        output = getoutput("dcm2niix --version")
    except Exception:
        logger.exception("Checking dcm2niix version", exc_info=False)
        return
    else:
        return output.split()[-1]
