"""Tests del árbol simulado y de los estimadores alto y bajo."""

import unittest

import numpy as np

from bg_pricing.model import Market, Option, black_scholes_european
from bg_pricing.tree import simulate_levels, tree_estimates


class HandComputedTreeTests(unittest.TestCase):
    def test_single_step_put(self):
        # Put con S0 = 90, K = 100 y tres precios terminales: 110, 90 y 70.
        # Payoffs: 0, 10 y 30. Sin descuento.
        # Alto: max(10, (0 + 10 + 30) / 3) = 40 / 3.
        # Bajo: (0 + 10 + 10) / 3 = 20 / 3.
        market = Market(spot=90.0, rate=0.0, dividend=0.0, volatility=0.2)
        option = Option(strike=100.0, maturity=1.0, kind="put")
        levels = [np.array([90.0]), np.array([110.0, 90.0, 70.0])]
        estimate = tree_estimates(levels, market, option, branching=3)
        self.assertAlmostEqual(estimate.high, 40.0 / 3.0, places=12)
        self.assertAlmostEqual(estimate.low, 20.0 / 3.0, places=12)

    def test_zero_steps(self):
        market = Market(spot=90.0, rate=0.05)
        option = Option(strike=100.0, maturity=1.0, kind="put")
        estimate = tree_estimates([np.array([90.0])], market, option, branching=3)
        self.assertAlmostEqual(estimate.high, 10.0)
        self.assertAlmostEqual(estimate.low, 10.0)
        self.assertAlmostEqual(estimate.european, 10.0)

    def test_mismatched_levels_raise(self):
        market = Market(spot=100.0, rate=0.05)
        option = Option(strike=100.0, maturity=1.0)
        levels = [np.array([100.0]), np.array([110.0, 90.0])]
        with self.assertRaises(ValueError):
            tree_estimates(levels, market, option, branching=3)


class SimulatedTreeTests(unittest.TestCase):
    def setUp(self):
        self.market = Market(spot=100.0, rate=0.05, dividend=0.10, volatility=0.2)
        self.call = Option(strike=100.0, maturity=1.0, kind="call")

    def test_level_sizes(self):
        rng = np.random.default_rng(1)
        levels = simulate_levels(self.market, self.call, steps=4, branching=3, rng=rng)
        self.assertEqual([len(level) for level in levels], [1, 3, 9, 27, 81])

    def test_low_not_above_high(self):
        # Teorema 5 del paper: en cada realización, L <= H.
        for seed in range(10):
            rng = np.random.default_rng(seed)
            levels = simulate_levels(self.market, self.call, steps=3, branching=3, rng=rng)
            estimate = tree_estimates(levels, self.market, self.call, branching=3)
            self.assertLessEqual(estimate.low, estimate.high + 1e-12)

    def test_deep_in_the_money_put_exercises_now(self):
        market = Market(spot=50.0, rate=0.5, dividend=0.0, volatility=0.1)
        option = Option(strike=100.0, maturity=0.25, kind="put")
        rng = np.random.default_rng(2)
        levels = simulate_levels(market, option, steps=1, branching=3, rng=rng)
        estimate = tree_estimates(levels, market, option, branching=3)
        self.assertAlmostEqual(estimate.high, 50.0, places=8)
        self.assertAlmostEqual(estimate.low, 50.0, places=8)

    def test_zero_volatility_call_equals_european(self):
        market = Market(spot=100.0, rate=0.05, dividend=0.0, volatility=0.0)
        option = Option(strike=90.0, maturity=1.0, kind="call")
        rng = np.random.default_rng(3)
        levels = simulate_levels(market, option, steps=4, branching=3, rng=rng)
        estimate = tree_estimates(levels, market, option, branching=3)
        expected = black_scholes_european(market, option)
        self.assertAlmostEqual(estimate.high, expected, places=8)
        self.assertAlmostEqual(estimate.low, expected, places=8)

    def test_invalid_branching(self):
        rng = np.random.default_rng(4)
        with self.assertRaises(ValueError):
            simulate_levels(self.market, self.call, steps=3, branching=1, rng=rng)


if __name__ == "__main__":
    unittest.main()
