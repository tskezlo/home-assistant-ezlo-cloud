# Ezlo HA Cloud

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/tskezlo/home-assistant-ezlo-cloud.svg)](https://github.com/tskezlo/home-assistant-ezlo-cloud/releases)
[![GitHub stars](https://img.shields.io/github/stars/tskezlo/home-assistant-ezlo-cloud.svg)](https://github.com/tskezlo/home-assistant-ezlo-cloud/stargazers)

A Home Assistant integration for Ezlo Cloud connectivity.

## Installation

### Option 1: HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Add this repository as a custom repository in HACS
3. Install "Ezlo HA Cloud" from the integrations tab

### Option 2: Manual Installation

1. Download the latest release from the [releases page](https://github.com/tskezlo/home-assistant-ezlo-cloud/releases)
2. Extract the `ezlocloud` folder to your `custom_components` directory
3. Restart Home Assistant

### Option 3: Direct Install Button

[![Open your Home Assistant instance and show the add integration dialog with a specific repository set up.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ezlohacloud)

Click the button above to open Home Assistant and add this integration directly.

## Configuration

After installation, you can configure the integration through the Home Assistant UI:

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Ezlo HA Cloud"
4. Follow the configuration flow

## TODO:

- Fix login issue, routing 401 Unauthorized.
- Signup 