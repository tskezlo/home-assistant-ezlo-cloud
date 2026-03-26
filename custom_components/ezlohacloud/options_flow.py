"""Ezlo HA Cloud integration options flow for Home Assistant."""

import asyncio
from datetime import datetime, timedelta
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.instance_id import async_get as async_get_instance_id
from homeassistant.helpers.network import NoURLAvailableError, get_url

from .api import (
    authenticate,
    create_stripe_session,
    decode_jwt_payload,
    get_subscription_status,
    signup,
)
from .const import DOMAIN, STRIPE_PRICE_ID
from .frp_helpers import fetch_and_update_frp_config, start_frpc, stop_frpc

_LOGGER = logging.getLogger(__name__)


def _raise_missing_uuid():
    raise ValueError("UUID missing in token payload")


class EzloOptionsFlowHandler(config_entries.OptionsFlow):
    """Handles the options flow for Ezlo HA Cloud integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Register options flow steps."""
        return EzloOptionsFlowHandler(config_entry)

    def _get_cloud_url(self) -> str:
        """Build the cloud URL from frpc config data."""
        subdomain = self._config_entry.data.get("subdomain", "")
        server_name = self._config_entry.data.get("server_name", "")

        if subdomain and server_name:
            return f"https://{subdomain}.{server_name}"
        return ""

    async def async_step_init(self, user_input=None):
        """Check login status and show the correct UI."""
        config_data = self._config_entry.data
        is_logged_in = config_data.get("is_logged_in", False)
        token_expiry = config_data.get("token_expiry", 0)

        if is_logged_in and datetime.now().timestamp() > token_expiry:
            return await self.async_step_force_logout()

        if is_logged_in:
            return self.async_show_menu(
                step_id="init",
                menu_options={
                    "cloud_status": "Cloud Connection Status",
                    "view_status": "Subscription Status",
                    "logout": "Logout",
                },
            )

        return self.async_show_menu(
            step_id="init",
            menu_options={
                "login": "Login to Ezlo Cloud",
                "signup": "Create a New Account",
            },
        )

    async def async_step_cloud_status(self, user_input=None):
        """Show cloud connection status and remote URL as a menu."""
        config_data = self._config_entry.data
        user_data = config_data.get("user", {})
        username = user_data.get("username", user_data.get("name", "Unknown"))

        # Check if frpc process is running
        entry_data = self.hass.data.get(DOMAIN, {}).get(
            self._config_entry.entry_id, {}
        )
        process = entry_data.get("process")
        if process and process.poll() is None:
            connection_status = "Connected"
        else:
            connection_status = "Disconnected"

        cloud_url = self._get_cloud_url()
        if not cloud_url:
            cloud_url = "Not available"

        return self.async_show_menu(
            step_id="cloud_status",
            menu_options={
                "init": "Back",
            },
            description_placeholders={
                "connection_status": connection_status,
                "username": username,
                "cloud_url": cloud_url,
            },
        )

    async def async_step_force_logout(self, user_input=None):
        """Force logout the user and return to the main options step."""
        new_data = self._config_entry.data.copy()
        new_data.update(
            {
                "is_logged_in": False,
                "auth_token": None,
                "user": {},
                "token_expiry": 0,
            }
        )
        self.hass.config_entries.async_update_entry(self._config_entry, data=new_data)
        return self.async_abort(reason="session_expired")

    async def async_step_login(self, user_input=None):
        """Handle login authentication form."""
        errors = {}
        if user_input is not None:
            username = user_input["username"]
            password = user_input["password"]

            system_uuid = await async_get_instance_id(self.hass) or ""
            if not system_uuid:
                system_uuid = ""
                _LOGGER.warning("Home Assistant system_uuid missing!")
            auth_response = await authenticate(
                self.hass, username, password, system_uuid
            )

            if auth_response["success"]:
                token = auth_response["data"]["token"]
                user_info = auth_response["data"]["user"]

                await self._handle_successful_login(
                    token,
                    {
                        "uuid": user_info["uuid"],
                        "username": user_info["username"],
                        "email": user_info["email"],
                        "ezlo_id": user_info["ezlo_id"],
                    },
                )
                return self.async_abort(reason="login_successful")
            errors["base"] = "invalid_credentials"

        return self.async_show_form(
            step_id="login",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_logout(self, user_input=None):
        """Handle manual logout action."""
        new_data = self._config_entry.data.copy()
        new_data.update(
            {
                "is_logged_in": False,
                "auth_token": None,
                "user": {},
                "token_expiry": 0,
            }
        )
        self.hass.config_entries.async_update_entry(self._config_entry, data=new_data)
        await stop_frpc(self.hass, self._config_entry)
        return self.async_abort(reason="logged_out")

    async def async_step_signup(self, user_input=None):
        """Handle signup and provide Stripe payment link."""
        errors = {}

        if user_input is not None:
            username = user_input["username"]
            email = user_input["email"]
            password = user_input["password"]

            system_uuid = await async_get_instance_id(self.hass) or ""
            if not system_uuid:
                system_uuid = ""
                _LOGGER.warning("Home Assistant system_uuid missing!")

            signup_response = await signup(
                self.hass, username, email, password, system_uuid
            )

            if signup_response.get("success") and "data" in signup_response:
                try:
                    token = signup_response["data"].get("token", "")
                    payload = decode_jwt_payload(token)
                    user_uuid = payload.get("uuid")

                    if not user_uuid:
                        _raise_missing_uuid()

                    new_data = self._config_entry.data.copy()
                    new_data.update(
                        {
                            "auth_token": token,
                            "user": {
                                "uuid": user_uuid,
                                "username": username,
                                "email": email,
                                "ezlo_id": payload.get("ezlo_user_id", ""),
                            },
                        }
                    )
                    self.hass.config_entries.async_update_entry(
                        self._config_entry, data=new_data
                    )

                    try:
                        # Prefer external URL so Stripe can redirect back
                        base_url = get_url(
                            self.hass,
                            allow_internal=False,
                            allow_external=True,
                        )
                    except NoURLAvailableError:
                        try:
                            base_url = get_url(
                                self.hass, require_current_request=True
                            )
                        except NoURLAvailableError:
                            base_url = get_url(self.hass)
                    back_url = (
                        f"{base_url}/config/integrations/integration/ezlohacloud"
                    )

                    stripe_response = await create_stripe_session(
                        self.hass,
                        user_uuid,
                        STRIPE_PRICE_ID,
                        back_url,
                    )

                    if stripe_response.get("success"):
                        data = stripe_response.get("data", {})
                        checkout_url = data.get("checkout_url")
                        # Start background polling
                        self.hass.async_create_task(
                            self._poll_payment_and_login(
                                user_uuid, token, username, email, payload
                            )
                        )
                        if checkout_url:
                            return self.async_show_form(
                                step_id="redirecting",
                                description_placeholders={"url": checkout_url},
                                data_schema=vol.Schema({}),
                            )
                        _LOGGER.warning(
                            "Stripe session success but no checkout_url: %s",
                            stripe_response,
                        )
                        errors["base"] = "stripe_failed"

                except Exception:
                    _LOGGER.exception("Signup post-processing failed")
                    errors["base"] = "signup_failed"
            else:
                errors["base"] = "signup_failed"

        return self.async_show_form(
            step_id="signup",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("email"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )

    async def _handle_successful_login(self, token: str, user_info: dict) -> None:
        """Shared logic to handle successful login or signup."""
        expiry_time = datetime.now() + timedelta(seconds=3600)

        new_data = self._config_entry.data.copy()
        new_data.update(
            {
                "auth_token": token,
                "user": {
                    "uuid": user_info.get("uuid"),
                    "name": user_info.get("username"),
                    "email": user_info.get("email", ""),
                    "ezlo_id": user_info.get("ezlo_id", ""),
                },
                "is_logged_in": True,
                "token_expiry": expiry_time.timestamp(),
            }
        )

        self.hass.config_entries.async_update_entry(self._config_entry, data=new_data)

        # Update the config toml and start the frpc client.
        try:
            frp_info = await fetch_and_update_frp_config(
                hass=self.hass,
                uuid=user_info["uuid"],
                token=token,
            )
            # Save connection details for the cloud status UI
            updated_data = self._config_entry.data.copy()
            updated_data["server_name"] = frp_info.get("server_name", "")
            updated_data["subdomain"] = frp_info.get("subdomain", "")
            self.hass.config_entries.async_update_entry(
                self._config_entry, data=updated_data
            )
            await start_frpc(hass=self.hass, config_entry=self._config_entry)
        except Exception as err:
            _LOGGER.error("Failed to fetch the server details: %s", err)
        self.hass.async_create_task(
            self.hass.config_entries.async_reload(self._config_entry.entry_id)
        )

    async def _poll_payment_and_login(
        self, user_uuid: str, token: str, username: str, email: str, payload: dict
    ):
        """Background task to poll payment status and login."""
        timeout = 15 * 60  # 15 minutes
        interval = 5  # seconds
        attempts = timeout // interval
        for _ in range(attempts):
            await asyncio.sleep(interval)
            status_response = await get_subscription_status(self.hass, user_uuid)

            if status_response.get("success") and status_response.get("is_active"):
                _LOGGER.info("Subscription activated. Completing login")
                await self._handle_successful_login(
                    token,
                    {
                        "uuid": user_uuid,
                        "username": username,
                        "email": email,
                        "ezlo_id": payload.get("ezlo_user_id", ""),
                    },
                )
                return

        _LOGGER.warning("Polling timeout: User did not complete Stripe payment")

    async def async_step_view_status(self, user_input=None):
        """Display the subscription status as a menu."""
        user_data = self._config_entry.data.get("user", {})
        user_uuid = user_data.get("uuid")

        status_text = "Unknown"
        url = self._config_entry.data.get(
            "payment_url", "https://example.com/cloud"
        )

        if user_uuid:
            status_response = await get_subscription_status(self.hass, user_uuid)
            if status_response.get("success"):
                status = status_response.get("status", "unknown").capitalize()
                is_active = status_response.get("is_active")
                if is_active:
                    status_text = f"Active ({status})"
                else:
                    status_text = f"Inactive ({status})"
            else:
                status_text = f"Error: {status_response.get('error')}"

        return self.async_show_menu(
            step_id="view_status",
            menu_options={
                "init": "Back",
            },
            description_placeholders={
                "url": url,
                "status": status_text,
            },
        )

    async def async_step_stripe_finish(self, user_input=None):
        """Handle return from Stripe redirect with flow_id."""
        _LOGGER.info("Stripe checkout finished, resuming flow")

        new_data = self._config_entry.data.copy()
        new_data["subscription_status"] = "paid"
        self.hass.config_entries.async_update_entry(self._config_entry, data=new_data)

    async def async_step_redirecting(self, user_input=None):
        """User returned from Stripe. Check payment status."""
        user_data = self._config_entry.data.get("user", {})
        user_uuid = user_data.get("uuid")

        _LOGGER.info("Stripe redirection for UUID: %s", user_uuid)

        if self._config_entry.data.get("is_logged_in"):
            return self.async_abort(reason="login_successful")

        return self.async_abort(reason="stripe_redirect_finished")
