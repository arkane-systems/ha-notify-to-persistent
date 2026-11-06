# ![icon](assets/notify-to-persistent-32px.png) Notify to Persistent for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

Home Assistant is moving notifications from legacy `notify.notify_name` services to notify entities. `notify_to_persistent` bridges that gap for one specific case: it exposes a single notify entity that turns any message sent to it into a Home Assistant [persistent notification](https://www.home-assistant.io/integrations/persistent_notification/) — the kind that shows up in the notification bell.

That's the entire integration. No configuration, no options, no YAML.

---

## Installation

Notify to Persistent is in the HACS default catalog. From Home Assistant 2026.11, HACS is built into Home Assistant as the **Marketplace** (Settings → Marketplace); on earlier versions, install it through [HACS](https://hacs.xyz/).

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=arkane-systems&repository=ha-notify-to-persistent&category=integration)

Open Notify to Persistent with the button above (it opens the Marketplace on 2026.11 or later, and HACS before that), or search for **Notify to Persistent** in the Marketplace or HACS. Download it and restart Home Assistant. Alternatively, copy the `custom_components/notify_to_persistent` directory into your Home Assistant `custom_components` folder manually.

---

## Setup

1. Add the integration:

   [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=notify_to_persistent)

   or go to **Settings → Devices & Services → Add Integration** and search for **Notify to Persistent**.
2. That's it — adding the integration immediately creates the `notify.persistent_notification` entity. There's nothing to configure, and only one instance is allowed.

```yaml
service: notify.send_message
target:
  entity_id: notify.persistent_notification
data:
  message: The garage door has been open for 10 minutes.
  title: Garage Alert
```

Each call creates a new persistent notification — the bell accumulates a history rather than overwriting a single banner. `title` is optional; if omitted, the persistent notification has no title.
