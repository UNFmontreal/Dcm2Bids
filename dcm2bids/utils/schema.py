import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error

from dcm2bids.utils.io import load_json, save_json
import dcm2bids.utils.tools as tools
from dcm2bids.utils import schema_data
from dcm2bids.version import __BIDSversion__

# Defaults for BIDS schema handling.
BIDS_SCHEMA_BASEURL = "https://bids-specification.readthedocs.io/en"

SCHEMA_ALIAS_CACHE_TTL = 7 * 24 * 60 * 60  # 1 week

logger = logging.getLogger(__name__)


def _schema_file_path(schema_version, log_dir):
    """
    Path to the full schema JSON on disk, e.g.:
      log/bids_schema_v1.9.0.json
      log/bids_schema_stable.json
    """
    log_dir = Path(log_dir)
    safe_ver = str(schema_version).replace("/", "_")
    return log_dir / f"bids_schema_{safe_ver}.json"


def _build_schema_url(
    schema_baseurl=BIDS_SCHEMA_BASEURL, schema_version=__BIDSversion__
):
    """
    Build the URL to the precompiled BIDS schema JSON for a given BIDS version
    (e.g. 'stable', 'latest', 'v1.9.0').
    """
    return f"{schema_baseurl}/{schema_version}/schema.json"


def _download_schema(schema_version, baseurl=BIDS_SCHEMA_BASEURL):
    """
    Download BIDS schema JSON for a given version label from the official URL.

    Performs HTTP + JSON parsing.
    Caching, disk paths, and fallbacks are handled in _get_schema.

    Returns:
        dict or None
    """
    url = _build_schema_url(schema_baseurl=baseurl, schema_version=schema_version)
    logger.info("Downloading BIDS schema from %s", url)
    try:
        req = request.Request(
            url,
            # need the headers, otherwise not allowed by readthedocs
            headers={"User-Agent": "Mozilla/5.0 (compatible; Dcm2Bids/1.0)"},
        )
        with request.urlopen(req, timeout=3) as resp:
            raw = resp.read()
    except error.HTTPError as e:
        logger.warning(
            "Failed to download BIDS schema (version=%s) from %s: %s",
            schema_version,
            url,
            e,
        )
        return None
    try:
        return json.loads(raw.decode())
    except json.JSONDecodeError:
        logger.warning(
            "Downloaded schema for version %s is not valid JSON.", schema_version
        )
        logger.debug("Schema JSON decode error:", exc_info=True)
        return None


def _load_schema_cache(log_dir):
    """
    Reuse tools' version cache file as a generic JSON cache, and
    keep schema entries under a dedicated 'schema' key.
    """
    cache = tools.load_version_cache(log_dir) if log_dir is not None else {}
    return cache.get("schema", {}), cache


def _save_schema_cache(schema_cache, full_cache, log_dir):
    """
    Update the 'schema' key and write back using tools' cache writer.
    """
    full_cache["schema"] = schema_cache
    tools.save_version_cache(full_cache, log_dir)


def _load_default_schema():
    """
    Load the schema that is default with dcm2bids.

    The JSON is packaged under `dcm2bids.utils.schema_data` as
    `bids_schema_<__BIDSversion__>.json`.
    """
    filename = f"bids_schema_{__BIDSversion__}.json"
    try:
        path = schema_data.file / filename
        with path.open("r", encoding="utf-8") as f:
            schema = json.load(f)
        logger.info(
            "Loading default BIDS schema (version=%s) from %s.",
            __BIDSversion__,
            path,
        )
        return schema
    except FileNotFoundError:
        logger.warning(
            "default BIDS schema file not found for version=%s (expected at %s).",
            __BIDSversion__,
            filename,
        )
        logger.debug("default schema load FileNotFoundError:", exc_info=True)
    except (OSError, json.JSONDecodeError):
        logger.warning(
            "Failed to load default BIDS schema (version=%s).",
            __BIDSversion__,
        )
        logger.debug("default schema load exception:", exc_info=True)
    return None


def get_schema(schema_version=__BIDSversion__, log_dir=None):
    """
    Fetch the BIDS schema JSON for a given version label, with caching and fallback.

    Returns:
        dict or None
    """
    schema = None
    # TODO: reduce complexity of this very long and complex function.
    if schema_version == "default":
        return _load_default_schema()
    is_alias = str(schema_version) in {"stable", "latest"}

    # If no log_dir, we can still download but won't persist cache metadata or files.
    schema_cache, full_cache = _load_schema_cache(log_dir) if log_dir else ({}, {})

    # 1) Cache lookup: metadata -> load from file if present (with TTL for aliases)
    cached_entry = schema_cache.get(schema_version)
    cached_schema_path = None
    cache_fresh = False

    if isinstance(cached_entry, dict):
        schema_path_str = cached_entry.get("path")
        bids_ver = cached_entry.get("bids_version")
        ts_str = cached_entry.get("timestamp")
        now = time.time()

        if is_alias and ts_str:
            try:
                ts_dt = datetime.fromisoformat(ts_str)
                age = now - ts_dt.timestamp()
                cache_fresh = age < SCHEMA_ALIAS_CACHE_TTL
                logger.debug(
                    "Schema cache: alias '%s' cached at %s "
                    "(age=%.1fs, fresh=%s, ttl=%ds)",
                    schema_version,
                    ts_str,
                    age,
                    cache_fresh,
                    SCHEMA_ALIAS_CACHE_TTL,
                )
            except Exception:
                logger.debug(
                    "Failed to parse schema cache timestamp '%s' for %s",
                    ts_str,
                    schema_version,
                    exc_info=True,
                )

        if schema_path_str:
            schema_path = Path(schema_path_str)
            if schema_path.exists():
                cached_schema_path = schema_path
                # For fixed versions, always try cache. For aliases, only if fresh.
                if not is_alias or cache_fresh:
                    try:
                        schema = load_json(schema_path)
                        logger.debug(
                            "Using cached BIDS schema for version '%s' from %s.",
                            schema_version,
                            schema_path,
                        )
                        # If we didn't have bids_version recorded (old cache),
                        # update it now and ensure timestamp is set.
                        if log_dir is not None:
                            changed = False
                            if bids_ver is None:
                                cached_entry["bids_version"] = schema.get(
                                    "bids_version"
                                )
                                changed = True
                            if not cached_entry.get("timestamp"):
                                cached_entry["timestamp"] = datetime.now(
                                    timezone.utc
                                ).replace(microsecond=0).isoformat()
                                changed = True
                            if changed:
                                schema_cache[schema_version] = cached_entry
                                _save_schema_cache(schema_cache, full_cache, log_dir)
                        return schema
                    except Exception:
                        logger.debug(
                            "Failed to load cached schema JSON from %s; "
                            "will try re-download.",
                            schema_path,
                            exc_info=True,
                        )

    if tools.has_internet():
        schema = _download_schema(schema_version)
        if schema is not None and log_dir is not None:
            # Write full schema to its own file in log dir
            schema_path = _schema_file_path(schema_version, log_dir)
            try:
                save_json(filename=schema_path, data=schema)
                logger.info(
                    "Saved BIDS schema for version '%s' to %s.",
                    schema_version,
                    schema_path,
                )
            except Exception:
                logger.debug(
                    "Failed to write schema JSON to %s; cache metadata will "
                    "still be updated but file-based cache is missing.",
                    schema_path,
                    exc_info=True,
                )
                schema_path = None

            # Store metadata in version_check.json under "schema"
            schema_cache[schema_version] = {
                "path": str(schema_path) if schema_path is not None else None,
                "bids_version": schema.get("bids_version"),
                "timestamp": datetime.now(timezone.utc)
                .replace(microsecond=0)
                .isoformat(),
            }
            _save_schema_cache(schema_cache, full_cache, log_dir)
        if schema is not None:
            return schema

        if is_alias and cached_schema_path is not None:
            try:
                logger.info(
                    "Failed to refresh '%s' schema from internet; "
                    "falling back to previously cached file at %s.",
                    schema_version,
                    cached_schema_path,
                )
                schema = load_json(cached_schema_path)
                return schema
            except Exception:
                logger.debug(
                    "Fallback to cached alias schema at %s failed.",
                    cached_schema_path,
                    exc_info=True,
                )
    else:
        logger.info(
            "No internet connection; cannot download BIDS schema (version=%s) "
            "from %s. If this is your first run with this label, you must either "
            "run once with internet or use the 'default' schema or a pinned, "
            "previously-cached version.",
            schema_version,
            BIDS_SCHEMA_BASEURL,
        )
        # If offline and there is a cached file (alias or not), try to use it.
        if cached_schema_path is not None:
            try:
                logger.info(
                    "Using previously cached BIDS schema for version '%s' from %s "
                    "while offline.",
                    schema_version,
                    cached_schema_path,
                )
                schema = load_json(cached_schema_path)
                return schema
            except Exception:
                logger.debug(
                    "Failed to load cached schema JSON from %s while offline.",
                    cached_schema_path,
                    exc_info=True,
                )

    # 3) Fallback to default only if requested version == default
    if schema_version in (__BIDSversion__,
                          f"v{__BIDSversion__}"):
        logger.info(
            "Falling back to default BIDS schema for default version %s.",
            __BIDSversion__,
        )
        schema = _load_default_schema()

    if schema is None:
        logger.debug("BIDS schema: no schema loaded (version=%s)", schema_version)
    return schema


def _get_entities_ordered(schema):
    """
    Return the list of entity definitions ordered according to `rules.entities`.

    Each item is one of the entries from `schema['objects']['entities']`.
    """
    entities = schema["objects"]["entities"]
    entities_order = schema["rules"]["entities"]
    return [entities[key] for key in entities_order]


def _get_entity_table_keys(schema):
    """
    Return the list of entity short names,
    ordered according to `rules.entities`.

    This is the schema-driven version of former DEFAULT.entityTableKeys.
    """

    ordered_entities = _get_entities_ordered(schema)
    return [ent["name"] for ent in ordered_entities]


def _get_raw_mri_entity_table_keys(schema):
    """
    Return ordered entity short names that are actually used
    in the raw MRI datatype rules.

    This is like `_get_entity_table_keys`, but restricted to entities that
    are referenced in `rules.files['raw']` for MRI datatypes.

    Note: A small quirk for (datatype == 'task') *only* when
    they target MRI datatypes, so that entities like 'rec' that appear
    in task timeseries__* rules for MRI are included.
    """
    rules = schema["rules"]
    raw_rules = rules["files"].get("raw", {})
    mri_datatypes = _get_mri_datatypes(schema)

    # Collect schema-level entity *keys* that appear in raw MRI rules
    used_schema_entities = set()

    for datatype, groups in raw_rules.items():
        if datatype in mri_datatypes:
            for spec in groups.values():
                for ent_key in (spec.get("entities") or {}):
                    used_schema_entities.add(ent_key)

        # Task rules that target MRI datatypes (timeseries__*)
        if datatype == "task":
            for spec in groups.values():
                target_dts = spec.get("datatypes", [])
                if all(dt not in mri_datatypes for dt in target_dts):
                    continue
                for ent_key in (spec.get("entities") or {}):
                    used_schema_entities.add(ent_key)

    # Walk rules.entities in order, but keep only those used in raw MRI
    entities = schema["objects"]["entities"]
    ordered_schema_keys = rules["entities"]

    ordered_entities = [
        entities[key]
        for key in ordered_schema_keys
        if key in used_schema_entities
    ]
    return [ent["name"] for ent in ordered_entities]


def _get_schema_to_bids_entity_map(schema):
    """
    Build mapping from schema entity key (used in rules) -> short entity names
    used in filenames, e.g., 'acquisition' -> 'acq', 'direction' -> 'dir'.
    """
    entities = schema["objects"]["entities"]
    return {schema_key: ent_def["name"] for schema_key, ent_def in entities.items()}


def _get_mri_datatypes(schema):
    """
    Return the list of MRI-related datatypes defined in the schema.

    This follows `rules.modalities['mri']['datatypes']`
    """
    rules = schema["rules"]
    mri = rules["modalities"].get("mri", {})
    datatypes = list(mri.get("datatypes", []))


    return datatypes


def _get_auto_entities_from_schema(schema):
    """
    Derive the 'auto entities' mapping from the schema.

    Keys look like 'anat_VFA', 'func_bold', 'fmap_epi', etc.
    Values are lists of entity short names (e.g. ['task'], ['dir'], ['flip', 'mt']).

    This is the schema-driven version of former DEFAULT.auto_entities.
    """
    raw_rules = schema["rules"]["files"]['raw']

    schema_to_bids = _get_schema_to_bids_entity_map(schema)
    mri_datatypes = _get_mri_datatypes(schema) 

    # Quirk: Add task into the list if it's not explicitly listed.
    mri_datatypes_with_task = mri_datatypes + ["task"]


    auto_required_entities = {}

    # Loop over datatype groups
    for datatype, groups in raw_rules.items():
        # Skip non-mri datatype
        if datatype not in mri_datatypes_with_task:
            continue

        for group_name, spec in groups.items():
            ent_spec = spec.get("entities", {})

            # don't keep 'subject' as is mandatory for all of them
            required_schema_entities = [
                key
                for key, requirement in ent_spec.items()
                if requirement == "required" and key != "subject"
            ]
            if not required_schema_entities:
                continue

            # Map schema keys -> BIDS abbreviations via schema_to_bids
            required_bids_entities = [
                schema_to_bids[key]
                for key in required_schema_entities
                if key in schema_to_bids
            ]
            if not required_bids_entities:
                continue

            suffixes = spec.get("suffixes", [])
            target_datatypes = spec.get("datatypes", [datatype])

            if datatype != "task":
                # For "plain" MRI datatypes (anat/func/fmap/perf/dwi/pet...),
                # keep same behavior (eg, anat_MP2RAGE)
                for suffix in suffixes:
                    key = f"{datatype}_{suffix}"
                    auto_required_entities[key] = required_bids_entities
            else:
                # task-* rules are trickier (timeseries__*) applicable to multiple
                # datatypes, so keys per *target* datatype, (eg anat_physio)
                for target_dt in target_datatypes:
                    if target_dt not in mri_datatypes_with_task:
                        continue
                    for suffix in suffixes:
                        key = f"{target_dt}_{suffix}"
                        auto_required_entities[key] = required_bids_entities

    return auto_required_entities


def derive_entities_from_schema(schema):
    """
    Helper that loads the BIDS schema and returns a small bundle
    of derived structures to integrate into DEFAULT.

    Returned dict includes:
      - 'raw_mri_entity_table_keys': Entity short names in order for MRI only
      - 'auto_entities': schema-driven auto-entities (MRI datatypes)
    """
    if schema is None:
        raise RuntimeError(
            f"Failed to load BIDS schema for version '{schema['bids_version']}'."
            "This indicates a broken dcm2bids installation or an invalid "
            "schema_version override."
        )

    # All entities in schema order
    auto_entities = _get_auto_entities_from_schema(schema)
    # Entities for raw MRI datatypes only
    raw_mri_entity_table_keys = _get_raw_mri_entity_table_keys(schema)

    # Make raw MRI entities the default
    # makes it backward compatible with manual tables in default
    return {
        # default set
        "entity_table_keys": raw_mri_entity_table_keys,
        "auto_entities": auto_entities
    }

def _resolve_bids_version_label(args_bids_version, log_dir):
    """
    Decide which schema label to use and log messages.
    Returns the actual label in used (e.g. 'default', 'stable', 'v1.11.1', etc)
    """
    if args_bids_version is None:
        default_version = __BIDSversion__
        logger.info(
            "No --bids_version provided; using 'default' BIDS spec (version=%s) "
            "for reproducible behavior.",
            default_version,
        )
        
        # Simplest place to check when default is used
        if tools.has_internet():
            _check_latest_stable(default_version, log_dir)

        return "default"

    logger.info(
        "Specific BIDS version requested via --bids_version=%s",
        args_bids_version,
    )

    if args_bids_version == "latest":
        logger.warning(
            "You requested BIDS version 'latest'. This typically tracks the "
            "current development version of the BIDS specification and may be "
            "unstable or change without notice. For reproducible pipelines, "
            "consider using a fixed version tag (e.g. 'v1.11.1') or 'default'."
        )
    elif args_bids_version == "stable":
        logger.info(
            "You requested BIDS version 'stable'. This label may point to "
            "different BIDS releases over time. For reproducible pipelines, "
            "consider using a fixed version tag (e.g. 'v1.11.1') or 'default'."
        )

    return args_bids_version


def _check_latest_stable(version, log_dir):
    """
    If possible, check remote 'stable' and suggest upgrading if newer.
    """
    logger.info("Checking for BIDS update")
    logger.debug(
        "Checking remote 'stable' BIDS spec to see if a newer version "
        "is available."
    )
    stable_schema = get_schema(schema_version="stable", log_dir=log_dir)
    stable_version = None
    if stable_schema is not None:
        stable_version = stable_schema.get("bids_version", "stable")

    if isinstance(stable_version, str):
        logger.debug(
            "default BIDS version: %s; remote 'stable' version: %s",
            version,
            stable_version,
        )
        if tools.version_newer(stable_version, version):
            logger.warning(
                "A newer 'stable' BIDS specification (%s) is available than the "
                "default version (%s). The default schema is still used "
                "for this run. Consider updating using "
                "--bids_version %s.",
                stable_version,
                version,
                stable_version,
            )
        else:
            logger.info("Using latest stable BIDS specification.")
    else:
        logger.info(
            "Could not determine version for 'stable'; "
            "continuing with default BIDS specification (%s).",
            version,
        )


def _abort_if_schema_missing(schema_version, schema):
    """
    Centralized error logging + exit when schema cannot be loaded.
    """
    if schema is not None:
        return
    # Be explicit so users know how to recover, aborting so user actually reads the log ;)
    logger.error(
        "Failed to load BIDS schema for '%s'. If you are running offline and "
        "this label has never been used before on this machine, there may be "
        "no cached file available.",
        schema_version,
    )
    logger.error(
        "To proceed offline, either:\n"
        "  * Run once with internet so the schema for '%s' can be cached, or\n"
        "  * Use the default schema without using '--bids_version', or\n",
        "  * Use the default schema with using '--bids_version default', or\n"
        "  * Pin to a specific BIDS version tag that is already cached.",
        schema_version,
    )
    logger.error(
        "BIDS version '%s' could not be found; verify the version provided.",
        schema_version,
    )
    logger.error(
        "dcm2bids cannot continue without a valid BIDS version. Aborting."
    )
    raise SystemExit(1)



def load_schema(args_bids_version, log_dir):
    """
    Helper to resolve and load the requested BIDS schema version for the current run.
    This function decides which BIDS version label to use, checks for updates, and
    aborts if the schema cannot be loaded.

    Args:
        args_bids_version: BIDS version label requested by the user.
        log_dir: Directory used for caching schema files and version checks.

    Returns:
        dict: Loaded BIDS schema JSON corresponding to the actual version label.

    Raises:
        SystemExit: If no valid BIDS schema can be loaded for the requested label.
    """
    actual_label = _resolve_bids_version_label(args_bids_version, log_dir)

    schema = get_schema(schema_version=actual_label, log_dir=log_dir)
    _abort_if_schema_missing(actual_label, schema)
    derived = derive_entities_from_schema(schema)

    return schema, derived