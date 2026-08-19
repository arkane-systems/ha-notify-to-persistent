# ![icon](assets/notify-to-persistent-32px.png) Notify to Persistent for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

Home Assistant is moving notifications from legacy `notify.notify_name` services to notify entities. `notify_to_persistent` bridges that gap for one specific case: it exposes a single notify entity that turns any message sent to it into a Home Assistant [persistent notification](https://www.home-assistant.io/integrations/persistent_notification/) — the kind that shows up in the notification bell.

That's the entire integration. No configuration, no options, no YAML.

---

## Installation

Install via [HACS](https://hacs.xyz/) as a custom repository, or copy the `custom_components/notify_to_persistent` directory into your Home Assistant `custom_components` folder.

---

## Setup

1. Go to **Settings → Devices & Services → Add Integration** and search for **Notify to Persistent**.
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
