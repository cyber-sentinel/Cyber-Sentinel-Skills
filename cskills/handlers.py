"""Pure, reviewed handlers. Supplied evidence is data, never instructions."""

import hashlib
import ipaddress
import re
from datetime import datetime, timezone

from .validation import deny


def source_index(data):
    sources = data["sources"]
    ids = [s["id"] for s in sources]
    if len(ids) != len(set(ids)):
        deny("duplicate-source-id")
    return set(ids)


def unique_ids(items):
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        deny("duplicate-record-id")


def require_sources(ids, known):
    if not ids or not set(ids) <= known:
        deny("missing-source-reference")


def summarize_evidence(data):
    known = source_index(data)
    unique_ids(data["claims"])
    for claim in data["claims"]:
        require_sources(claim["source_ids"], known)
    claims = sorted(data["claims"], key=lambda c: c["id"])
    return {
        "claims": claims,
        "counts": {
            "source_facts": sum(c["classification"] == "source-fact" for c in claims),
            "analyst_inferences": sum(c["classification"] == "analyst-inference" for c in claims),
        },
        "limitations": ["Classifications are supplied by the caller; authenticity and truth were not verified."],
    }


DOMAIN = re.compile(r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def normalize_iocs(data):
    known = source_index(data)
    unique_ids(data["indicators"])
    merged = {}
    rejected = []
    for item in data["indicators"]:
        require_sources(item["source_ids"], known)
        value = item["value"].strip()
        kind = item["type"]
        try:
            if kind in ("ipv4", "ipv6"):
                addr = ipaddress.ip_address(value)
                if addr.version != (4 if kind == "ipv4" else 6) or "%" in value:
                    raise ValueError
                value = str(addr)
            elif kind == "domain":
                value = value.replace("[.]", ".").lower().removesuffix(".")
                if not DOMAIN.fullmatch(value):
                    raise ValueError
            elif kind == "sha256":
                value = value.lower()
                if not re.fullmatch(r"[a-f0-9]{64}", value):
                    raise ValueError
        except ValueError:
            rejected.append({"id": item["id"], "reason": "invalid-indicator"})
            continue
        key = (kind, value)
        record = merged.setdefault(key, {"type": kind, "value": value,
                                         "source_ids": set(), "record_ids": []})
        record["source_ids"].update(item["source_ids"])
        record["record_ids"].append(item["id"])
    values = []
    for key in sorted(merged):
        record = merged[key]
        record["source_ids"] = sorted(record["source_ids"])
        record["record_ids"].sort()
        values.append(record)
    return {"indicators": values, "rejected": sorted(rejected, key=lambda r: r["id"]),
            "limitations": ["Normalization makes no reputation, ownership or maliciousness judgment; no lookup was performed."]}


TIMESTAMP = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.[0-9]{1,6})?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])$")


def build_timeline(data):
    known = source_index(data)
    unique_ids(data["events"])
    events = []
    for item in data["events"]:
        require_sources([item["source_id"]], known)
        timestamp = item["timestamp"]
        if not TIMESTAMP.fullmatch(timestamp) or timestamp.endswith("-00:00"):
            deny("timestamp-requires-known-offset")
        try:
            instant = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            normalized = instant.astimezone(timezone.utc).isoformat(
                timespec="microseconds").replace("+00:00", "Z")
        except (ValueError, OverflowError):
            deny("invalid-timestamp")
        events.append({**item, "timestamp_utc": normalized})
    events.sort(key=lambda e: (e["timestamp_utc"], e["id"]))
    return {"events": events, "limitations": [
        "Ordering does not establish causality; clock accuracy and source authenticity were not verified."
    ]}


def review_detection_spec(data):
    known = source_index(data)
    rule = data["rule"]
    require_sources(rule["source_ids"], known)
    findings = []
    for condition, code, message in (
        (not rule["log_sources"], "missing-telemetry", "Declare the telemetry needed to evaluate the detection."),
        (rule["time_window_minutes"] is None, "missing-window", "Declare the intended lookback window."),
        (not rule["test_source_ids"], "missing-test-evidence", "Provide references to positive and negative validation evidence."),
        (not rule["false_positive_notes"].strip(), "missing-false-positive-notes", "Document expected benign matches and tuning considerations."),
    ):
        if condition:
            findings.append({"code": code, "message": message})
    if rule["test_source_ids"]:
        require_sources(rule["test_source_ids"], known)
    return {
        "rule_id": rule["id"], "backend": rule["backend"],
        "expression_sha256": hashlib.sha256(rule["expression"].encode("utf-8")).hexdigest(),
        "findings": findings, "metadata_complete": not findings,
        "limitations": ["This is a metadata readiness review; query syntax, behavior and test results were not evaluated."],
    }


HANDLERS = {
    "cs.skills.research.summarize-evidence": ("research", "summarize-evidence", summarize_evidence),
    "cs.skills.threat-intelligence.normalize-iocs": ("threat-intelligence", "normalize-iocs", normalize_iocs),
    "cs.skills.incident-response.build-timeline": ("incident-response", "build-timeline", build_timeline),
    "cs.skills.detection-engineering.review-detection-spec": (
        "detection-engineering", "review-detection-spec", review_detection_spec),
}
