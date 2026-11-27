#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call the Bridge render API with a widened scope; expect ScopeDenied."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import w1_bridge_reference as bridge

expl = json.load(open(sys.argv[1], encoding="utf-8"))
try:
    bridge.render_agent_context(expl, "Codex", expl["identity"]["scope"] + " AND MORE")
except bridge.ScopeDenied:
    print("SCOPE_DENIED")
    sys.exit(0)
print("NOT_DENIED")
sys.exit(3)
