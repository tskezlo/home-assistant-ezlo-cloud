# Ezlo HA Cloud

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/tskezlo/home-assistant-ezlo-cloud.svg)](https://github.com/tskezlo/home-assistant-ezlo-cloud/releases)
[![GitHub stars](https://img.shields.io/github/stars/tskezlo/home-assistant-ezlo-cloud.svg)](https://github.com/tskezlo/home-assistant-ezlo-cloud/stargazers)

A Home Assistant integration for Ezlo Cloud connectivity.

## Installation

Installing a custom Home Assistant integration takes two phases: first the **files** have to land in your `custom_components/` directory (HACS or manual copy), then Home Assistant has to load the **config flow** so you can add it. The buttons below cover both phases.

### Option 1: HACS (Recommended)

Make sure you have [HACS](https://hacs.xyz/) installed, then click the button below to add this repository to HACS in one click:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tskezlo&repository=home-assistant-ezlo-cloud&category=integration)

After clicking the button:

1. Confirm **Add** in the HACS *"Add custom repository"* dialog.
2. ⬇️ **Click the `DOWNLOAD` button in HACS** — this is the step that actually installs the integration files. It is the floating button in the **bottom-right corner** of the HACS repository page.
3. Confirm **Download** in the version dialog that appears (defaults to the latest release, lands at `/config/custom_components/ezlohacloud`). HACS will reload the integration automatically; you do not need to restart Home Assistant for this integration.
4. Continue to [Configuration](#configuration) below.

> **⚠️ Do not click "Add Integration to My Home Assistant" inside the HACS page in step 2.** HACS renders this README inline, so you will see that button there too — but it does **not** install the integration and will throw *"This integration does not support configuration via the UI"* if clicked before Download. The correct action in step 2 is the **`DOWNLOAD`** button in the bottom-right corner of the HACS page.

### Option 2: Manual Installation

1. Download the latest release from the [releases page](https://github.com/tskezlo/home-assistant-ezlo-cloud/releases).
2. Extract the `ezlohacloud` folder into your Home Assistant `config/custom_components/` directory.
3. Restart Home Assistant. (Required for manual installs — Home Assistant does not auto-detect files added outside of HACS.)
4. Continue to [Configuration](#configuration) below.

## Configuration

After the integration is installed, click the button below to open the config flow directly:

[![Open your Home Assistant instance and show the add integration dialog with a specific repository set up.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ezlohacloud)

Or add it manually through the UI:

1. Go to **Settings** → **Devices & Services**.
2. Click **Add Integration**.
3. Search for "Ezlo HA Cloud".
4. Follow the configuration flow.

> **Note:** The button above only opens the config flow — it does not install the integration. If you click it before Option 1 or Option 2 has been completed, you will see *"This integration does not support configuration via the UI"*. That message is misleading; it just means Home Assistant hasn't loaded the integration files yet. Install via HACS (Option 1) or manual (Option 2) first, then click the button.
