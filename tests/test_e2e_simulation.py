import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Set up paths so we can import backend and src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Configure test environment variables BEFORE importing backend modules
os.environ["ADMIN_USERNAME"] = "e2eadmin"
os.environ["ADMIN_PASSWORD"] = "e2epass123"
os.environ["API_SECRET_KEY"] = "e2e-secret-key-12345"
os.environ["TELEGRAM_BOT_TOKEN"] = "123456789:mocktoken"
os.environ["API_BASE_URL"] = "http://127.0.0.1:8001"
os.environ["RUN_BOT"] = "false"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database import Base, get_db
from main import app
from translations import t


# Setup a dedicated clean SQLite database for the E2E simulation
TEST_DB_FILE = "./test_e2e.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply FastAPI dependency override for database session
app.dependency_overrides[get_db] = override_get_db


class TestE2ESimulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Backup original env variables to prevent leaks
        cls._orig_env = {
            "ADMIN_USERNAME": os.environ.get("ADMIN_USERNAME"),
            "ADMIN_PASSWORD": os.environ.get("ADMIN_PASSWORD"),
            "API_SECRET_KEY": os.environ.get("API_SECRET_KEY"),
        }
        
        # Set mock env variables at runtime to override values from .env
        os.environ["ADMIN_USERNAME"] = "e2eadmin"
        os.environ["ADMIN_PASSWORD"] = "e2epass123"
        os.environ["API_SECRET_KEY"] = "e2e-secret-key-12345"

        # Override database session factory in database and main modules to redirect background tasks
        import database
        import main
        cls._orig_SessionLocal = database.SessionLocal
        database.SessionLocal = TestingSessionLocal
        main.SessionLocal = TestingSessionLocal

        # Remove database file if it exists to ensure a completely clean database state
        if os.path.exists(TEST_DB_FILE):
            try:
                os.remove(TEST_DB_FILE)
            except Exception as e:
                print(f"Warning: Could not remove old test database: {e}")

        # Create database schema
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Restore original SessionLocal
        import database
        import main
        database.SessionLocal = cls._orig_SessionLocal
        main.SessionLocal = cls._orig_SessionLocal

        # Clean up database tables
        Base.metadata.drop_all(bind=engine)
        # Dispose of engine to release database file lock on Windows
        engine.dispose()
        if os.path.exists(TEST_DB_FILE):
            try:
                os.remove(TEST_DB_FILE)
            except Exception as e:
                print(f"Warning: could not delete {TEST_DB_FILE}: {e}")

        # Restore original env variables
        for k, v in cls._orig_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_e2e_user_workflow(self):
        """Simulate a complete user journey between Dashboard, Backend, and Telegram Bot."""
        headers = {}

        # ----------------------------------------------------
        # Step 1: Admin logs into the Web Dashboard
        # ----------------------------------------------------
        login_resp = self.client.post(
            "/api/auth/login",
            data={"username": "e2eadmin", "password": "e2epass123"}
        )
        self.assertEqual(login_resp.status_code, 200, f"Login failed: {login_resp.text}")
        token_data = login_resp.json()
        token = token_data.get("access_token")
        self.assertIsNotNone(token)
        
        headers["Authorization"] = f"Bearer {token}"

        # ----------------------------------------------------
        # Step 2: Teacher/Admin registers a new class "GRADE-10"
        # ----------------------------------------------------
        class_resp = self.client.post(
            "/api/classes",
            json={"name": "Grade 10 Upper Class", "code": "GRADE-10"},
            headers=headers
        )
        self.assertEqual(class_resp.status_code, 201, f"Class creation failed: {class_resp.text}")
        self.assertEqual(class_resp.json()["code"], "GRADE-10")

        # ----------------------------------------------------
        # Step 3: Parent joins the Telegram bot and registers
        # ----------------------------------------------------
        # The bot makes a post to backend /api/subscribers to register the Telegram ID
        parent_tg_id = "888888888"
        sub_resp = self.client.post(
            "/api/subscribers",
            json={
                "telegram_id": parent_tg_id,
                "first_name": "Somnang",
                "username": "somnang_parent"
            }
        )
        self.assertEqual(sub_resp.status_code, 201, f"Subscriber registration failed: {sub_resp.text}")
        sub_data = sub_resp.json()
        self.assertEqual(sub_data["first_name"], "Somnang")
        self.assertEqual(sub_data["language"], "en")  # Default language is English

        # Parent selects Khmer language in the Telegram bot UI
        lang_resp = self.client.patch(
            f"/api/subscribers/{parent_tg_id}/language",
            json={"language": "km"}
        )
        self.assertEqual(lang_resp.status_code, 200)
        self.assertEqual(lang_resp.json()["language"], "km")

        # Parent selects the class code "GRADE-10"
        bind_resp = self.client.patch(
            f"/api/subscribers/{parent_tg_id}/class",
            json={"telegram_id": parent_tg_id, "class_code": "GRADE-10"}
        )
        self.assertEqual(bind_resp.status_code, 200, f"Class binding failed: {bind_resp.text}")
        self.assertEqual(bind_resp.json()["class_code"], "GRADE-10")

        # ----------------------------------------------------
        # Step 4: Teacher uploads Homework for "GRADE-10"
        # ----------------------------------------------------
        # Form-data post mimicking teacher dashboard upload
        homework_resp = self.client.post(
            "/api/homework",
            data={
                "class_code": "GRADE-10",
                "subject": "Chemistry",
                "description": "Read page 45-50 and do exercise 3",
                "due_date": "2026-06-25",
                "submitted_by": "Teacher Sopheap"
            },
            headers=headers
        )
        self.assertEqual(homework_resp.status_code, 201, f"Homework submission failed: {homework_resp.text}")
        hw_id = homework_resp.json().get("id")
        self.assertIsNotNone(hw_id)

        # ----------------------------------------------------
        # Step 5: Parent queries homework through the Telegram Bot
        # ----------------------------------------------------
        # Simulates bot calling the API to fetch homework for parent's bound class
        parent_hw_resp = self.client.get("/api/homework/GRADE-10")
        self.assertEqual(parent_hw_resp.status_code, 200)
        hws = parent_hw_resp.json()
        self.assertEqual(len(hws), 1)
        
        fetched_hw = hws[0]
        self.assertEqual(fetched_hw["subject"], "Chemistry")
        self.assertEqual(fetched_hw["submitted_by"], "Teacher Sopheap")

        # Test local translation formatting inside bot logic
        # Simulating how bot formats output in Khmer:
        hw_header_text = t("hw_header", "km", code="GRADE-10", date="2026-06-20", count=len(hws), plural="")
        hw_item_text = f"📚 *{fetched_hw['subject']}*\n📝 {fetched_hw['description']}\n" + t("hw_due", "km", date=fetched_hw["due_date"]) + "\n" + t("hw_teacher", "km", name=fetched_hw["submitted_by"])
        
        self.assertIn("GRADE-10", hw_header_text)
        self.assertIn("កិច្ចការផ្ទះ", hw_header_text)
        self.assertIn("Chemistry", hw_item_text)
        self.assertIn("Teacher Sopheap", hw_item_text)

        # ----------------------------------------------------
        # Step 6: Admin broadcasts announcement
        # ----------------------------------------------------
        # We mock the HTTP client post to prevent real calls to the Telegram sendMessage API.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}

        # Mock the async httpx client post method
        with patch("httpx.AsyncClient.post", return_value=mock_response) as mock_post:
            broadcast_resp = self.client.post(
                "/api/broadcast",
                json={"message": "Urgent: School closed tomorrow due to heavy rain!"},
                headers=headers
            )
            self.assertEqual(broadcast_resp.status_code, 200, f"Broadcast enqueuing failed: {broadcast_resp.text}")
            self.assertEqual(broadcast_resp.json()["sent_to"], 1)

            # TestClient runs FastAPI background tasks synchronously during the request context,
            # so the task has already executed. Let's check that httpx.AsyncClient.post was called
            # to sendMessage to our parent's Telegram ID
            mock_post.assert_called_once()
            call_args = mock_post.call_args[1]
            self.assertIn("sendMessage", mock_post.call_args[0][0])
            self.assertEqual(call_args["json"]["chat_id"], parent_tg_id)
            self.assertIn("School closed tomorrow", call_args["json"]["text"])


if __name__ == "__main__":
    unittest.main()
