"""Automated curation-policy gates (see docs/curation-policy.md).

Global checks run against every record in data.json and catalog/resources/.
Forward-looking checks apply from FORWARD_POLICY_START onward while historical
records await retroactive cleanup; remove the cutoff once Phase 2 lands.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import pytest

ROOT = Path(__file__).resolve().parent.parent
CAT_DIR = ROOT / "catalog" / "resources"

# Cutoff for rules that historical records do not yet satisfy cleanly.
# Remove this gate date after the retroactive catalog cleanup PR lands.
FORWARD_POLICY_START = "2026-11-26"

SOCIAL_STATUS_RE = re.compile(
    r"^https?://(?:www\.)?(?:x\.com|twitter\.com|fxtwitter\.com|vxtwitter\.com|t\.co)/",
    re.I,
)
X_TRACKING_PARAM_RE = re.compile(r"(?:^|[?&])(?:s|a|t)=(?:20|46|[A-Za-z0-9_-]{8,})(?:&|$)")


@pytest.fixture(scope="module")
def legacy_rows():
    return json.loads((ROOT / "data.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def catalog_records():
    return [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted(CAT_DIR.glob("*.json"))
    ]


def test_no_literal_warning_marker_in_brief(legacy_rows, catalog_records):
    bad_legacy = [r["id"] for r in legacy_rows if "- Warning:" in r["brief"]]
    bad_cat = [r["id"] for r in catalog_records if "- Warning:" in r["brief"]]
    assert bad_legacy == [], f"literal '- Warning:' leaked into data.json brief: {bad_legacy}"
    assert bad_cat == [], f"literal '- Warning:' leaked into catalog brief: {bad_cat}"


def test_global_url_hygiene(catalog_records):
    bad = []
    for r in catalog_records:
        url = r["canonical_url"]
        parsed = urlparse(url)
        if "utm_" in (parsed.query or "").lower():
            bad.append((r["id"], "utm_ param", url))
        if re.search(r"/u/\d+/", parsed.path or ""):
            bad.append((r["id"], "account-index path", url))
    assert bad == [], f"URL hygiene violations: {bad}"


def test_details_length_within_limit(catalog_records):
    too_long = [
        (r["id"], len(r["details"]))
        for r in catalog_records
        if r.get("details") and len(r["details"]) > 2000
    ]
    assert too_long == [], f"details > 2000 chars: {too_long}"


def test_provider_consistency(catalog_records):
    bad = []
    for r in catalog_records:
        is_prov_period = r["display_period"] == "providers"
        has_prov_cat = "providers" in r["legacy_categories"]
        is_prov_type = r["resource_type"] == "provider"
        if not (is_prov_period == has_prov_cat == is_prov_type):
            bad.append((
                r["id"],
                r["display_period"],
                r["legacy_categories"],
                r["resource_type"],
            ))
    assert bad == [], (
        "Channel/category/resource_type mismatch for provider vs non-provider "
        f"(see docs/curation-policy.md §2): {bad}"
    )


def test_forward_no_social_urls_or_x_tracking(catalog_records):
    bad = []
    for r in catalog_records:
        if r["shared_on"] < FORWARD_POLICY_START:
            continue
        url = r["canonical_url"]
        if SOCIAL_STATUS_RE.match(url):
            bad.append((r["id"], "social status/post URL", url))
        if X_TRACKING_PARAM_RE.search(url):
            bad.append((r["id"], "X tracking param", url))
    assert bad == [], f"Forward URL hygiene violations: {bad}"
