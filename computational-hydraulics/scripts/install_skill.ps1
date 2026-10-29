# ==============================================================================
# Скрипт автоматической установки навыка computational-hydraulics для Windows
# Кафедра ИСИТ / РГУ нефти и газа им. И.М. Губкина
# ==============================================================================

param(
    [string]$Target = "menu"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "   Установка AI Skill: computational-hydraulics (Windows)" -ForegroundColor Cyan
Write-Host "   Каталог навыка: $SkillDir" -ForegroundColor Gray
Write-Host "=================================================================" -ForegroundColor Cyan

function Install-Codex {
    $targetDir = Join-Path $HOME ".codex\skills\computational-hydraulics"
    Write-Host "-> Установка для OpenAI Codex Agent..." -ForegroundColor Green
    New-Item -ItemType Directory -Force -Path (Join-Path $HOME ".codex\skills") | Out-Null
    if (Test-Path $targetDir) { Remove-Item -Recurse -Force $targetDir }
    Copy-Item -Recurse -Force $SkillDir $targetDir
    Write-Host "   [OK] Установлено в: $targetDir" -ForegroundColor Green
}

function Install-Antigravity {
    $targetDir = Join-Path $HOME ".agents\skills\computational-hydraulics"
    Write-Host "-> Установка для Google Antigravity & Open Agent Skills..." -ForegroundColor Blue
    New-Item -ItemType Directory -Force -Path (Join-Path $HOME ".agents\skills") | Out-Null
    if (Test-Path $targetDir) { Remove-Item -Recurse -Force $targetDir }
    Copy-Item -Recurse -Force $SkillDir $targetDir
    Write-Host "   [OK] Установлено в: $targetDir" -ForegroundColor Green
}

function Install-Claude {
    $targetDir = Join-Path $HOME ".claude\skills\computational-hydraulics"
    Write-Host "-> Установка для Anthropic Claude Code CLI..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path (Join-Path $HOME ".claude\skills") | Out-Null
    if (Test-Path $targetDir) { Remove-Item -Recurse -Force $targetDir }
    Copy-Item -Recurse -Force $SkillDir $targetDir
    
    $claudeMd = Join-Path $HOME ".claude\CLAUDE.md"
    $directive = "`n# Computational Hydraulics Skill`nAlways refer to $targetDir\SKILL.md when solving hydraulics tasks.`n"
    if (!(Test-Path $claudeMd) -or !(Select-String -Path $claudeMd -Pattern "computational-hydraulics" -Quiet)) {
        Add-Content -Path $claudeMd -Value $directive
    }
    Write-Host "   [OK] Установлено в: $targetDir" -ForegroundColor Green
    Write-Host "   [OK] Обновлен: $claudeMd" -ForegroundColor Green
}

function Install-Cursor {
    param([string]$ProjectDir = ".")
    Write-Host "-> Настройка для Cursor AI..." -ForegroundColor Magenta
    $rulesDir = Join-Path $ProjectDir ".cursor\rules"
    New-Item -ItemType Directory -Force -Path $rulesDir | Out-Null
    $content = @"
---
description: Computational hydraulics, Eigen linear systems, and strict 3-stage agentic workflow
globs: src/**/*.cpp, src/**/*.h, tests/**/*.cpp, docs/**/*.md
---

# Computational Hydraulics & Agentic Protocol
Strictly follow rules in ~/.agents/skills/computational-hydraulics/SKILL.md:
1. Follow 3-stage protocol: ТЗ -> Architecture -> Plan -> GoogleTests.
2. Eigen: NEVER use `A.inverse() * b`. Use PartialPivLU or FullPivLU.
3. Git: NEVER commit or push automatically. Developer commits manually.
4. Code style: snake_case, structs end with `_t`, concise 1-line Doxygen comments with SI units.
"@
    Set-Content -Path (Join-Path $rulesDir "hydraulics.mdc") -Value $content -Encoding UTF8
    Write-Host "   [OK] Создан файл: $rulesDir\hydraulics.mdc" -ForegroundColor Green
}

function Install-Windsurf {
    param([string]$ProjectDir = ".")
    Write-Host "-> Настройка для Windsurf (Codeium)..." -ForegroundColor Cyan
    $agentsMd = Join-Path $SkillDir "templates\AGENTS.md"
    if (Test-Path $agentsMd) {
        Copy-Item -Force $agentsMd (Join-Path $ProjectDir ".windsurfrules")
        Write-Host "   [OK] Создан файл: $ProjectDir\.windsurfrules" -ForegroundColor Green
    }
}

function Install-Cline {
    param([string]$ProjectDir = ".")
    Write-Host "-> Настройка для Roo Code & Cline..." -ForegroundColor Blue
    $agentsMd = Join-Path $SkillDir "templates\AGENTS.md"
    if (Test-Path $agentsMd) {
        Copy-Item -Force $agentsMd (Join-Path $ProjectDir ".clinerules")
        Write-Host "   [OK] Создан файл: $ProjectDir\.clinerules" -ForegroundColor Green
    }
}

function Install-Aider {
    Write-Host "-> Настройка для Aider CLI..." -ForegroundColor Gray
    $aiderConf = Join-Path $HOME ".aider.conf.yml"
    $skillPath = Join-Path $HOME ".agents\skills\computational-hydraulics\SKILL.md"
    if (!(Test-Path $skillPath)) { Install-Antigravity }
    $directive = "`nread:`n  - $skillPath`n"
    if (!(Test-Path $aiderConf) -or !(Select-String -Path $aiderConf -Pattern "computational-hydraulics" -Quiet)) {
        Add-Content -Path $aiderConf -Value $directive
    }
    Write-Host "   [OK] Обновлен конфиг: $aiderConf" -ForegroundColor Green
}

function Install-Copilot {
    param([string]$ProjectDir = ".")
    Write-Host "-> Настройка для GitHub Copilot..." -ForegroundColor White
    $githubDir = Join-Path $ProjectDir ".github"
    New-Item -ItemType Directory -Force -Path $githubDir | Out-Null
    $agentsMd = Join-Path $SkillDir "templates\AGENTS.md"
    if (Test-Path $agentsMd) {
        Copy-Item -Force $agentsMd (Join-Path $githubDir "copilot-instructions.md")
        Write-Host "   [OK] Создан файл: $githubDir\copilot-instructions.md" -ForegroundColor Green
    }
}

function Install-All {
    Install-Codex
    Install-Antigravity
    Install-Claude
    Install-Aider
    Install-Cursor "."
    Install-Windsurf "."
    Install-Cline "."
    Install-Copilot "."
    Write-Host "=================================================================" -ForegroundColor Green
    Write-Host "   [УСПЕХ] Все конфигурации для Windows успешно установлены!" -ForegroundColor Green
    Write-Host "=================================================================" -ForegroundColor Green
}

switch ($Target.ToLower()) {
    "--all" { Install-All }
    "all" { Install-All }
    "--codex" { Install-Codex }
    "codex" { Install-Codex }
    "--antigravity" { Install-Antigravity }
    "antigravity" { Install-Antigravity }
    "--claude" { Install-Claude }
    "claude" { Install-Claude }
    "--cursor" { Install-Cursor "." }
    "cursor" { Install-Cursor "." }
    "--windsurf" { Install-Windsurf "." }
    "windsurf" { Install-Windsurf "." }
    "--cline" { Install-Cline "." }
    "cline" { Install-Cline "." }
    "--aider" { Install-Aider }
    "aider" { Install-Aider }
    "--copilot" { Install-Copilot "." }
    "copilot" { Install-Copilot "." }
    default {
        Write-Host "Выберите среду для установки:"
        Write-Host "  1) OpenAI Codex Agent (~/.codex/skills/)"
        Write-Host "  2) Google Antigravity (~/.agents/skills/)"
        Write-Host "  3) Anthropic Claude Code CLI (~/.claude/skills/)"
        Write-Host "  4) Cursor AI IDE (.cursor/rules/hydraulics.mdc)"
        Write-Host "  5) Windsurf (.windsurfrules)"
        Write-Host "  6) Roo Code & Cline (.clinerules)"
        Write-Host "  7) Aider CLI (~/.aider.conf.yml)"
        Write-Host "  8) GitHub Copilot (.github/copilot-instructions.md)"
        Write-Host "  9) Установить для всех сред (All-in-one)"
        Write-Host "  q) Выход"
        $choice = Read-Host "Введите номер [1-9]"
        switch ($choice) {
            "1" { Install-Codex }
            "2" { Install-Antigravity }
            "3" { Install-Claude }
            "4" { Install-Cursor "." }
            "5" { Install-Windsurf "." }
            "6" { Install-Cline "." }
            "7" { Install-Aider }
            "8" { Install-Copilot "." }
            "9" { Install-All }
            default { Write-Host "Отмена." }
        }
    }
}
