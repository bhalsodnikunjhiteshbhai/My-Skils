---
name: promo-writer
description: Guides the creation of promotional marketing campaigns. Use when writing promotional copy to ensure both compliant email and SMS formats are provided according to brand guidelines.
---

# Promo Writer

This skill defines the mandatory guidelines and structure for crafting promotional marketing communications.

## Required Preparation

Before generating any copy, you MUST read the reference files located in the `references/` directory:
- [brand-voice.md](references/brand-voice.md): Follow all tone and style instructions (friendly, outdoorsy, never shouty, and strictly forbidding emojis).
- [email-template.txt](references/email-template.txt): Follow the standard layout structure (subject, greeting, hook, offer, link, footer).

## Rules & Requirements

Whenever generating promotional messages, you must strictly adhere to the following rules:

1. **Dual Format Requirement**:
   - Every promotional message campaign must include **both** an **Email** and an **SMS blast**.

2. **Email Guidelines**:
   - Structure the email following `references/email-template.txt` (subject, greeting, hook, offer, link, footer).
   - The email must include a clear and engaging **Subject line**.
   - The email must end with the exact opt-out phrase: `Reply STOP to opt out.`

3. **SMS Guidelines**:
   - The SMS blast must be strictly **under 160 characters** (including spaces, links, and disclaimers).
   - The SMS blast must end with the exact opt-out phrase: `Reply STOP to opt out.`

4. **Brand Voice & Tone**:
   - Strictly adhere to `references/brand-voice.md`.
   - Strictly forbid emojis across all generated copy (no emojis in email or SMS).
   - Keep the tone friendly, outdoorsy, authentic, and never shouty.

## Execution Workflow

When fulfilling a promotional campaign request, follow this exact procedure:

1. **Save the Draft**: Save your drafted promotional email and SMS to a file (e.g., `draft.json` or `draft.txt`).
2. **Validate Compliance in a Loop**:
   - Run `python scripts/check-compliance.py <draft_file>`.
   - If compliance checks fail, inspect the errors, adjust the draft, and re-run `check-compliance.py` in a loop until it passes with exit code `0`.
3. **Broadcast Campaign**:
   - **ONLY** when compliance validation passes, execute `python scripts/mock-dispatch.py <draft_file>` to simulate broadcasting the campaign to the gateway.
