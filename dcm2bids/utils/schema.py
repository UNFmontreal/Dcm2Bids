import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error
import json

from dcm2bids.utils.io import load_json, save_json
import dcm2bids.utils.tools as tools
from dcm2bids.utils import schema_data

# Defaults for BIDS schema handling.
BIDS_SCHEMA_DEFAULT_VERSION = "v1.11.1"  # imported in DEFAULT
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
    schema_baseurl=BIDS_SCHEMA_BASEURL, schema_version=BIDS_SCHEMA_DEFAULT_VERSION
):
    """
    Build the URL to the precompiled BIDS schema JSON for a given BIDS version
    (e.g. 'stable', 'latest', 'v1.9.0').
    """
    return f"{schema_baseurl}/{schema_version}/schema.json"


def _download_schema(schema_version, baseurl=BIDS_SCHEMA_BASEURL):
    """
    Download BIDS schema JSON for a given version label from the official URL.

    This is a low-level primitive: it only performs HTTP + JSON parsing.
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
    except Exception:
        logger.warning(
            "Unexpected error while downloading BIDS schema (version=%s) from %s",
            schema_version,
            url,
        )
        logger.debug("Schema download exception:", exc_info=True)
        return None

    try:
        return json.loads(raw.decode())
    except Exception:
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
    cache = tools._load_version_cache(log_dir) if log_dir is not None else {}
    return cache.get("schema", {}), cache


def _save_schema_cache(schema_cache, full_cache, log_dir):
    """
    Update the 'schema' key and write back using tools' cache writer.
    """
    full_cache["schema"] = schema_cache
    tools._save_version_cache(full_cache, log_dir)


def _load_bundled_schema():
    """
    Load the schema that is bundled with dcm2bids.

    The JSON is packaged under `dcm2bids.utils.schema_data` as
    `bids_schema_<BIDS_SCHEMA_DEFAULT_VERSION>.json`, e.g.:

        dcm2bids/utils/schema_data/bids_schema_v1.11.1.json
    """
    filename = f"bids_schema_{BIDS_SCHEMA_DEFAULT_VERSION}.json"
    try:
        path = schema_data.file / filename
        with path.open("r", encoding="utf-8") as f:
            schema = json.load(f)
        logger.info(
            "Loaded bundled BIDS schema (version=%s) from %s.",
            BIDS_SCHEMA_DEFAULT_VERSION,
            path,
        )
        return schema
    except FileNotFoundError:
        logger.warning(
            "Bundled BIDS schema file not found for version=%s (expected at %s).",
            BIDS_SCHEMA_DEFAULT_VERSION,
            filename,
        )
        logger.debug("Bundled schema load FileNotFoundError:", exc_info=True)
    except Exception:
        logger.warning(
            "Failed to load bundled BIDS schema (version=%s).",
            BIDS_SCHEMA_DEFAULT_VERSION,
        )
        logger.debug("Bundled schema load exception:", exc_info=True)
    return None


def _get_schema(schema_version=BIDS_SCHEMA_DEFAULT_VERSION, log_dir=None):
    """
    Fetch the BIDS schema JSON for a given version label, with caching and fallback.

    Returns:
        dict or None
    """
    schema = None
    # TODO: reduce complexity of this very long and complex function.
    if schema_version == "bundled":
        return _load_bundled_schema()
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
                        logger.info(
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
            "run once with internet or use the 'bundled' schema or a pinned, "
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

    # 3) Fallback to bundled only if requested version == default
    if schema_version in (BIDS_SCHEMA_DEFAULT_VERSION,
                          f"v{BIDS_SCHEMA_DEFAULT_VERSION}"):
        logger.info(
            "Falling back to bundled BIDS schema for default version %s.",
            BIDS_SCHEMA_DEFAULT_VERSION,
        )
        schema = _load_bundled_schema()

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

    This is the schema-driven version of DEFAULT.auto_entities.
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


def load_schema_derived_defaults(
        schema_version=BIDS_SCHEMA_DEFAULT_VERSION,
        log_dir=None):
    """
    Helper that loads the BIDS schema and returns a small bundle
    of derived structures to integrate into DEFAULT.

    Returned dict includes:
      - 'entity_table_keys': Entity short names
      - 'auto_entities': schema-driven auto-entities (MRI datatypes)
    """
    schema = _get_schema(schema_version=schema_version, log_dir=log_dir)
    if schema is None:
        raise RuntimeError(
            f"Failed to load BIDS schema for version '{schema_version}'. "
            "This indicates a broken dcm2bids installation or an invalid "
            "schema_version override."
        )

    # All entities in schema order
    entity_table_keys_all = _get_entity_table_keys(schema)
    auto_entities = _get_auto_entities_from_schema(schema)
    # Entities for raw MRI datatypes only
    raw_mri_entity_table_keys = _get_raw_mri_entity_table_keys(schema)

    # Make raw MRI entities the default
    # makes it backward compatible with manual tables in default
    return {
        # default set
        "entity_table_keys": raw_mri_entity_table_keys,
        "auto_entities": auto_entities,
        # keep the full list available
        "all_entity_table_keys": entity_table_keys_all,
    }
