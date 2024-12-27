import unittest
from smart_contracts.meme_token import MemeToken
from smart_contracts.trading import Trading

class TestMemeToken(unittest.TestCase):
    def setUp(self):
        self.token = MemeToken()

    def test_initial_supply(self):
        self.assertEqual(self.token.total_supply(), 1000000)

    def test_transfer(self):
        self.token.transfer("address1", 100)
        self.assertEqual(self.token.balance_of("address1"), 100)

class TestTrading(unittest.TestCase):
    def setUp(self):
        self.trading = Trading()

    def test_trade(self):
        result = self.trading.execute_trade("address1", "address2", 50)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()