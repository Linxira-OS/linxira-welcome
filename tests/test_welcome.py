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
            {"installer", "shelly", "package_center", "component_manager", "config", "settings", "update", "gaming", "hardware", "recovery"},
        )
        self.assertEqual(apps["shelly"], ("/usr/bin/shelly-ui", []))
        self.assertEqual(apps["package_center"], ("/usr/bin/linxira-package-center", []))
        self.assertEqual(apps["component_manager"], ("/usr/bin/linxira-component-manager", []))
        self.assertEqual(apps["update"], ("/usr/bin/linxira-update", []))
        self.assertEqual(apps["gaming"], ("/usr/bin/linxira-gaming-manager", []))
        self.assertEqual(apps["hardware"], ("/usr/bin/linxira-hardware-driver-manager", []))
        self.assertEqual(apps["recovery"], ("/usr/bin/linxira-recovery-diagnostics-gui", []))
        self.assertEqual(
            apps["config"],
            ("/usr/bin/konsole", ["--hold", "-e", "/usr/bin/linxira-config", "status"]),
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
            "open_shelly", "open_software", "open_components", "open_config", "open_settings",
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
