import unittest
from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)


class TestBankAPI(unittest.TestCase):
    def setUp(self):
        # Reset database before each test
        client.post("/reset")

    def test_get_balance_non_existing_account(self):
        response = client.get("/balance", params={"account_id": "1234"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 0)

    def test_create_account_with_initial_balance(self):
        response = client.post("/event", json={
            "type": "deposit",
            "destination": "100",
            "amount": 10
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"destination": {"id": "100", "balance": 10}})

    def test_deposit_into_existing_account(self):
        client.post("/event", json={"type": "deposit", "destination": "100", "amount": 10})
        response = client.post("/event", json={"type": "deposit", "destination": "100", "amount": 10})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"destination": {"id": "100", "balance": 20}})

    def test_get_balance_existing_account(self):
        client.post("/event", json={"type": "deposit", "destination": "100", "amount": 20})
        response = client.get("/balance", params={"account_id": "100"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "20")

    def test_withdraw_from_non_existing_account(self):
        response = client.post("/event", json={"type": "withdraw", "origin": "200", "amount": 10})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 0)

    def test_withdraw_from_existing_account(self):
        client.post("/event", json={"type": "deposit", "destination": "100", "amount": 20})
        response = client.post("/event", json={"type": "withdraw", "origin": "100", "amount": 5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"origin": {"id": "100", "balance": 15}})

    def test_transfer_from_existing_account(self):
        client.post("/event", json={"type": "deposit", "destination": "100", "amount": 15})
        response = client.post("/event", json={"type": "transfer", "origin": "100", "destination": "300", "amount": 15})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "origin": {"id": "100", "balance": 0},
            "destination": {"id": "300", "balance": 15}
        })

    def test_transfer_from_non_existing_account(self):
        response = client.post("/event", json={"type": "transfer", "origin": "200", "destination": "300", "amount": 15})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 0)

    def test_reset(self):
        client.post("/event", json={"type": "deposit", "destination": "100", "amount": 50})
        client.post("/reset")
        response = client.get("/balance", params={"account_id": "100"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 0)
