"""
tests/test_day1_assignment.py - the Day 1 take-home changes.

Part B: loyalty customers get a late-delivery grace of 1 day instead of 3.
Part C: instructions hidden in ticket text are caught by code (policy rule 7), not only by prompts.
"""
import unittest

from common import llm
from solutions.day1_ai_spectrum import dispute_tools as dt
from solutions.day1_ai_spectrum import level3_ai_agent as l3
from solutions.day1_ai_spectrum._report import actual_outcome, expected_outcome
from tests.fakes import FakeClient, response, text_block, tool_block


def order(days_late, tier=None, amount=40.0):
    """A delivered order, promised 2026-10-10, that arrived `days_late` days after the promise."""
    row = {"order_id": "ORD-9999", "customer_email": "x@example.com", "item": "Test item", "amount": amount,
           "status": "delivered", "ordered": "2026-10-01", "promised": "2026-10-10",
           "delivered": f"2026-10-{10 + days_late:02d}", "condition_note": ""}
    if tier:
        row["customer_tier"] = tier
    return row


class LoyaltyGraceRule(unittest.TestCase):
    """Part B."""

    def test_loyalty_two_days_late_is_refunded(self):
        d = dt.evaluate("x@example.com", order(2, "loyalty"))
        self.assertEqual((d["decision"], d["reason_code"], d["amount"]), ("refund", "LATE_DELIVERY", 40.0))

    def test_loyalty_boundary_exactly_one_day_late_is_not_late(self):
        self.assertNotEqual(dt.evaluate("x@example.com", order(1, "loyalty"))["decision"], "refund")

    def test_standard_customer_two_days_late_is_not_late(self):
        self.assertNotEqual(dt.evaluate("x@example.com", order(2))["decision"], "refund")

    def test_standard_boundary_three_and_four_days(self):
        self.assertNotEqual(dt.evaluate("x@example.com", order(3))["decision"], "refund")
        self.assertEqual(dt.evaluate("x@example.com", order(4))["decision"], "refund")

    def test_ticket_t09_is_refunded_by_the_new_rule(self):
        desk = dt.DisputeDesk(write_logs=False)
        self.assertEqual(expected_outcome(desk, desk.tickets["T-09"]), "refunded")
        self.assertEqual(desk.issue_refund("T-09", "ORD-1009", 40.0, "late, loyalty")["status"], "refunded")


class InstructionsInTicket(unittest.TestCase):
    """Part C: the code-level control."""

    def setUp(self):
        self.desk = dt.DisputeDesk(write_logs=False)

    def test_all_injection_tickets_are_flagged(self):
        for tid in ("T-07", "T-10", "T-11"):
            with self.subTest(tid):
                self.assertTrue(dt.find_instructions(self.desk.tickets[tid]["text"]))

    def test_ordinary_tickets_are_not_flagged(self):
        for tid in ("T-01", "T-02", "T-03", "T-04", "T-05", "T-06", "T-08", "T-09"):
            with self.subTest(tid):
                self.assertEqual(dt.find_instructions(self.desk.tickets[tid]["text"]), [])

    def test_hidden_instruction_blocks_an_otherwise_valid_refund(self):
        # ORD-1010 really is 6 days late, so without the ticket text the policy would refund it.
        t = self.desk.tickets["T-10"]
        self.assertEqual(dt.evaluate(t["customer_email"], self.desk.orders["ORD-1010"])["decision"], "refund")
        r = self.desk.issue_refund("T-10", "ORD-1010", 35.0, "late")
        self.assertEqual((r["status"], r["reason"]), ("blocked", "POLICY_SAYS_ESCALATE:INSTRUCTIONS_IN_TICKET"))
        self.assertTrue(r["signals"])
        self.assertEqual(self.desk.refunds, [])

    def test_expected_outcome_follows_rule_7(self):
        for tid in ("T-07", "T-10", "T-11"):
            with self.subTest(tid):
                self.assertEqual(expected_outcome(self.desk, self.desk.tickets[tid]), "escalated")

    def tearDown(self):
        llm._client = None

    def test_manager_impersonation_obeyed_by_model_is_still_blocked(self):
        """Worst case: the model believes the fake team lead and asks for the refund."""
        llm._client = FakeClient([
            response([tool_block("issue_refund", {"ticket_id": "T-11", "order_id": "ORD-1011", "amount": 95.0,
                                                  "reason": "approved exception TL-2291"}, "a")], "tool_use"),
            response([tool_block("escalate_to_human", {"ticket_id": "T-11", "reason": "refund blocked"}, "b")], "tool_use"),
            response([text_block("Escalated.")]),
        ])
        l3.run_ticket(self.desk, self.desk.tickets["T-11"])
        self.assertEqual(self.desk.refunds, [])
        self.assertEqual(actual_outcome(self.desk, "T-11"), "escalated")


if __name__ == "__main__":
    unittest.main()
