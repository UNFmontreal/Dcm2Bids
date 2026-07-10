import json
from datetime import datetime, timedelta, timezone

import pytest

from dcm2bids.utils.tools import normalize_version, version_newer
from dcm2bids.utils import schema as schema_mod
from dcm2bids.utils.schema import (
    get_schema,
    load_schema,
    _get_raw_mri_entity_table_keys,
    _get_auto_entities_from_schema,
)
from dcm2bids.utils.utils import DEFAULT
from dcm2bids.version import __BIDSversion__


@pytest.mark.parametrize(
    "raw, expected",
    [
        # BIDS version tags
        ("v1.11.1", (1, 11, 1)),
        ("1.11.1", (1, 11, 1)),
        ("v1.2.0", (1, 2, 0)),
        ("1.2.0", (1, 2, 0)),
        # dcm2bids tags: major.minor.patch
        ("3.2.0", (3, 2, 0)),
        ("v3.2.0", (3, 2, 0)),
        # dcm2niix-like tags: date-style versions
        ("v1.0.20260416", (1, 0, 20260416)),
        ("1.0.20240229", (1, 0, 20240229)),
        # Extra whitespace
        ("  v1.2.3  ", (1, 2, 3)),
        # Leading "v" is ignored, shorter tuples are allowed
        ("v1", (1,)),
        ("1", (1,)),
        ("1.2", (1, 2)),
        ("01.002.0003", (1, 2, 3)),
        # Empty segments are treated as zero
        ("1..2", (1, 0, 2)),
        (".1", (0, 1)),
        ("1.", (1, 0)),
        # Unparsable versions: fall back to string comparison
        ("dev", "dev"),
        ("1.11.1-rc1", "1.11.1-rc1"),
        ("v1.11.1-rc1", "v1.11.1-rc1"),
        ("1.2.0-dev", "1.2.0-dev"),
        ("stable", "stable"),
        ("latest", "latest"),
    ],
)
def test_normalize_version(raw, expected):
    assert normalize_version(raw) == expected


@pytest.mark.parametrize(
    "latest, current, expected",
    [
        # dcm2bids tags
        ("3.2.0", "3.1.5", True),
        ("v3.2.0", "3.1.5", True),
        ("3.2.0", "v3.2.0", False),
        ("v3.2.0", "v3.2.0", False),

        # dcm2niix tags
        ("v1.0.20260416", "v1.0.20210101", True),
        ("1.0.20260416", "1.0.20210101", True),
        ("v1.0.20210101", "v1.0.20260416", False),

        # BIDS tags
        ("v1.11.1", "v1.9.0", True),
        ("1.11.1", "1.9.0", True),
        ("1.11.1", "1.11.0", True),
        ("1.11.0", "1.11.1", False),

        # Leading v ---
        ("v1.2.3", "1.2.3", False),
        ("1.2.3", "v1.2.2", True),

        # For these, we just assert that behavior is consistent, not that it
        # encodes SemVer semantics.
        ("v1.2.0", "v1.2.0-dev", False),
        ("v1.2.0-dev", "v1.2.0", True),
        ("1.11.1-dev", "1.11.1", True),   # "1.11.1-dev" > "1.11.1" lexicographically
        ("1.11.1", "1.11.1-dev", False),
        ("1.11.1-rc1", "1.11.1", True),
        ("1.11.1", "1.11.1-rc1", False),
        ("1.11.1-rc2", "1.11.1-rc1", True),
        ("1.11.1-rc1", "1.11.1-rc2", False)
    ],
)
def test_version_newer(latest, current, expected):
    """
    version_newer should:
      * Treat tags we actually use (dcm2bids, dcm2niix, BIDS) sensibly.
      * Use numeric comparison when both normalize cleanly.
      * Pad shorter tuples with zeros.
      * Fall back to string comparison for non‑numeric tags (dev, rc, stable, latest).
    """
    assert version_newer(latest, current) is expected


def test_get_schema_default_calls_loader(monkeypatch):
    """
    When schema_version='default', get_schema should delegate directly to
    _load_default_schema and return exactly what it yields.
    """
    called = {"count": 0}
    fake_schema = {"bids_version": "vX.Y.Z", "dummy": True}

    def fake_load_default():
        called["count"] += 1
        return fake_schema

    monkeypatch.setattr(schema_mod, "_load_default_schema", fake_load_default)

    result = get_schema(schema_version="default", log_dir=None)

    assert called["count"] == 1
    assert result is fake_schema


def test_get_schema_default_returns_none_if_loader_fails(monkeypatch):
    """
    If _load_default_schema returns None, get_schema('default') should
    also return None and not raise. The caller decides if this is fatal.
    """
    def fake_load_default():
        return None

    monkeypatch.setattr(schema_mod, "_load_default_schema", fake_load_default)

    result = get_schema(schema_version="default", log_dir=None)
    assert result is None


def test_get_schema_default_online_uncached_downloads_and_caches(monkeypatch, tmp_path):
    """
    When requesting the default schema version with internet and no cache:
      * _download_schema is called with the default version
      * schema JSON is written to bids_schema_<version>.json in log_dir
      * schema cache metadata is updated via _save_schema_cache
      * the downloaded schema is returned
    """
    log_dir = tmp_path / "log"
    log_dir.mkdir()

    fake_schema = {"bids_version": __BIDSversion__, "from": "download"}
    downloaded = {"called": False}
    saved_cache = {"cache": None, "full": None, "log_dir": None}
    saved_path = {"path": None}

    def fake_has_internet(timeout=3):
        return True

    def fake_download_schema(version, baseurl=schema_mod.BIDS_SCHEMA_BASEURL):
        downloaded["called"] = True
        assert version == __BIDSversion__
        return fake_schema

    def fake_schema_file_path(schema_version, ld):
        # ensure we use our tmp log_dir
        assert ld == log_dir
        path = log_dir / f"bids_schema_{schema_version}.json"
        saved_path["path"] = path
        return path

    def fake_load_schema_cache(ld):
        # No prior schema cache
        assert ld == log_dir
        return {}, {}

    def fake_save_schema_cache(schema_cache, full_cache, ld):
        saved_cache["cache"] = schema_cache
        saved_cache["full"] = full_cache
        saved_cache["log_dir"] = ld

    monkeypatch.setattr(schema_mod.tools, "has_internet", fake_has_internet)
    monkeypatch.setattr(schema_mod, "_download_schema", fake_download_schema)
    monkeypatch.setattr(schema_mod, "_schema_file_path", fake_schema_file_path)
    monkeypatch.setattr(schema_mod, "_load_schema_cache", fake_load_schema_cache)
    monkeypatch.setattr(schema_mod, "_save_schema_cache", fake_save_schema_cache)

    # Use the real save_json/load_json to verify file round-trip
    result = get_schema(schema_version=__BIDSversion__, log_dir=log_dir)

    assert downloaded["called"] is True
    assert result == fake_schema
    # schema file was written
    assert saved_path["path"] is not None
    assert saved_path["path"].exists()
    # cache metadata stored for this version
    assert __BIDSversion__ in saved_cache["cache"]
    entry = saved_cache["cache"][__BIDSversion__]
    assert entry["bids_version"] == __BIDSversion__
    # timestamp is set
    assert isinstance(entry.get("timestamp"), str)


def test_get_schema_default_online_cached_uses_cache(monkeypatch, tmp_path):
    """
    When requesting the default schema with internet and an existing cache entry:
      * cached file is loaded and returned
      * _download_schema is not called
    """
    log_dir = tmp_path / "log"
    log_dir.mkdir()

    # Prepare a fake cached schema file
    cached_schema = {"bids_version": __BIDSversion__, "from": "cache"}
    schema_path = log_dir / f"bids_schema_{__BIDSversion__}.json"
    schema_path.write_text(json.dumps(cached_schema), encoding="utf-8")

    def fake_has_internet(timeout=3):
        return True

    def fake_download_schema(version, baseurl=schema_mod.BIDS_SCHEMA_BASEURL):
        raise AssertionError("_download_schema should not be called when cache is valid")

    def fake_load_schema_cache(ld):
        assert ld == log_dir
        return (
            {
                __BIDSversion__: {
                    "path": str(schema_path),
                    "bids_version": __BIDSversion__,
                    "timestamp": None,  # simulate old cache w/o timestamp
                }
            },
            {},
        )

    saved_cache = {}

    def fake_save_schema_cache(schema_cache, full_cache, ld):
        saved_cache["schema_cache"] = schema_cache
        saved_cache["full_cache"] = full_cache
        saved_cache["log_dir"] = ld

    monkeypatch.setattr(schema_mod.tools, "has_internet", fake_has_internet)
    monkeypatch.setattr(schema_mod, "_download_schema", fake_download_schema)
    monkeypatch.setattr(schema_mod, "_load_schema_cache", fake_load_schema_cache)
    monkeypatch.setattr(schema_mod, "_save_schema_cache", fake_save_schema_cache)

    result = get_schema(schema_version=__BIDSversion__, log_dir=log_dir)
    assert result == cached_schema

    # cache should have been updated with timestamp (and keep bids_version)
    assert saved_cache["schema_cache"][__BIDSversion__]["bids_version"] == __BIDSversion__
    assert isinstance(
        saved_cache["schema_cache"][__BIDSversion__]["timestamp"], str
    )


def test_get_schema_default_offline_with_cache(monkeypatch, tmp_path):
    """
    When offline with a cached schema file:
      * cached file is used
      * no download attempt is made
    """
    log_dir = tmp_path / "log"
    log_dir.mkdir()

    cached_schema = {"bids_version": __BIDSversion__, "from": "offline-cache"}
    schema_path = log_dir / f"bids_schema_{__BIDSversion__}.json"
    schema_path.write_text(json.dumps(cached_schema), encoding="utf-8")

    def fake_has_internet(timeout=3):
        return False

    def fake_load_schema_cache(ld):
        assert ld == log_dir
        return (
            {
                __BIDSversion__: {
                    "path": str(schema_path),
                    "bids_version": __BIDSversion__,
                    "timestamp": None,
                }
            },
            {},
        )

    monkeypatch.setattr(schema_mod.tools, "has_internet", fake_has_internet)
    monkeypatch.setattr(schema_mod, "_load_schema_cache", fake_load_schema_cache)

    result = get_schema(schema_version=__BIDSversion__, log_dir=log_dir)
    assert result == cached_schema


def test_get_schema_default_offline_without_cache_falls_back_to_default(
    monkeypatch, tmp_path
):
    """
    When offline, no cache exists, and the requested version equals the default:
      * _load_default_schema is used as a fallback
      * the default schema is returned
    """
    log_dir = tmp_path / "log"
    log_dir.mkdir()

    def fake_has_internet(timeout=3):
        return False

    def fake_load_schema_cache(ld):
        assert ld == log_dir
        return {}, {}

    default_called = {"called": False}
    default_schema = {
        "bids_version": __BIDSversion__,
        "from": "default-fallback",
    }

    def fake_load_default_schema():
        default_called["called"] = True
        return default_schema

    monkeypatch.setattr(schema_mod.tools, "has_internet", fake_has_internet)
    monkeypatch.setattr(schema_mod, "_load_schema_cache", fake_load_schema_cache)
    monkeypatch.setattr(schema_mod, "_load_default_schema", fake_load_default_schema)

    result = get_schema(schema_version=__BIDSversion__, log_dir=log_dir)
    assert default_called["called"] is True
    assert result == default_schema


def test_get_schema_alias_fresh_cache_uses_cache(monkeypatch, tmp_path):
    """
    For alias labels like 'stable':
      * If cache entry exists and is fresh, get_schema should return cached
        schema and not attempt a download.
    """
    log_dir = tmp_path / "log"
    log_dir.mkdir()

    schema_version = "stable"
    cached_schema = {"bids_version": "v1.11.1", "from": "alias-fresh-cache"}
    schema_path = log_dir / f"bids_schema_{schema_version}.json"
    schema_path.write_text(json.dumps(cached_schema), encoding="utf-8")

    # Fresh timestamp: now
    now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    def fake_has_internet(timeout=3):
        # Even if we report internet, fresh cache should short-circuit.
        return True

    def fake_load_schema_cache(ld):
        assert ld == log_dir
        return (
            {
                schema_version: {
                    "path": str(schema_path),
                    "bids_version": cached_schema["bids_version"],
                    "timestamp": now_iso,
                }
            },
            {},
        )

    def fake_download_schema(version, baseurl=schema_mod.BIDS_SCHEMA_BASEURL):
        raise AssertionError("_download_schema must not be called for fresh alias cache")

    monkeypatch.setattr(schema_mod.tools, "has_internet", fake_has_internet)
    monkeypatch.setattr(schema_mod, "_load_schema_cache", fake_load_schema_cache)
    monkeypatch.setattr(schema_mod, "_download_schema", fake_download_schema)

    result = get_schema(schema_version=schema_version, log_dir=log_dir)
    assert result == cached_schema


def test_get_schema_alias_stale_cache_downloads_and_updates(monkeypatch, tmp_path):
    """
    For alias labels like 'stable':
      * If cache entry exists but is stale, get_schema should attempt to
        re-download from the internet.
      * On successful download, it should return the new schema and update
        the cache metadata.
    """
    log_dir = tmp_path / "log"
    log_dir.mkdir()

    schema_version = "stable"
    old_schema = {"bids_version": "v1.10.0", "from": "alias-stale-cache"}
    new_schema = {"bids_version": "v1.11.1", "from": "alias-download"}

    schema_path = log_dir / f"bids_schema_{schema_version}.json"
    schema_path.write_text(json.dumps(old_schema), encoding="utf-8")

    # Stale: set timestamp far in the past
    old_ts = (datetime.now(timezone.utc) - timedelta(days=30)).replace(microsecond=0).isoformat()

    def fake_has_internet(timeout=3):
        return True

    download_called = {"called": False}

    def fake_download_schema(version, baseurl=schema_mod.BIDS_SCHEMA_BASEURL):
        download_called["called"] = True
        assert version == schema_version
        return new_schema

    def fake_load_schema_cache(ld):
        assert ld == log_dir
        return (
            {
                schema_version: {
                    "path": str(schema_path),
                    "bids_version": old_schema["bids_version"],
                    "timestamp": old_ts,
                }
            },
            {},
        )

    saved_cache = {}

    def fake_save_schema_cache(schema_cache, full_cache, ld):
        saved_cache["schema_cache"] = schema_cache
        saved_cache["full_cache"] = full_cache
        saved_cache["log_dir"] = ld

    # Let _schema_file_path compute where to write, but ensure it's in log_dir
    def fake_schema_file_path(ver, ld):
        assert ver == schema_version
        assert ld == log_dir
        return log_dir / f"bids_schema_{ver}.json"

    monkeypatch.setattr(schema_mod.tools, "has_internet", fake_has_internet)
    monkeypatch.setattr(schema_mod, "_download_schema", fake_download_schema)
    monkeypatch.setattr(schema_mod, "_load_schema_cache", fake_load_schema_cache)
    monkeypatch.setattr(schema_mod, "_save_schema_cache", fake_save_schema_cache)
    monkeypatch.setattr(schema_mod, "_schema_file_path", fake_schema_file_path)

    result = get_schema(schema_version=schema_version, log_dir=log_dir)
    assert download_called["called"] is True
    assert result == new_schema

    # cache metadata updated to new bids_version and has a timestamp
    entry = saved_cache["schema_cache"][schema_version]
    assert entry["bids_version"] == new_schema["bids_version"]
    assert isinstance(entry["timestamp"], str)


def test_get_schema_alias_stale_cache_download_fails_falls_back_to_cache(
    monkeypatch, tmp_path
):
    """
    For alias labels like 'stable':
      * If cache entry exists but is stale and download fails, _get_schema
        should fall back to the cached schema file.
    """
    log_dir = tmp_path / "log"
    log_dir.mkdir()

    schema_version = "stable"
    cached_schema = {"bids_version": "v1.10.0", "from": "alias-stale-cache-fallback"}
    schema_path = log_dir / f"bids_schema_{schema_version}.json"
    schema_path.write_text(json.dumps(cached_schema), encoding="utf-8")

    old_ts = (datetime.now(timezone.utc) - timedelta(days=30)).replace(microsecond=0).isoformat()

    def fake_has_internet(timeout=3):
        return True

    def fake_download_schema(version, baseurl=schema_mod.BIDS_SCHEMA_BASEURL):
        assert version == schema_version
        # Simulate remote failure
        return None

    def fake_load_schema_cache(ld):
        assert ld == log_dir
        return (
            {
                schema_version: {
                    "path": str(schema_path),
                    "bids_version": cached_schema["bids_version"],
                    "timestamp": old_ts,
                }
            },
            {},
        )

    monkeypatch.setattr(schema_mod.tools, "has_internet", fake_has_internet)
    monkeypatch.setattr(schema_mod, "_download_schema", fake_download_schema)
    monkeypatch.setattr(schema_mod, "_load_schema_cache", fake_load_schema_cache)

    result = get_schema(schema_version=schema_version, log_dir=log_dir)
    assert result == cached_schema


def test_get_schema_alias_offline_with_and_without_cache(monkeypatch, tmp_path):
    """
    Offline behavior for alias labels:
      * If a cached file exists, it should be used.
      * If no cached file, returns None.
    """
    log_dir = tmp_path / "log"
    log_dir.mkdir()
    schema_version = "stable"

    # Case 1: with cache
    cached_schema = {"bids_version": "v1.10.0", "from": "alias-offline-cache"}
    schema_path = log_dir / f"bids_schema_{schema_version}.json"
    schema_path.write_text(json.dumps(cached_schema), encoding="utf-8")

    def fake_has_internet(timeout=3):
        return False

    def fake_load_schema_cache_with(ld):
        assert ld == log_dir
        return (
            {
                schema_version: {
                    "path": str(schema_path),
                    "bids_version": cached_schema["bids_version"],
                    "timestamp": None,
                }
            },
            {},
        )

    monkeypatch.setattr(schema_mod.tools, "has_internet", fake_has_internet)
    monkeypatch.setattr(schema_mod, "_load_schema_cache", fake_load_schema_cache_with)

    result_with = get_schema(schema_version=schema_version, log_dir=log_dir)
    assert result_with == cached_schema

    # Case 2: without cache
    def fake_load_schema_cache_without(ld):
        assert ld == log_dir
        return {}, {}

    monkeypatch.setattr(schema_mod, "_load_schema_cache", fake_load_schema_cache_without)

    result_without = get_schema(schema_version=schema_version, log_dir=log_dir)
    assert result_without is None


def test_derive_entities_from_schema_entity_table_keys_non_empty():
    """
    derive_entities_from_schema should return a non-empty list of
    entity_table_keys, and it should at least contain core entities
    like 'sub', 'ses', and 'run' that are required by the BIDS spec.
    """
    schema, derived = load_schema(None, None)
    entity_keys = derived["entity_table_keys"]

    assert isinstance(entity_keys, list)
    assert len(entity_keys) > 0

    # Basic sanity: these entities exist in BIDS entity table for MRI.
    for required in ("sub", "ses", "run"):
        assert required in entity_keys

    # DEFAULT should be using exactly these keys.
    assert DEFAULT.entityTableKeys == entity_keys


def test_derive_entities_from_schema_auto_entities_non_empty_and_matches_default():
    """
    derive_entities_from_schema should return a non-empty mapping of
    auto_entities and it should be consistent with DEFAULT.auto_entities,
    which is initialized from the same helper at import time.
    """
    schema, derived = load_schema(None, None)
    auto_entities = derived["auto_entities"]

    assert isinstance(auto_entities, dict)
    assert len(auto_entities) > 0

    # DEFAULT.auto_entities is built from derive_entities_from_schema()
    # at import time; they should match for the default schema version.
    assert DEFAULT.auto_entities == auto_entities


# https://bids-specification.readthedocs.io/en/v1.11.1/99-appendices/04-entity-table.html
def test_bids_v1_11_1_entity_table_keys_match_hardcoded_list(tmp_path):
    """
    For BIDS v1.11.1, the derived entity_table_keys should match the
    hardcoded list from the v1.11.1 entity table in the spec for MRI (raw, not derivatives).
    """
    expected_entity_keys = [
        'sub',
        'ses',
        'task',
        'acq',
        'ce',
        'rec',
        'dir',
        'run',
        'mod',
        'echo',
        'flip',
        'inv',
        'mt',
        'part',
        'recording',
        'chunk'
    ]

    # Load the v1.11.1 schema directly from the web or cache.
    schema = get_schema(schema_version="v1.11.1", log_dir=tmp_path)
    assert schema is not None
    assert schema.get("bids_version") in ("1.11.1", "v1.11.1")

    entity_keys = _get_raw_mri_entity_table_keys(schema)
    assert entity_keys == expected_entity_keys


def test_bids_v1_11_1_auto_entities_match_hardcoded_mapping(tmp_path):
    """
    For BIDS v1.11.1, the derived auto_entities should match the
    hardcoded mapping we used previously.
    """
    expected_auto_entities = {
        "anat_IRT1": ["inv"],
        "anat_MEGRE": ["echo"],
        "anat_MESE": ["echo"],
        "anat_MP2RAGE": ["inv"],
        "anat_MPM": ["flip", "mt"],
        "anat_MTS": ["flip", "mt"],
        "anat_MTR": ["mt"],
        "anat_VFA": ["flip"],
        "anat_physio": ["task"],
        "anat_physioevents": ["task"],
        "anat_stim": ["task"],
        "func_cbv": ["task"],
        "func_bold": ["task"],
        "func_sbref": ["task"],
        # "func_events": ["task"], # only 3 above needed
        "func_stim": ["task"],
        "func_phase": ["task"],
        "func_physio": ["task"],
        "func_physioevents": ["task"],
        "func_noRF": ["task"],
        # "fmap_epi": ["dir"], # not anymore!
        "fmap_TB1DAM": ["flip"],
        "fmap_TB1EPI": ["echo", "flip"],
        "fmap_TB1SRGE": ["flip", "inv"],
    }

    schema = get_schema(schema_version="v1.11.1", log_dir=tmp_path)
    assert schema is not None
    assert schema.get("bids_version") in ("1.11.1", "v1.11.1")

    auto_entities = _get_auto_entities_from_schema(schema)
    # Exact equality: ensures we haven't regressed compared to the manually-input tables
    assert auto_entities == expected_auto_entities
