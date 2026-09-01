"""Tests for the REMAINING-WORK-INVENTORY P0-claim fix.

Per WS-2 item 4 of the Phase Kernel brief:
  "Correct `docs/REMAINING-WORK-INVENTORY-2026-09-01.md`: replace
   'zero P0 items open' with the four open credential leaks."

The fix is in the inventory file (a markdown doc). This test enforces that
the fix is present and that the false 'zero P0 open' claim is gone. It
prevents accidental reversion if a future session reads an older copy or
restores the inventory from a stale source.
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).parent.parent
INVENTORY = REPO / "docs" / "REMAINING-WORK-INVENTORY-2026-09-01.md"


class TestInventoryExists(unittest.TestCase):
    def test_inventory_exists(self):
        self.assertTrue(INVENTORY.exists(),
                        f"missing: {INVENTORY}")

    def test_inventory_non_empty(self):
        self.assertGreater(INVENTORY.stat().st_size, 1000,
                           "Inventory file is suspiciously small")


class TestP0ClaimCorrected(unittest.TestCase):
    """The CRITICAL property: the false 'zero P0' claim is REMOVED."""

    def test_zero_P0_claim_gone(self):
        content = INVENTORY.read_text()
        # The exact false claim (original wording)
        self.assertNotIn("zero P0 items open", content,
                         "The literal false claim is still in the inventory")

    def test_zero_P0_claim_gone_loose(self):
        """Catch other phrasings of the same lie."""
        content = INVENTORY.read_text()
        # Any assertion that there are zero open P0 items is the lie
        # (per fb2b81f audit, 4 credential leaks + 79 dead crons)
        if "zero" in content.lower() and "P0" in content:
            # If both present, must be in the context of "previously claimed"
            # or in a quoted correction. Look for the falsifiable form.
            bad_patterns = [
                r"zero\s+P0\s+items?\s+open",
                r"no\s+open\s+P0",
                r"no\s+P0\s+items?\s+open",
            ]
            for pat in bad_patterns:
                self.assertIsNone(re.search(pat, content, re.IGNORECASE),
                                  f"Pattern {pat!r} still present (false P0 claim)")

    def test_p0_items_now_listed(self):
        """The 4 credential leaks must be named in the inventory."""
        content = INVENTORY.read_text()
        # Per fb2b81f and the Phase Kernel brief, these are the 4 leaks
        expected = [
            "SUPABASE_SERVICE_ROLE_KEY",
            "GitHub PAT",
            "R2 presigned",
            ".env",
        ]
        for needle in expected:
            self.assertIn(needle, content,
                          f"Credential leak not named in inventory: {needle!r}")

    def test_cron_79_broken_named(self):
        """Per Q23 of the audit: 79 of 168 enabled crons are broken."""
        content = INVENTORY.read_text()
        self.assertIn("79", content, "Broken-cron count '79' missing")
        self.assertIn("168", content, "Total-enabled cron count '168' missing")
        self.assertIn("litellm-primary", content,
                      "litellm-primary alias not mentioned")

    def test_audit_commit_cited(self):
        """The corrected inventory must cite the audit that fixed it."""
        content = INVENTORY.read_text()
        self.assertIn("fb2b81f", content,
                      "Inventory must cite the audit commit that corrected it")

    def test_token_cap_fix_named(self):
        """The token-cap fix (e03a52a) should be reflected."""
        content = INVENTORY.read_text()
        self.assertIn("e03a52a", content,
                      "Inventory must cite the token-cap fix commit")


if __name__ == "__main__":
    unittest.main(verbosity=2)
