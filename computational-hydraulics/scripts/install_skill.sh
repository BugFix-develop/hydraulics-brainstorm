#!/usr/bin/env bash
# ==============================================================================
# Скрипт автоматической установки навыка computational-hydraulics
# для различных AI-агентов и сред разработки (Antigravity, Claude, Cursor, etc.)
# Кафедра ИСИТ / РГУ нефти и газа им. И.М. Губкина
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "================================================================="
echo "   Установка AI Skill: computational-hydraulics"
echo "   Каталог навыка: ${SKILL_DIR}"
echo "================================================================="

install_antigravity() {
    local target_dir="${HOME}/.agents/skills/computational-hydraulics"
    echo "-> Установка для Google Antigravity & Open Agent Skills..."
    mkdir -p "${HOME}/.agents/skills"
    rm -rf "${target_dir}"
    cp -r "${SKILL_DIR}" "${target_dir}"
    echo "   [OK] Установлено в: ${target_dir}"
}

install_claude() {
    local target_dir="${HOME}/.claude/skills/computational-hydraulics"
    echo "-> Установка для Claude Code (Anthropic CLI)..."
    mkdir -p "${HOME}/.claude/skills"
    rm -rf "${target_dir}"
    cp -r "${SKILL_DIR}" "${target_dir}"
    
    # Добавление ссылки в глобальный CLAUDE.md
    local claude_md="${HOME}/.claude/CLAUDE.md"
    if [ ! -f "${claude_md}" ] || ! grep -q "computational-hydraulics" "${claude_md}" 2>/dev/null; then
        echo -e "\n# Computational Hydraulics Skill\nAlways refer to ${target_dir}/SKILL.md when solving pipeline hydraulics, TGC circuits, and C++ numerical tasks.\n" >> "${claude_md}"
    fi
    echo "   [OK] Установлено в: ${target_dir}"
    echo "   [OK] Обновлен глобальный: ${claude_md}"
}

install_cursor() {
    local project_dir="${1:-.}"
    echo "-> Настройка для Cursor AI в каталоге: ${project_dir}..."
    local rules_dir="${project_dir}/.cursor/rules"
    mkdir -p "${rules_dir}"
    cat << 'EOF' > "${rules_dir}/hydraulics.mdc"
---
description: Computational hydraulics, Eigen linear systems, and strict 3-stage agentic workflow
globs: src/**/*.cpp, src/**/*.h, tests/**/*.cpp, docs/**/*.md
---

# Computational Hydraulics & Agentic Development Protocol
Strictly adhere to the following rules:
1. Always follow the 3-stage protocol: ТЗ (docs/<n>_<topic>.md) -> Architecture (docs/<n>_<topic>_architecture.md) -> Plan (docs/<n>_<topic>_plan.md).
2. Never vibe-code C++ without approved ТЗ and Architecture.
3. Eigen: NEVER use `A.inverse() * b`. Always use `PartialPivLU` or `FullPivLU`.
4. Git: NEVER execute `git commit` or `git push` automatically. The developer commits manually.
5. Code style: snake_case, structs end with `_t`, concise 1-line Doxygen comments with SI units in brackets.
6. Verify against GoogleTest with non-tautological analytical benchmarks.
EOF
    echo "   [OK] Создан файл правил: ${rules_dir}/hydraulics.mdc"
}

install_windsurf() {
    local project_dir="${1:-.}"
    echo "-> Настройка для Windsurf (Codeium) в: ${project_dir}..."
    if [ -f "${SKILL_DIR}/templates/AGENTS.md" ]; then
        cp "${SKILL_DIR}/templates/AGENTS.md" "${project_dir}/.windsurfrules"
        echo "   [OK] Создан файл: ${project_dir}/.windsurfrules"
    fi
}

install_cline() {
    local project_dir="${1:-.}"
    echo "-> Настройка для Cline & Roo Code в: ${project_dir}..."
    if [ -f "${SKILL_DIR}/templates/AGENTS.md" ]; then
        cp "${SKILL_DIR}/templates/AGENTS.md" "${project_dir}/.clinerules"
        echo "   [OK] Создан файл: ${project_dir}/.clinerules"
    fi
}

install_aider() {
    echo "-> Настройка для Aider CLI..."
    local aider_conf="${HOME}/.aider.conf.yml"
    local skill_path="${HOME}/.agents/skills/computational-hydraulics/SKILL.md"
    if [ ! -f "${skill_path}" ]; then
        install_antigravity
    fi
    if [ ! -f "${aider_conf}" ] || ! grep -q "computational-hydraulics" "${aider_conf}" 2>/dev/null; then
        echo -e "\nread:\n  - ${skill_path}\n" >> "${aider_conf}"
    fi
    echo "   [OK] Обновлен конфигурационный файл: ${aider_conf}"
}

install_copilot() {
    local project_dir="${1:-.}"
    echo "-> Настройка для GitHub Copilot в: ${project_dir}..."
    mkdir -p "${project_dir}/.github"
    if [ -f "${SKILL_DIR}/templates/AGENTS.md" ]; then
        cp "${SKILL_DIR}/templates/AGENTS.md" "${project_dir}/.github/copilot-instructions.md"
        echo "   [OK] Создан файл: ${project_dir}/.github/copilot-instructions.md"
    fi
}

install_all() {
    echo "-> Установка для всех поддерживаемых сред..."
    install_antigravity
    install_claude
    install_aider
    install_cursor "."
    install_windsurf "."
    install_cline "."
    install_copilot "."
    echo "================================================================="
    echo "   [УСПЕХ] Все глобальные и локальные конфигурации обновлены!"
    echo "================================================================="
}

# Обработка аргументов командной строки
TARGET="${1:-menu}"

case "${TARGET}" in
    --all|all)
        install_all
        ;;
    --antigravity|antigravity)
        install_antigravity
        ;;
    --claude|claude)
        install_claude
        ;;
    --cursor|cursor)
        install_cursor "${2:-.}"
        ;;
    --windsurf|windsurf)
        install_windsurf "${2:-.}"
        ;;
    --cline|cline|roo)
        install_cline "${2:-.}"
        ;;
    --aider|aider)
        install_aider
        ;;
    --copilot|copilot)
        install_copilot "${2:-.}"
        ;;
    menu|*)
        echo "Выберите среду для установки:"
        echo "  1) Google Antigravity & Open Agent Skills (~/.agents/skills/)"
        echo "  2) Claude Code CLI (~/.claude/skills/ & CLAUDE.md)"
        echo "  3) Cursor AI IDE (.cursor/rules/hydraulics.mdc)"
        echo "  4) Windsurf (.windsurfrules)"
        echo "  5) Cline & Roo Code (.clinerules)"
        echo "  6) Aider CLI (~/.aider.conf.yml)"
        echo "  7) GitHub Copilot (.github/copilot-instructions.md)"
        echo "  8) Установить для всех сред (All-in-one)"
        echo "  q) Выход"
        echo ""
        read -rp "Введите номер [1-8]: " choice
        case "${choice}" in
            1) install_antigravity ;;
            2) install_claude ;;
            3) install_cursor "." ;;
            4) install_windsurf "." ;;
            5) install_cline "." ;;
            6) install_aider ;;
            7) install_copilot "." ;;
            8) install_all ;;
            *) echo "Отмена." ;;
        esac
        ;;
esac
