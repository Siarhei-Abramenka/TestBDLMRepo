import pytest

from src.dummy_script import validate_email


class TestValidateEmail:
    """Tests for validate_email function"""

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("user@example.com", True),
            ("test.user@domain.com", True),
            ("user123@example.co.uk", True),
            ("first.last@company.org", True),
            ("user_name@example-domain.com", True),
            ("a@b.co", True),
            ("user@subdomain.example.com", True),
            ("user_name-123@test-domain.co.uk", True),
            ("simple@example.io", True),
            ("test123@test-domain.co", True),
        ],
    )
    def test_valid_emails(self, email, expected):
        """Test valid email addresses"""
        assert validate_email(email) == expected

    @pytest.mark.parametrize(
        "email",
        [
            "invalid.email",
            "@example.com",
            "user@",
            "user@.com",
            "user@com",
            "user@example.",
            "user@example.c",
            "user@example",
            "123@456.789",
        ],
    )
    def test_invalid_emails(self, email):
        """Test invalid email addresses"""
        assert validate_email(email) is False

    @pytest.mark.parametrize(
        "email",
        [
            "",
            "user..name@example.com",  # Double dot in local part
            ".user@example.com",  # Starts with dot
            "user.@example.com",  # Ends with dot
            "user@.example.com",  # Domain starts with dot
            "user@example..com",  # Double dot in domain
        ],
    )
    def test_edge_cases(self, email):
        """Test edge cases"""
        assert validate_email(email) is False

    @pytest.mark.parametrize(
        "invalid_input",
        [
            123,
            None,
            [],
            {},
            True,
            False,
            3.14,
        ],
    )
    def test_non_string_input(self, invalid_input):
        """Test non-string input"""
        assert validate_email(invalid_input) is False

    def test_length_limits_valid(self):
        """Test valid email length limits"""
        # Valid length - local part at limit
        long_local = "a" * 64 + "@example.com"
        assert validate_email(long_local) is True

        # Valid length - just under 254 chars
        valid_long = "a" * 60 + "@" + "b" * 60 + ".com"
        assert len(valid_long) < 254
        assert validate_email(valid_long) is True

    def test_length_limits_invalid(self):
        """Test invalid email length limits"""
        # Too long local part
        too_long_local = "a" * 65 + "@example.com"
        assert validate_email(too_long_local) is False

        # Very long email (over 254 chars)
        very_long = "a" * 250 + "@example.com"
        assert validate_email(very_long) is False

        # Domain part too long
        long_domain = "user@" + "a" * 254 + ".com"
        assert validate_email(long_domain) is False

    def test_tld_validation(self):
        """Test TLD (top-level domain) validation"""
        # Valid TLDs
        assert validate_email("user@example.com") is True
        assert validate_email("user@example.org") is True
        assert validate_email("user@example.co.uk") is True

        # Invalid TLDs
        assert validate_email("user@example.c") is False  # Too short
        assert validate_email("user@example.") is False  # No TLD
        assert validate_email("user@example") is False  # No TLD

    def test_special_characters(self):
        """Test emails with special characters"""
        # Valid special characters (dots, hyphens, underscores)
        assert validate_email("user.name@example.com") is True
        assert validate_email("user-name@example.com") is True
        assert validate_email("user_name@example.com") is True

        # Invalid special characters (not in pattern)
        assert validate_email("user+tag@example.com") is False
        assert validate_email("user#tag@example.com") is False
        assert validate_email("user$tag@example.com") is False

    def test_multiple_dots_in_domain(self):
        """Test emails with multiple dots in domain"""
        assert validate_email("user@sub.domain.example.com") is True
        assert validate_email("user@a.b.c.d.example.com") is True

    def test_numeric_emails(self):
        """Test emails with numeric parts"""
        assert validate_email("123@456.com") is True
        assert validate_email("user123@example.com") is True
        assert validate_email("123user@example.com") is True
