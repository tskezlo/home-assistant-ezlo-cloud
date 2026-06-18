# Ezlo HA Cloud

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/tskezlo/home-assistant-ezlo-cloud.svg)](https://github.com/tskezlo/home-assistant-ezlo-cloud/releases)
[![GitHub stars](https://img.shields.io/github/stars/tskezlo/home-assistant-ezlo-cloud.svg)](https://github.com/tskezlo/home-assistant-ezlo-cloud/stargazers)

A Home Assistant integration for Ezlo Cloud connectivity.

## Installation

Installing a custom Home Assistant integration takes two phases: first the **files** have to land in your `custom_components/` directory (HACS or manual copy), then Home Assistant has to load the **config flow** so you can add it. The two buttons below cover both phases.

### Option 1: HACS (Recommended)

Make sure you have [HACS](https://hacs.xyz/) installed, then click the button below to add this repository to HACS in one click:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tskezlo&repository=home-assistant-ezlo-cloud&category=integration)

After clicking the button:

1. Confirm **Add** in the HACS dialog that opens.
2. Click **Download** on the Ezlo HA Cloud entry in HACS.
3. **Restart Home Assistant** when prompted.
4. Continue to [Configuration](#configuration) below.

### Option 2: Manual Installation

1. Download the latest release from the [releases page](https://github.com/tskezlo/home-assistant-ezlo-cloud/releases).
2. Extract the `ezlohacloud` folder to your `custom_components` directory.
3. Restart Home Assistant.
4. Continue to [Configuration](#configuration) below.

## Configuration

After the integration is installed **and Home Assistant has been restarted**, click the button below to open the config flow directly:

[![Open your Home Assistant instance and show the add integration dialog with a specific repository set up.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ezlohacloud)

Or add it manually through the UI:

1. Go to **Settings** → **Devices & Services**.
2. Click **Add Integration**.
3. Search for "Ezlo HA Cloud".
4. Follow the configuration flow.

> **Note:** The button above only opens the config flow — it cannot install the integration. If you click it before Option 1 or Option 2 has been completed (including a Home Assistant restart), you will see *"This integration does not support configuration via the UI"*. That message is misleading; it just means Home Assistant hasn't loaded the integration files yet. Install via HACS or manual first, restart, then click the button.
