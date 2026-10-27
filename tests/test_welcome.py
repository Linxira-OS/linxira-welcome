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

    def test_has_home_status_terminal_system_and_help_pages(self):
        self.assertIn("self._home_page()", self.source)
        self.assertIn("self._status_page()", self.source)
        self.assertIn("self._terminal_page()", self.source)
        self.assertIn("self._system_page()", self.source)
        self.assertIn("self._help_page()", self.source)
        self.assertIn('.tr("terminal")', self.source)
        for removed in (
            "_setup_page",
            "_software_page",
            "_sources_page",
            "_resources_page",
        ):
            self.assertNotIn(removed, self.source)

    def test_terminal_page_lists_bash_then_alphabetic_shells(self):
        choices = assignment_value(self.source, "SHELL_CHOICES")
        self.assertEqual([entry[0] for entry in choices], ["bash", "fish", "nushell", "zsh"])
        self.assertIsNone(choices[0][3])
        self.assertEqual(
            [entry[3] for entry in choices[1:]],
            ["component-fish", "component-nushell", "component-zsh"],
        )
        self.assertIn('["--select", leaf_id]', self.source)
        self.assertIn("chsh -s {path}", self.source)

    def test_uses_only_the_fixed_product_launchers(self):
        apps = assignment_value(self.source, "APPS")
        self.assertEqual(
            set(apps),
            {"installer", "shelly", "package_center", "component_manager", "config", "settings", "update", "gaming", "hardware", "recovery", "terminal"},
        )
        self.assertEqual(apps["shelly"], ("/usr/bin/shelly-ui", []))
        self.assertEqual(apps["package_center"], ("/usr/bin/linxira-package-center", []))
        self.assertEqual(apps["component_manager"], ("/usr/bin/linxira-component-manager", []))
        self.assertEqual(apps["update"], ("/usr/bin/linxira-update", ["--launch"]))
        self.assertEqual(apps["gaming"], ("/usr/bin/linxira-gaming-manager", []))
        self.assertEqual(apps["hardware"], ("/usr/bin/linxira-hardware-driver-manager", []))
        self.assertEqual(apps["recovery"], ("/usr/bin/linxira-recovery-diagnostics-gui", []))
        self.assertEqual(apps["terminal"], ("/usr/bin/cosmic-term", []))
        self.assertEqual(apps["settings"], ("/usr/bin/cosmic-settings", "/usr/bin/systemsettings"))
        self.assertEqual(
            apps["config"],
            ("/usr/bin/konsole", ["--hold", "-e", "/usr/bin/linxira-config"]),
        )
        self.assertIn("QProcess.startDetached(executable, list(arguments))", self.source)
        self.assertIn(
            '"/usr/bin/cosmic-term": ("-e",)',
            self.source,
        )
        self.assertIn(
            '"/usr/bin/konsole": ("--hold", "-e")',
            self.source,
        )
        self.assertIn(
            '"/usr/bin/xterm": ("-hold", "-e")',
            self.source,
        )
        self.assertIn("if app in (\"terminal\", \"config\"):", self.source)

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
        self.assertIn("open_shelly", self.source)

    def test_installed_home_exposes_health_and_completion_states(self):
        self.assertIn('self.tr("health")', self.source)
        self.assertIn('self.tr("first_completion")', self.source)
        self.assertIn('receipt_status in ("installed", "none")', self.source)
        # 2026-09-20: 回执恒为 "installed", 延后完成状态由显式延后条目推导;
        # 原死代码分支 status=="deferred" 移除。
        self.assertNotIn('receipt_status == "deferred"', self.source)
        self.assertIn('_deferred_component_count', self.source)
        self.assertIn('"explicitly-deferred"', self.source)

    def test_reads_catalog_v3_before_legacy_v2(self):
        # 2026-09-20: v3 镜像只装 catalog-v3.json, 旧默认 v2 路径导致
        # 健康状态恒为"需要关注"; 现在优先 v3, 保留 v2 回退。
        self.assertIn("CATALOG_PATHS", self.source)
        self.assertIn('"/usr/share/linxira/catalog/catalog-v3.json"', self.source)
        self.assertIn('Path("/usr/share/linxira/catalog/catalog-v2.json")', self.source)
        self.assertNotIn('catalog/catalog-v2.json"\n    )\n)', self.source)

    def test_component_deferred_banner_is_wired_and_translated(self):
        for key in (
            "component_deferred_title",
            "component_deferred_body",
            "component_deferred_continue",
        ):
            self.assertIn(f'"{key}"', self.source)
            for path in sorted(I18N.glob("zh_*.json")):
                document = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn(key, document, path.name)
        self.assertIn('"component_manager"', self.source)

    def test_all_translations_cover_the_reduced_surface(self):
        required = {
            "home", "status", "help", "install", "launchers",
            "open_shelly", "open_terminal", "open_software", "open_components", "open_config", "open_settings",
            "open_update", "open_gaming", "open_hardware", "open_recovery", "available_updates", "last_update_check", "reboot_required",
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


class SystemPageTests(unittest.TestCase):
    """The System page is an entry point only: it reads the capability manifest
    and opens linxira-config; it never mutates the system itself."""

    @classmethod
    def setUpClass(cls):
        cls.source = WELCOME.read_text(encoding="utf-8")

    def test_reads_the_capability_manifest(self):
        self.assertIn("CAPABILITIES_PATH", self.source)
        self.assertIn('"/usr/share/linxira/agent/capabilities.json"', self.source)
        self.assertIn('document.get("commands")', self.source)
        self.assertIn('meta.get("scope", "any")', self.source)

    def test_filters_entries_by_hardware_scope(self):
        self.assertIn('scope = "laptop" if self._is_laptop() else "desktop"', self.source)
        self.assertIn('if wanted not in ("any", scope):', self.source)
        self.assertIn("/sys/class/dmi/id/chassis_type", self.source)
        self.assertIn('glob("BAT*")', self.source)

    def test_never_runs_mutating_entries(self):
        self.assertIn('if command.get("mutating") and meta.get("allow_mutating") is not True:', self.source)
        self.assertIn('self._launch_app("config", label)', self.source)

    def test_system_keys_are_translated(self):
        required = {
            "system", "system_body", "system_unavailable", "system_config_missing",
            "open_power", "open_remote", "open_security", "open_network",
            "open_mirrors", "open_runtime", "open_logs",
        }
        for path in sorted(I18N.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(required.issubset(document), path.name)

    def test_synthetic_battery_in_a_vm_is_not_a_laptop(self):
        self.assertIn("_is_virtual_machine", self.source)
        self.assertIn('if self._is_virtual_machine():', self.source)
        self.assertIn('"Microsoft Corporation"', self.source)
