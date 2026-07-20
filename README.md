# Linxira Welcome

Plasma-native status and routing surface for Linxira OS.

The application reads the versioned Linxira software catalog and installer
receipt, then exposes a fixed allowlist of desktop tools and project resources.
It does not list installable software or execute shell strings, package
transactions, `sudo`, or `pkexec`.

The three pages follow the authoritative Phase 1 product boundary:

- **Home** makes installation the primary Live action. On an installed system it
  shows health and first-completion state derived from the read-only catalog and
  installer receipt.
- **Status** shows release, kernel, network, catalog, receipt, and installation
  selection metadata.
- **Help** provides reviewed documentation links and the login preference.

Home has at most four stable tool launchers: Package Center, Component Manager,
Config CLI in Konsole, and System Settings. Applications, source/runtime
subcommands, and duplicate system-tool inventories remain owned by their
dedicated products and are not reproduced in Welcome.

## Runtime dependencies

- Python 3
- PySide6
- Linxira catalog v2 in `/usr/share/linxira/catalog/`

Optional launch targets are enabled only when their fixed executable exists.
Welcome starts a fixed executable with a fixed argument vector and never
constructs or executes shell strings.

## Layout

- `src/linxira-welcome`: application entry point
- `data/org.linxira.Welcome.desktop`: application-menu entry
- `data/autostart/org.linxira.Welcome.desktop`: Plasma login entry
- `data/i18n/*.json`: reviewed UI translations with English fallback
- `tests/test_welcome.py`: source-boundary and translation contract tests

The language selector currently exposes English, Simplified Chinese,
Traditional Chinese, German, Spanish, French, Japanese, Korean, Brazilian
Portuguese, and Russian.

The autostart entry respects the user's `Show Welcome at login` setting. The
Live ISO has an ephemeral profile, so Welcome opens on every fresh Live boot.

## Test

```console
python -m unittest discover -s tests -v
```
