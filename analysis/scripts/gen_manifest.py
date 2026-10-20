#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerate analysis/MANIFEST.json - SHA-256 of every input and output artifact.

Run LAST, after all analysis scripts. Any change to an upstream file changes the
manifest and therefore invalidates a release claim.
"""

import hashlib
import json
import os
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

INCLUDE_DIRS = [
    "analysis/config",
    "analysis/scripts",
    "analysis/results",
]
# raw GEO inputs: hashed but never packaged (re-downloadable, tens of MB)
RAW_GLOBS = [
    "analysis/data/raw/_download.sh",
    "analysis/data/raw/_gse98547",
    "analysis/data/raw/_gse261676",
    "analysis/data/raw/_annotation/gencode_v24lift37_geneid_to_biotype.tsv",
]


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def walk(rel):
    p = os.path.join(ROOT, rel)
    if os.path.isfile(p):
        yield rel, p
        return
    for dirpath, _, files in os.walk(p):
        for f in sorted(files):
            full = os.path.join(dirpath, f)
            yield os.path.relpath(full, ROOT).replace("\\", "/"), full


def main():
    files = {}
    for d in INCLUDE_DIRS:
        for rel, full in walk(d):
            files[rel] = {"sha256": sha256(full), "bytes": os.path.getsize(full)}

    raw = {}
    for pat in RAW_GLOBS:
        p = os.path.join(ROOT, pat)
        if os.path.isfile(p):
            raw[pat] = {"sha256": sha256(p), "bytes": os.path.getsize(p)}
        elif os.path.isdir(p):
            for rel, full in walk(pat):
                raw[rel] = {"sha256": sha256(full), "bytes": os.path.getsize(full)}

    out = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_artifacts": len(files),
        "n_raw_inputs": len(raw),
        "artifacts": files,
        "raw_inputs_not_packaged": raw,
    }
    dest = os.path.join(ROOT, "analysis", "MANIFEST.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f"wrote {dest}: {len(files)} artifacts, {len(raw)} raw inputs")


if __name__ == "__main__":
    main()
