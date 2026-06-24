import os
import sys
import unittest
from datetime import datetime

# Set up paths so we can import backend.schemas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from pydantic import ValidationError
from backend.schemas import (
    LoginRequest,
    ClassCreate,
    ClassOut,
    HomeworkCreate,
    HomeworkOut,
    HolidayCreate,
    HolidayOut,
    SubscriberUpsert,
    SubscriberOut,
    SubscriberSetClass,
    SubscriberSetLanguage,
    BroadcastRequest,
)


class MockORMObject:
    """Helper to mock database entities (SQLAlchemy model instances) for from_attributes tests."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestSchemas(unittest.TestCase):
    def test_login_request_validation(self):
        """Verify LoginRequest rejects missing fields but accepts complete structures."""
        # Valid input
        req = LoginRequest(username="admin", password="password")
        self.assertEqual(req.username, "admin")
        self.assertEqual(req.password, "password")

        # Missing password
        with self.assertRaises(ValidationError):
            LoginRequest(username="admin")

    def test_class_create_validation(self):
        """Verify ClassCreate requirements and parsing."""
        req = ClassCreate(name="Grade 10", code="GRADE10")
        self.assertEqual(req.name, "Grade 10")
        self.assertEqual(req.code, "GRADE10")

        # Missing name or code
        with self.assertRaises(ValidationError):
            ClassCreate(code="GRADE10")

    def test_class_out_orm_compatibility(self):
        """Verify ClassOut can populate fields from ORM attributes successfully."""
        now = datetime.now()
        orm_mock = MockORMObject(id=1, name="Grade 12", code="G12", created_at=now)
        
        dto = ClassOut.model_validate(orm_mock)
        self.assertEqual(dto.id, 1)
        self.assertEqual(dto.name, "Grade 12")
        self.assertEqual(dto.code, "G12")
        self.assertEqual(dto.created_at, now)

    def test_homework_create_validation(self):
        """Verify HomeworkCreate validation constraints."""
        hw = HomeworkCreate(
            class_code="G12",
            subject="Mathematics",
            description="Complete exercises 1-5",
            due_date="2026-06-25",
            submitted_by="Teacher Alice"
        )
        self.assertEqual(hw.class_code, "G12")
        self.assertEqual(hw.subject, "Mathematics")

        # Missing field
        with self.assertRaises(ValidationError):
            HomeworkCreate(class_code="G12", subject="Math")

    def test_homework_out_orm_compatibility(self):
        """Verify HomeworkOut conversion handles optional file details correctly."""
        now = datetime.now()
        orm_mock = MockORMObject(
            id=5,
            subject="History",
            description="Read chapter 2",
            due_date="2026-06-28",
            submitted_by="Teacher Bob",
            file_name=None,
            file_url=None,
            created_at=now
        )
        
        dto = HomeworkOut.model_validate(orm_mock)
        self.assertEqual(dto.id, 5)
        self.assertEqual(dto.file_name, None)
        self.assertEqual(dto.file_url, None)

    def test_holiday_create_validation(self):
        """Verify HolidayCreate accepts reason as optional while title and dates are required."""
        hol = HolidayCreate(
            title="Summer Break",
            start_date="2026-07-01",
            end_date="2026-08-31"
        )
        self.assertIsNone(hol.reason)

        hol_with_reason = HolidayCreate(
            title="National Day",
            start_date="2026-11-09",
            end_date="2026-11-09",
            reason="National celebration"
        )
        self.assertEqual(hol_with_reason.reason, "National celebration")

    def test_subscriber_upsert_validation(self):
        """Verify SubscriberUpsert accepts partial profile fields from Telegram callback payloads."""
        sub = SubscriberUpsert(telegram_id="123456789")
        self.assertEqual(sub.telegram_id, "123456789")
        self.assertIsNone(sub.first_name)
        self.assertIsNone(sub.class_code)

        sub_full = SubscriberUpsert(
            telegram_id="123456789",
            first_name="John",
            username="john_doe",
            class_code="GRADE-5"
        )
        self.assertEqual(sub_full.first_name, "John")
        self.assertEqual(sub_full.class_code, "GRADE-5")

    def test_subscriber_out_orm_compatibility(self):
        """Verify SubscriberOut maps active states, registered class, default languages."""
        now = datetime.now()
        orm_mock = MockORMObject(
            id=1,
            telegram_id="987654321",
            first_name="Jane",
            username="jane_tg",
            is_active=True,
            class_code="GRADE-9",
            language="km",
            subscribed_at=now
        )

        dto = SubscriberOut.model_validate(orm_mock)
        self.assertEqual(dto.telegram_id, "987654321")
        self.assertEqual(dto.is_active, True)
        self.assertEqual(dto.language, "km")
        self.assertEqual(dto.subscribed_at, now)


if __name__ == "__main__":
    unittest.main()
