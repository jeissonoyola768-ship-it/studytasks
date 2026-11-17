import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
os.environ["SQLITE_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

import app as studytasks  # noqa: E402


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.client = studytasks.app.test_client()

    def test_health(self):
        r = self.client.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["status"], "ok")

    def test_crud(self):
        r = self.client.post("/api/tareas", json={"titulo": "Entrega Docker", "materia": "SO", "fecha_limite": "2026-12-01"})
        self.assertEqual(r.status_code, 201)
        tid = r.get_json()["id"]
        self.assertIn(tid, [t["id"] for t in self.client.get("/api/tareas").get_json()])
        self.assertEqual(self.client.patch(f"/api/tareas/{tid}").get_json()["completada"], 1)
        self.assertEqual(self.client.delete(f"/api/tareas/{tid}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/tareas/{tid}").status_code, 404)

    def test_validaciones(self):
        self.assertEqual(self.client.post("/api/tareas", json={"titulo": "  "}).status_code, 400)
        self.assertEqual(self.client.post("/api/tareas", json={"titulo": "x", "fecha_limite": "01/12/2026"}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
