#!/bin/bash
# Replace CachyOS branding with Linxira in all i18n files
set -euo pipefail

I18N_DIR="/mnt/g/Linxira-OS/_build/linxira-welcome/i18n"

echo "Updating i18n files..."

for ftl_file in "$I18N_DIR"/*/cachyos_hello.ftl; do
    lang=$(basename "$(dirname "$ftl_file")")
    echo "  Processing: $lang"

    # about-dialog-title
    sed -i 's/about-dialog-title = CachyOS/about-dialog-title = Linxira/g' "$ftl_file"
    sed -i 's/about-dialog-title = CachyOS 欢迎/about-dialog-title = Linxira 欢迎/g' "$ftl_file"

    # about-dialog-comments
    sed -i 's/about-dialog-comments = Welcome screen for CachyOS/about-dialog-comments = Welcome screen for Linxira OS/g' "$ftl_file"
    sed -i 's/about-dialog-comments = CachyOS 的欢迎界面/about-dialog-comments = Linxira OS 的欢迎界面/g' "$ftl_file"
    sed -i 's/about-dialog-comments = Écran de bienvenue pour CachyOS/about-dialog-comments = Écran de bienvenue pour Linxira OS/g' "$ftl_file"
    sed -i 's/about-dialog-comments = Pantalla de bienvenida para CachyOS/about-dialog-comments = Pantalla de bienvenida para Linxira OS/g' "$ftl_file"
    sed -i 's/about-dialog-comments = CachyOS のようこそ画面/about-dialog-comments = Linxira OS のようこそ画面/g' "$ftl_file"
    sed -i 's/about-dialog-comments = Benvenuto schermata per CachyOS/about-dialog-comments = Benvenuto schermata per Linxira OS/g' "$ftl_file"
    sed -i 's/about-dialog-comments = Dobrodošli ekran za CachyOS/about-dialog-comments = Dobrodošli ekran za Linxira OS/g' "$ftl_file"
    sed -i 's/about-dialog-comments = Vítejte obrazovka pro CachyOS/about-dialog-comments = Vítejte obrazovka pro Linxira OS/g' "$ftl_file"
    sed -i 's/about-dialog-comments = CachyOS Hoşgeldiniz ekranı/about-dialog-comments = Linxira OS Hoşgeldiniz ekranı/g' "$ftl_file"
    sed -i 's/about-dialog-comments = CachyOS歡迎畫面/about-dialog-comments = Linxira OS歡迎畫面/g' "$ftl_file"

    # welcome-title
    sed -i 's/welcome-title = Welcome to CachyOS!/welcome-title = Welcome to Linxira OS!/g' "$ftl_file"
    sed -i 's/welcome-title = 欢迎使用 CachyOS！/welcome-title = 欢迎使用 Linxira OS！/g' "$ftl_file"
    sed -i 's/welcome-title = Bienvenue sur CachyOS !/welcome-title = Bienvenue sur Linxira OS !/g' "$ftl_file"
    sed -i 's/welcome-title = ¡Bienvenido a CachyOS!/welcome-title = ¡Bienvenido a Linxira OS!/g' "$ftl_file"
    sed -i 's/welcome-title = CachyOS へようこそ！/welcome-title = Linxira OS へようこそ！/g' "$ftl_file"
    sed -i 's/welcome-title = Benvenuto in CachyOS!/welcome-title = Benvenuto in Linxira OS!/g' "$ftl_file"
    sed -i 's/welcome-title = Dobrodošli u CachyOS!/welcome-title = Dobrodošli u Linxira OS!/g' "$ftl_file"
    sed -i 's/welcome-title = Vítejte v CachyOS!/welcome-title = Vítejte v Linxira OS!/g' "$ftl_file"
    sed -i 's/welcome-title = CachyOS Hoş Geldiniz!/welcome-title = Linxira OS Hoş Geldiniz!/g' "$ftl_file"

    # welcome-body - replace CachyOS mentions
    sed -i 's/CachyOS Developers/Linxira OS Developers/g' "$ftl_file"
    sed -i 's/CachyOS 的开发者/Linxira OS 的开发者/g' "$ftl_file"
    sed -i 's/CachyOS 开発者/Linxira OS 開発者/g' "$ftl_file"
    sed -i 's/développeurs de CachyOS/développeurs de Linxira OS/g' "$ftl_file"
    sed -i 's/desarrolladores de CachyOS/desarrolladores de Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS Entwicklern/Linxira OS Entwicklern/g' "$ftl_file"
    sed -i 's/sviluppatori di CachyOS/sviluppatori di Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS razvijaoca/Linxira OS razvijaoca/g' "$ftl_file"
    sed -i 's/vývojářů CachyOS/vývojářů Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS 开发者/Linxira OS 开发者/g' "$ftl_file"

    # welcome-body - replace CachyOS usage mentions
    sed -i 's/using CachyOS/using Linxira OS/g' "$ftl_file"
    sed -i 's/usar CachyOS/usar Linxira OS/g' "$ftl_file"
    sed -i 's/utiliser CachyOS/utiliser Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS を使用する/Linxira OS を使用する/g' "$ftl_file"
    sed -i 's/usare CachyOS/usare Linxira OS/g' "$ftl_file"
    sed -i 's/koristiti CachyOS/koristiti Linxira OS/g' "$ftl_file"
    sed -i 's/používat CachyOS/používat Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS kullanmak/Linxira OS kullanmak/g' "$ftl_file"
    sed -i 's/使用 CachyOS/使用 Linxira OS/g' "$ftl_file"

    # welcome-body - replace building mentions
    sed -i 's/enjoy building it/enjoy building it/g' "$ftl_file"
    sed -i 's/aus der Entwicklung/aus der Entwicklung/g' "$ftl_file"

    # outdated-version-warning
    sed -i 's/older version of CachyOS ISO/older version of Linxira OS ISO/g' "$ftl_file"
    sed -i 's/CachyOS 的一个旧版 ISO/Linxira OS 的一个旧版 ISO/g' "$ftl_file"
    sed -i 's/une ancienne version de CachyOS/une ancienne version de Linxira OS/g' "$ftl_file"
    sed -i 's/una versión antigua de CachyOS/una versión antigua de Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS の古いバージョン/Linxira OS の古いバージョン/g' "$ftl_file"
    sed -i 's/una versione vecchia di CachyOS/una versione vecchia di Linxira OS/g' "$ftl_file"
    sed -i 's/staru verziju CachyOS/staru verziju Linxira OS/g' "$ftl_file"
    sed -i 's/starou verzi CachyOS/starou verzi Linxira OS/g' "$ftl_file"
    sed -i 's/eski bir CachyOS/eski bir Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS 的旧版/Linxira OS 的旧版/g' "$ftl_file"

    # testing-iso-warning - replace CachyOS mentions
    sed -i 's/testing CachyOS/testing Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS 的测试/Linxira OS 的测试/g' "$ftl_file"
    sed -i 's/CachyOS のテスト版/Linxira OS のテスト版/g' "$ftl_file"
    sed -i 's/CachyOS Test/Linxira OS Test/g' "$ftl_file"
    sed -i 's/test de CachyOS/test de Linxira OS/g' "$ftl_file"
    sed -i 's/pruebas de CachyOS/pruebas de Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS テスト/Linxira OS テスト/g' "$ftl_file"
    sed -i 's/test di CachyOS/test di Linxira OS/g' "$ftl_file"
    sed -i 's/test CachyOS/test Linxira OS/g' "$ftl_file"
    sed -i 's/testovací CachyOS/testovací Linxira OS/g' "$ftl_file"
    sed -i 's/test CachyOS/test Linxira OS/g' "$ftl_file"
    sed -i 's/CachyOS 的测试版/Linxira OS 的测试版/g' "$ftl_file"

    # Any remaining CachyOS mentions
    sed -i 's/CachyOS/Linxira OS/g' "$ftl_file"
done

echo "Done! Updated all $(ls "$I18N_DIR"/*/cachyos_hello.ftl 2>/dev/null | wc -l) language files."
