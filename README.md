# Linxira Welcome

Plasma-native workstation control center for Linxira OS.

The application reads the versioned Linxira software catalog and installer
receipt, then exposes a fixed allowlist of desktop tools and project resources.
It does not execute shell strings, package transactions, `sudo`, or `pkexec`.

Current surfaces include the Live installer entry, workstation status, curated
profiles, installation receipts, system and recovery tools, Arch Linux News,
project documentation, and a persistent language/login preference.

## Runtime dependencies

- Python 3
- PySide6
- Linxira catalog v2 in `/usr/share/linxira/catalog/`

Optional launch targets such as Shelly, Timeshift, System Settings, Info Center,
Konsole, and Calamares are enabled only when their fixed executable exists.

## Layout

- `src/linxira-welcome`: application entry point
- `data/org.linxira.Welcome.desktop`: application-menu entry
- `data/autostart/org.linxira.Welcome.desktop`: Plasma login entry
- `data/i18n/*.json`: reviewed UI translations with English fallback

The language selector currently exposes English, Simplified Chinese,
Traditional Chinese, German, Spanish, French, Japanese, Korean, Brazilian
Portuguese, and Russian. Catalog profile metadata falls back to English when a
catalog translation for the selected locale is unavailable.

The autostart entry respects the user's `Show Welcome at login` setting. The
Live ISO has an ephemeral profile, so Welcome opens on every fresh Live boot.
