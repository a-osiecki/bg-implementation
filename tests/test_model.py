"""Tests del modelo de mercado y de la fórmula de Black-Scholes."""

import math
import unittest

from bg_pricing.model import Market, Option, black_scholes_european, payoff


class PayoffTests(unittest.TestCase):
    def test_call_scalar(self):
        option = Option(strike=100.0, maturity=1.0, kind="call")
        self.assertAlmostEqual(float(payoff(120.0, option)), 20.0)
        self.assertAlmostEqual(float(payoff(80.0, option)), 0.0)

    def test_put_vector(self):
        option = Option(strike=100.0, maturity=1.0, kind="put")
        values = payoff([120.0, 90.0], option)
        self.assertAlmostEqual(values[0], 0.0)
        self.assertAlmostEqual(values[1], 10.0)

    def test_invalid_market(self):
        with self.assertRaises(ValueError):
            Market(spot=0.0, rate=0.05)

    def test_invalid_option(self):
        with self.assertRaises(ValueError):
            Option(strike=-1.0, maturity=1.0)


class BlackScholesTests(unittest.TestCase):
    def setUp(self):
        self.market = Market(spot=100.0, rate=0.05, dividend=0.10, volatility=0.20)
        self.call = Option(strike=100.0, maturity=1.0, kind="call")

    def test_call_value(self):
        value = black_scholes_european(self.market, self.call)
        self.assertAlmostEqual(value, 5.3017, places=4)

    def test_put_call_parity(self):
        put = Option(strike=100.0, maturity=1.0, kind="put")
        call_value = black_scholes_european(self.market, self.call)
        put_value = black_scholes_european(self.market, put)
        forward = self.market.spot * math.exp(-self.market.dividend) - self.call.strike * math.exp(
            -self.market.rate
        )
        self.assertAlmostEqual(call_value - put_value, forward, places=8)

    def test_zero_volatility(self):
        market = Market(spot=100.0, rate=0.05, dividend=0.0, volatility=0.0)
        call = Option(strike=90.0, maturity=1.0, kind="call")
        expected = 100.0 - 90.0 * math.exp(-0.05)
        self.assertAlmostEqual(black_scholes_european(market, call), expected, places=8)

    def test_zero_maturity(self):
        option = Option(strike=100.0, maturity=0.0, kind="call")
        self.assertAlmostEqual(black_scholes_european(self.market, option), 0.0)


if __name__ == "__main__":
    unittest.main()
