# linxira-welcome · Agent 开发规范

> **档位**:A · 系统源仓
> **本仓职责**:面向 Linxira OS 的 Plasma 原生状态与路由界面,读取版本化 catalog 与安装回执,
> 暴露固定的桌面工具与项目资源入口。
> 通用约束见工作区总纲 `f:\Linxira-OS\AGENTS.md` 与发布规范 `linxira-os/docs/RELEASE_STANDARD.md`;
> 本文只写本仓特有内容。

## 职责与边界

- **不列出可安装软件**,不执行 shell 字符串、包事务、`sudo` 或 `pkexec`。
- 三页遵循 Phase 1 产品边界:
  - **Home**:Live 环境把"安装"作为主操作;已安装系统显示由只读 catalog 与安装回执派生的健康度与首启完成态。
  - **Status**:展示 release、内核、网络、catalog、回执与安装选择元数据。
  - **Help**:提供已复核文档链接与登录偏好。
- Home 暴露**固定**工具启动器:Shelly、Quick System Software Setup、Quick System Runtime Setup、
  Konsole 中的 Config CLI、System Settings 及已安装的系统维护工具;这些入口由各自产品拥有,Welcome 不复刻其清单。
- **消费 `linxira-hooks` 的 reboot-required 状态**:`linxira-hooks` 在升级后写
  `/var/lib/linxira/reboot-required` 标记,Welcome 作为只读消费方据此提示重启(不强制重启)。
- 可选启动目标仅在其固定可执行文件存在时才启用;Welcome 以**固定可执行文件 + 固定 argv** 启动,
  永不构造或执行 shell 字符串。
- 运行时依赖:Python 3、PySide6、`/usr/share/linxira/catalog/` 下的 catalog v2。

## 目录布局

- `src/linxira-welcome`:应用入口脚本(无 `pyproject.toml`)
- `data/org.linxira.Welcome.desktop`(菜单入口)、`data/autostart/org.linxira.Welcome.desktop`(Plasma 登录入口)
- `data/org.linxira.Welcome.metainfo.xml`
- `data/i18n/*.json`:已复核 UI 翻译(en 兜底),当前含 en、zh_CN、zh_TW、de、es、fr、ja、ko、pt_BR、ru
- `tests/test_welcome.py`(源码边界与翻译契约)、`tests/test_about_metadata.py`
- 无 `pyproject.toml`:以 `src/linxira-welcome` 单脚本 + `data/` 资源方式交付

## 本地校验

CI(分支 `main` / `master`,python 3.13):

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src
```

## 版本与发布

- 版本唯一来源是本仓根 `VERSION`(当前 `1.0.5`)。
- 改 `VERSION` 触发 `.github/workflows/release.yml`(分支 `main`)自动建 Release,进入 `[linxira]` 全自动链。**禁止手工 bump**。

## 禁区

- 不得在 Welcome 内新增安装/卸载、包事务或 shell 字符串执行;不得复制其他产品的应用/运行时清单。
- 启动外部程序必须保持固定可执行文件 + 固定 argv,且仅在其存在时启用。
- autostart 须尊重用户 "Show Welcome at login" 设置;Live ISO 用临时 profile(每次新 Live 启动即打开)。
- 不引入 `cachyos` / `aur` / `seafoam`;不直接 `sudo`/`su`/`doas`/`run0`;不 `git add -A`。