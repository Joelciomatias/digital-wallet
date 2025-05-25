import unittest
from fastapi.testclient import TestClient

from app.api.routes import router
from app.main import app


client = TestClient(app)

class TestAPI(unittest.TestCase):

    def test_get_balance(self):
        response = client.get("/balance")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "ok"})

    def test_post_event(self):
        response = client.post("/event")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "ok"})
