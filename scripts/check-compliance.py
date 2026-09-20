#!/usr/bin/env python3
"""
check-compliance.py
Validates promotional copy against compliance and brand voice rules:
1. SMS length must be strictly under 160 characters.
2. Both Email and SMS must end with 'Reply STOP to opt out.'
3. Email must include a subject line.
4. Emojis are strictly prohibited.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

OPT_OUT_PHRASE = "Reply STOP to opt out."
EMOJI_PATTERN = re.compile(
    "[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50\u2b55\u200d\ufe0f]",
    flags=re.UNICODE
)

def validate_promo(email_text: str, sms_text: str, subject: str = ""):
    errors = []
    
    # 1. Subject Line Check
    clean_email = email_text.strip()
    if not subject and not clean_email.lower().startswith("subject:"):
        errors.append("Compliance Error: Email must contain a 'Subject:' line.")

    # 2. SMS Length Check (< 160 characters)
    sms_len = len(sms_text.strip())
    if sms_len >= 160:
        errors.append(
            f"Compliance Error: SMS length is {sms_len} characters. It must be strictly under 160 characters."
        )

    # 3. Opt-Out Footer Check
    if not clean_email.endswith(OPT_OUT_PHRASE):
        errors.append(
            f"Compliance Error: Email must end with exact footer: '{OPT_OUT_PHRASE}'"
        )

    if not sms_text.strip().endswith(OPT_OUT_PHRASE):
        errors.append(
            f"Compliance Error: SMS must end with exact footer: '{OPT_OUT_PHRASE}'"
        )

    # 4. Emoji Prohibition Check
    if EMOJI_PATTERN.search(clean_email):
        errors.append("Brand Voice Error: Emojis detected in email copy (strictly prohibited).")
    if EMOJI_PATTERN.search(sms_text):
        errors.append("Brand Voice Error: Emojis detected in SMS copy (strictly prohibited).")

    return errors

def parse_text_draft(content: str):
    email = ""
    sms = ""
    subject = ""
    
    # Check for Markdown/Text sections
    if "## SMS" in content or "SMS:" in content:
        parts = re.split(r"(?:##\s*SMS|SMS\s*Blast:?|SMS:)", content, flags=re.IGNORECASE)
        email_part = parts[0]
        sms_part = parts[1] if len(parts) > 1 else ""
        
        # Clean up email part
        email_part = re.sub(r"^(?:##\s*Email|Email:?)\s*", "", email_part, flags=re.IGNORECASE).strip()
        sms = sms_part.strip().strip("> \n\r\"'")
        email = email_part.strip()
    else:
        email = content.strip()

    # Extract subject if present
    subj_match = re.search(r"^\s*Subject:\s*(.+)$", email, re.MULTILINE | re.IGNORECASE)
    if subj_match:
        subject = subj_match.group(1).strip()

    return email, sms, subject

def main():
    parser = argparse.ArgumentParser(description="Validate promotional copy compliance.")
    parser.add_argument("draft_file", nargs="?", help="Path to draft file (.json, .txt, or .md)")
    parser.add_argument("--sms", help="SMS text content directly via CLI")
    parser.add_argument("--email", help="Email text content directly via CLI")
    parser.add_argument("--subject", help="Email subject line directly via CLI")

    args = parser.parse_args()

    email = args.email or ""
    sms = args.sms or ""
    subject = args.subject or ""

    if args.draft_file:
        file_path = Path(args.draft_file)
        if not file_path.exists():
            print(f"[FAIL] Error: Draft file not found at {file_path}")
            sys.exit(1)
        
        content = file_path.read_text(encoding="utf-8")
        if file_path.suffix.lower() == ".json":
            data = json.loads(content)
            email = data.get("email", "")
            sms = data.get("sms", "")
            subject = data.get("subject", "")
        else:
            email, sms, subject = parse_text_draft(content)
    elif not email and not sms:
        # Check if default draft file exists in current directory
        for default_name in ["draft.json", "draft.md", "draft.txt"]:
            p = Path(default_name)
            if p.exists():
                print(f"[INFO] Using detected draft file: {default_name}")
                content = p.read_text(encoding="utf-8")
                if p.suffix.lower() == ".json":
                    data = json.loads(content)
                    email = data.get("email", "")
                    sms = data.get("sms", "")
                    subject = data.get("subject", "")
                else:
                    email, sms, subject = parse_text_draft(content)
                break

    if not email and not sms:
        print("[FAIL] Error: No promotional draft provided. Specify a draft file or use --email and --sms.")
        sys.exit(1)

    errors = validate_promo(email, sms, subject)

    if errors:
        print("\n" + "="*50)
        print("COMPLIANCE VALIDATION FAILED:")
        print("="*50)
        for err in errors:
            print(f"  - {err}")
        print(f"\nSMS character count: {len(sms.strip())} chars (limit: <160)")
        print("="*50 + "\n")
        sys.exit(1)
    else:
        print("\n" + "="*50)
        print("COMPLIANCE VALIDATION PASSED!")
        print("="*50)
        print(f"[OK] SMS Length: {len(sms.strip())} chars (< 160)")
        print("[OK] Opt-Out Footers: Present in both channels")
        print("[OK] Subject Line: Present")
        print("[OK] Emojis: None detected (Complies with brand voice)")
        print("="*50 + "\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
