"""Run with:  python -m unittest discover -s tests -v   (pytest also works)"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import metrics as M                      # noqa: E402
import report_generator as G             # noqa: E402
from run_pipeline import build_everything   # noqa: E402


class TestMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = build_everything()
        cls.p = cls.b["metrics"].set_index("project_id")

    def test_fifteen_projects(self):
        self.assertEqual(len(self.p), 15)

    def test_earned_value_identities(self):
        for _, r in self.p.iterrows():
            self.assertAlmostEqual(r["spi"], r["ev"] / r["pv"])
            self.assertAlmostEqual(r["cpi"], r["ev"] / r["ac"])
            self.assertAlmostEqual(r["eac"], r["bac"] / r["cpi"])

    def test_erp_migration_is_the_worst_project_and_escalated(self):
        worst = self.b["metrics"].iloc[0]
        self.assertEqual(worst["project_id"], "P01")
        self.assertEqual(worst["rag"], "Red")
        self.assertTrue(worst["escalate"])

    def test_health_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(M.WEIGHTS.values()), 1.0)

    def test_health_score_range_and_rag(self):
        self.assertTrue(self.p["health_score"].between(0, 100).all())
        self.assertEqual(M.rag_for(75), "Green")
        self.assertEqual(M.rag_for(74.9), "Amber")
        self.assertEqual(M.rag_for(54.9), "Red")

    def test_linear_score_bounds(self):
        self.assertEqual(M.linear_score(1.2), 100)
        self.assertEqual(M.linear_score(0.3), 0)
        self.assertAlmostEqual(M.linear_score(0.75), 50)

    def test_dba_is_overallocated(self):
        u = self.b["util"].set_index("name")
        self.assertEqual(u.loc["Jonas Keller", "utilisation_pct"], 140)

    def test_allocation_totals_match(self):
        t = self.b["tables"]
        self.assertAlmostEqual(self.b["util"]["allocation_fte"].sum(), t["allocations"]["allocation_fte"].sum())

    def test_closed_items_do_not_count(self):
        # P03 has one closed issue; it must not reduce the issues score.
        self.assertEqual(self.p.loc["P03", "issue_penalty"], 0)


class TestReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = build_everything()["facts"]

    def test_offline_report_numbers_are_traceable(self):
        md = G.offline_report(self.facts)
        self.assertEqual(G.verify_numbers(md, self.facts), [])

    def test_verifier_catches_invented_number(self):
        md = "The ERP project is forecast to overrun by EUR 913k and has 4217 open defects."
        bad = G.verify_numbers(md, self.facts)
        self.assertIn("913", bad)
        self.assertIn("4217", bad)

    def test_prompt_contains_rules_and_facts(self):
        system, user = G.build_prompt(self.facts)
        self.assertIn("ONLY numbers", system)
        self.assertIn("P01", user)

    def test_llm_provider_paths_parse_responses(self):
        """Providers are exercised with a fake HTTP layer (no network, no key needed)."""
        import os
        calls = []
        def fake_post(url, headers, payload):
            calls.append(url)
            if "anthropic" in url:
                return {"content": [{"text": "## Report\nP01 is Red."}]}
            return {"choices": [{"message": {"content": "## Report\nP01 is Red."}}]}
        real, env = G._post, dict(os.environ)
        G._post = fake_post
        os.environ.update({"ANTHROPIC_API_KEY": "x", "OPENAI_API_KEY": "x", "OPENAI_MODEL": "m"})
        try:
            for prov in ("anthropic", "openai"):
                md, used = G.generate_report(self.facts, prov)
                self.assertEqual(used, prov)
                self.assertTrue(md.startswith("## Report"))
            self.assertEqual(len(calls), 2)
        finally:
            G._post = real
            os.environ.clear(); os.environ.update(env)


if __name__ == "__main__":
    unittest.main()
