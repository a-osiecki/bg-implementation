"""Tests de la estimación con n réplicas y del intervalo de confianza."""

import unittest

from bg_pricing.model import Market, Option
from bg_pricing.pricing import price_american

PAPER_MARKET = Market(spot=100.0, rate=0.05, dividend=0.10, volatility=0.20)
PAPER_CALL = Option(strike=100.0, maturity=1.0, kind="call")


class PricingTests(unittest.TestCase):
    def test_small_run_brackets(self):
        result = price_american(
            PAPER_MARKET,
            PAPER_CALL,
            steps=3,
            branching=3,
            replications=50,
            seed=7,
        )
        self.assertLessEqual(result.low_mean, result.high_mean)
        self.assertLessEqual(result.ci_low, result.point)
        self.assertLessEqual(result.point, result.ci_high)
        self.assertGreater(result.low_stderr, 0.0)
        self.assertGreater(result.high_stderr, 0.0)

    def test_ci_low_truncated_at_intrinsic(self):
        market = Market(spot=50.0, rate=0.5, dividend=0.0, volatility=0.1)
        option = Option(strike=100.0, maturity=0.25, kind="put")
        result = price_american(market, option, steps=1, branching=3, replications=10, seed=3)
        self.assertAlmostEqual(result.ci_low, 50.0, places=8)
        self.assertAlmostEqual(result.high_mean, 50.0, places=8)

    def test_control_variate_reduces_stderr(self):
        plain = price_american(
            PAPER_MARKET,
            PAPER_CALL,
            steps=3,
            branching=20,
            replications=50,
            seed=11,
        )
        adjusted = price_american(
            PAPER_MARKET,
            PAPER_CALL,
            steps=3,
            branching=20,
            replications=50,
            seed=11,
            control_variate=True,
        )
        self.assertLess(adjusted.low_stderr, plain.low_stderr)
        self.assertLess(adjusted.high_stderr, plain.high_stderr)

    def test_requires_two_replications(self):
        with self.assertRaises(ValueError):
            price_american(PAPER_MARKET, PAPER_CALL, steps=3, branching=3, replications=1)

    def test_invalid_confidence(self):
        with self.assertRaises(ValueError):
            price_american(
                PAPER_MARKET,
                PAPER_CALL,
                steps=3,
                branching=3,
                replications=10,
                confidence=1.5,
            )


if __name__ == "__main__":
    unittest.main()
