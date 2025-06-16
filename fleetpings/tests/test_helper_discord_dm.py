"""Tests for the discord_dm helper."""

# Standard Library
from unittest import TestCase
from unittest.mock import patch, MagicMock

# Alliance Auth (External Libs)
from app_utils.testing import create_fake_user

# AA Fleet Pings
from fleetpings.helper.discord_dm import ping_discord_dm


class TestDiscordDM(TestCase):
    """Test sending a discord DM."""

    @patch("fleetpings.helper.discord_dm.requests.post")
    @patch("fleetpings.helper.discord_dm.DiscordUser")
    def test_ping_discord_dm(self, mock_discord_user, mock_post):
        user = create_fake_user()
        mock_discord_user.objects.get.return_value.uid = "1234"

        ping_discord_dm(ping_context={"ping_channel": {"webhook": None}}, user=user)

        self.assertTrue(mock_post.called)
