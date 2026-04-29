"""Constants for the Ezlo HA Cloud integration."""

DOMAIN = "ezlohacloud"

STORAGE_KEY = "ezlo_user_data"
STORAGE_VERSION = 1

EZLO_API_URI = "https://haapi-dev.ezlo.com"
STRIPE_PRICE_ID = "price_1TN5VXDRlmhIfMaksNlyB050"
HOMEASSISTANT_HOST = "homeassistant.local"

# Subscription status values (from Stripe)
SUBSCRIPTION_TRIALING = "trialing"
SUBSCRIPTION_ACTIVE = "active"
SUBSCRIPTION_PAST_DUE = "past_due"
SUBSCRIPTION_CANCELED = "canceled"
SUBSCRIPTION_INCOMPLETE = "incomplete"

# States that grant access to the integration
SUBSCRIPTION_VALID_STATES = (SUBSCRIPTION_TRIALING, SUBSCRIPTION_ACTIVE)
# States that require resubscription
SUBSCRIPTION_INVALID_STATES = (
    SUBSCRIPTION_PAST_DUE,
    SUBSCRIPTION_CANCELED,
    SUBSCRIPTION_INCOMPLETE,
)
