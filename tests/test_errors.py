"""Tests for validation functions."""

import pytest
from splitwise_mcp_server.errors import validate_user_split, ValidationError


class TestValidateUserSplit:
    def test_valid_with_user_id(self):
        users = [{"user_id": 123, "paid_share": "25.00", "owed_share": "12.50"}]
        validate_user_split(users)

    def test_valid_with_email_and_name(self):
        users = [
            {
                "email": "jane@example.com",
                "first_name": "Jane",
                "last_name": "Doe",
                "paid_share": "0.00",
                "owed_share": "12.50",
            }
        ]
        validate_user_split(users)

    def test_invalid_no_identification(self):
        users = [{"paid_share": "25.00", "owed_share": "12.50"}]
        with pytest.raises(ValidationError, match="user_id.*or.*email"):
            validate_user_split(users)

    def test_invalid_email_without_name(self):
        users = [{"email": "jane@example.com", "paid_share": "0", "owed_share": "10"}]
        with pytest.raises(ValidationError, match="first_name.*last_name"):
            validate_user_split(users)

    def test_negative_share_raises(self):
        users = [{"user_id": 1, "paid_share": "-5.00", "owed_share": "10.00"}]
        with pytest.raises(ValidationError, match="non-negative"):
            validate_user_split(users)

    def test_empty_list_raises(self):
        with pytest.raises(ValidationError):
            validate_user_split([])

    def test_mixed_identification_valid(self):
        users = [
            {"user_id": 1, "paid_share": "50.00", "owed_share": "25.00"},
            {
                "email": "bob@example.com",
                "first_name": "Bob",
                "last_name": "Smith",
                "paid_share": "0.00",
                "owed_share": "25.00",
            },
        ]
        validate_user_split(users)

    def test_non_dict_user_raises(self):
        users = ["not_a_dict"]
        with pytest.raises(ValidationError, match="must be a dictionary"):
            validate_user_split(users)
