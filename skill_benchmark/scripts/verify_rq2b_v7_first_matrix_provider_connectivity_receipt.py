#!/usr/bin/env python3
"""Replay the sanitised V7 provider-connectivity receipt without network."""

from __future__ import annotations

import json

from build_rq2b_v7_first_matrix_provider_connectivity_receipt import verify


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
