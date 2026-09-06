# Copyright (c) 2026 Ali RahimDabagh
# SPDX-License-Identifier: Apache-2.0

"""Offline checks for the owner-approved license and project attribution."""

import hashlib

from .validation import deny

PROJECT_LICENSE = "Apache-2.0"
LICENSE_STATUS = "approved"
# Official Apache 2.0 text, retrieved 2026-09-06; only CRLF is normalized.
LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
NOTICE_LINES = {
    "Cyber-Sentinel-Skills",
    "Copyright (c) 2026 Ali RahimDabagh",
    "Canonical source: https://github.com/cyber-sentinel/Cyber-Sentinel-Skills",
}


def check_license_materials(license_text, notice):
    """Check this distribution's materials; not a signature or legal audit."""
    if hashlib.sha256(license_text.replace(b"\r\n", b"\n")).hexdigest() != LICENSE_SHA256:
        deny("project-license-mismatch")
    try:
        lines = notice.decode("utf-8").splitlines()
    except UnicodeError:
        deny("invalid-project-notice")
    if not NOTICE_LINES.issubset(lines):
        deny("missing-project-attribution")
