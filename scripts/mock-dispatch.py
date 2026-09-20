#!/usr/bin/env python3
"""
mock-dispatch.py
Simulates broadcasting the validated promotional campaign to the Cymbal Outdoor
marketing messaging gateway.
"""

import sys
import os
import time
import json
import uuid
import argparse
from pathlib import Path

def simulate_dispatch(draft_name: str, payload_info: dict):
    print("=" * 60)
    print("CYMBAL OUTDOOR MARKETING GATEWAY - CAMPAIGN BROADCAST")
    print("=" * 60)
    print(f"[*] Loading campaign draft: {draft_name}")
    print("[*] Connecting to messaging gateway at https://gateway.cymbaloutdoor.internal/v1/broadcast ...")
    time.sleep(0.5)
    print("[*] Verifying gateway credentials and compliance certificate... [OK]")
    time.sleep(0.4)

    # Email Dispatch Simulation
    print("\n[EMAIL DISPATCH]")
    print(f"  - Subject: {payload_info.get('subject', 'Cymbal Outdoor Campaign')}")
    print("  - Target Audience: Active Outdoor Club Members (15,420 subscribers)")
    print("  - Status: QUEUED -> DELIVERED")

    # SMS Dispatch Simulation
    print("\n[SMS DISPATCH]")
    print(f"  - Length: {payload_info.get('sms_len', 115)} characters (1 segment)")
    print("  - Target Numbers: SMS Opt-in List (12,850 phone numbers)")
    print("  - Status: QUEUED -> BROADCASTED")

    # Final Receipt
    broadcast_id = f"CYM-BCAST-{uuid.uuid4().hex[:8].upper()}"
    print("\n" + "-" * 60)
    print(f"[SUCCESS] Broadcast Completed Successfully!")
    print(f"Broadcast ID  : {broadcast_id}")
    print(f"Total Sent    : 28,270 messages across 2 channels")
    print(f"Response Code : 200 OK")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Simulate broadcasting campaign to gateway.")
    parser.add_argument("draft_file", nargs="?", help="Path to draft file (.json, .txt, or .md)")
    args = parser.parse_args()

    draft_path = None
    if args.draft_file:
        draft_path = Path(args.draft_file)
    else:
        for default_name in ["draft.json", "draft.md", "draft.txt"]:
            p = Path(default_name)
            if p.exists():
                draft_path = p
                break

    payload_info = {"subject": "New Product Launch", "sms_len": 120}
    draft_name = "Manual Draft"

    if draft_path and draft_path.exists():
        draft_name = draft_path.name
        try:
            content = draft_path.read_text(encoding="utf-8")
            if draft_path.suffix.lower() == ".json":
                data = json.loads(content)
                payload_info["subject"] = data.get("subject", "Cymbal Outdoor Launch")
                payload_info["sms_len"] = len(data.get("sms", ""))
            else:
                for line in content.splitlines():
                    if line.lower().startswith("subject:"):
                        payload_info["subject"] = line.split(":", 1)[1].strip()
                        break
                if "## SMS" in content:
                    sms_content = content.split("## SMS", 1)[1].strip()
                    payload_info["sms_len"] = len(sms_content)
        except Exception:
            pass

    simulate_dispatch(draft_name, payload_info)
    sys.exit(0)

if __name__ == "__main__":
    main()
