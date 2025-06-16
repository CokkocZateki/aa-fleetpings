"""Send Discord Direct Messages."""

from __future__ import annotations

# Standard Library
import logging
from typing import Any

import requests
from django.conf import settings
from django.contrib.auth.models import User

from fleetpings.constants import APP_NAME, GITHUB_URL
from fleetpings.helper.eve_images import get_character_portrait_from_evecharacter
from fleetpings.helper.ping_context import _get_webhook_ping_context

try:
    from allianceauth.services.modules.discord.models import DiscordUser
except Exception:  # pragma: no cover - allianceauth not available
    DiscordUser = None  # type: ignore

logger = logging.getLogger(__name__)


def ping_discord_dm(ping_context: dict[str, Any], user: User) -> None:
    """Send a direct message with fleet ping details to the given user."""

    if DiscordUser is None:
        logger.warning("Discord service not installed, cannot send DM")
        return

    token = getattr(settings, "FLEETPINGS_BOT_TOKEN", None)
    if not token:
        logger.warning("FLEETPINGS_BOT_TOKEN not configured")
        return

    try:
        discord_user = DiscordUser.objects.get(user=user)
    except Exception as ex:  # pragma: no cover - external lib
        logger.warning("Could not find Discord user for %s: %s", user, ex)
        return

    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": f"{APP_NAME} ({GITHUB_URL})",
        "Content-Type": "application/json",
    }

    # Create DM channel
    response = requests.post(
        "https://discord.com/api/v10/users/@me/channels",
        json={"recipient_id": str(discord_user.uid)},
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    channel_id = response.json()["id"]

    webhook_ping_context = _get_webhook_ping_context(ping_context=ping_context)
    message = f"{webhook_ping_context['header']}\n{webhook_ping_context['content']}"

    send_resp = requests.post(
        f"https://discord.com/api/v10/channels/{channel_id}/messages",
        json={"content": message},
        headers=headers,
        timeout=10,
    )
    send_resp.raise_for_status()
