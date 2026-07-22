import ast
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
WELCOME = ROOT / "src/linxira-welcome"
I18N = ROOT / "data/i18n"


def assignment_value(source, name):
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            class ResolveConstants(ast.NodeTransformer):
                def visit_Name(self, value):
                    if value.id == "LIVE_INSTALLER":
                        return ast.copy_location(ast.Constant("/usr/local/bin/linxira-installer-shell"), value)
                    return value

            node.value = ResolveConstants().visit(node.value)
            return ast.literal_eval(node.value)
    raise AssertionError(f"missing assignment: {name}")


class WelcomeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WELCOME.read_text(encoding="utf-8")

    def test_has_only_home_status_and_help_pages(self):
        self.assertIn("self._home_page()", self.source)
        self.assertIn("self._status_page()", self.source)
        self.assertIn("self._help_page()", self.source)
        for removed in (
            "_setup_page",
            "_software_page",
            "_sources_page",
            "_system_page",
            "_resources_page",
        ):
            self.assertNotIn(removed, self.source)

    def test_uses_only_the_fixed_product_launchers(self):
        apps = assignment_value(self.source, "APPS")
        self.assertEqual(
            set(apps),
            {"installer", "package_center", "component_manager", "config", "settings", "update", "gaming", "recovery"},
        )
        self.assertEqual(apps["component_manager"], ("/usr/bin/linxira-component-manager", []))
        self.assertEqual(apps["update"], ("/usr/bin/linxira-update", []))
        self.assertEqual(apps["gaming"], ("/usr/bin/linxira-gaming-manager", []))
        self.assertEqual(apps["recovery"], ("/usr/bin/linxira-recovery-diagnostics", []))
        self.assertEqual(
            apps["config"],
            ("/usr/bin/konsole", ["--hold", "-e", "/usr/bin/linxira-config", "help"]),
        )
        self.assertIn("QProcess.startDetached(executable, arguments)", self.source)

    def test_has_no_privileged_shell_or_package_transaction_path(self):
        for forbidden in (
            "shell=True",
            "bash -c",
            "sh -c",
            "sudo",
            "pkexec",
            "pacman",
            '"mirror"',
            '"runtime"',
            '"conda"',
        ):
            self.assertNotIn(forbidden, self.source)

    def test_does_not_reproduce_catalog_application_cards(self):
        self.assertNotIn('self.catalog.get("applications", [])', self.source)
        self.assertNotIn("application_count", self.source)
        self.assertNotIn("open_shelly", self.source)

    def test_installed_home_exposes_health_and_completion_states(self):
        self.assertIn('self.tr("health")', self.source)
        self.assertIn('self.tr("first_completion")', self.source)
        self.assertIn('receipt_status in ("installed", "none")', self.source)
        self.assertIn('receipt_status == "deferred"', self.source)

    def test_all_translations_cover_the_reduced_surface(self):
        required = {
            "home", "status", "help", "install", "launchers",
            "open_software", "open_components", "open_config", "open_settings",
            "open_update", "open_gaming", "open_recovery", "available_updates", "last_update_check", "reboot_required",
            "yes", "no", "unknown",
            "health", "health_ready", "health_attention", "first_completion",
            "completion_complete", "completion_pending", "completion_unknown",
            "workstation_status", "selection", "docs", "show_login", "launch_error",
        }
        translations = sorted(I18N.glob("*.json"))
        self.assertEqual(len(translations), 9)
        for path in translations:
            document = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(required.issubset(document), path.name)

    def test_reads_the_updater_status_contract(self):
        self.assertIn("LINXIRA_UPDATE_STATUS_PATH", self.source)
        self.assertIn('"available_update_count"', self.source)
        self.assertIn('"last_check"', self.source)
        self.assertIn('"reboot_required"', self.source)


if __name__ == "__main__":
    unittest.main()
