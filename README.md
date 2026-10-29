# 🌊 Computational Hydraulics Brain & AI Agent Skill
> **База знаний, архитектурные шаблоны C++ и агентский навык для курсов «Вычислительная гидравлика» и «Теория гидравлических цепей» (Кафедра ИСИТ, РГУ нефти и газа им. И.М. Губкина)**

[![C++20](https://img.shields.io/badge/C%2B%2B-20-blue.svg)](https://en.cppreference.com/w/cpp/20)
[![Eigen](https://img.shields.io/badge/Eigen-3.4%2B-green.svg)](https://gitlab.com/libeigen/eigen)
[![GoogleTest](https://img.shields.io/badge/GoogleTest-v1.14%2B-red.svg)](https://github.com/google/googletest)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## 📌 О репозитории

Данный репозиторий представляет собой законченную инженерную базу знаний и автономный специализированный навык (**AI Agent Skill** `computational-hydraulics`) для студентов и разработчиков, выполняющих лабораторные и исследовательские работы по гидравлике трубопроводных систем и расчету сложных гидравлических сетей.

Репозиторий решает главную проблему студента на 3 курсе: **лабораторные задания даются в сухом виде**, без явного раскрытия физической картины и математической постановки. Агент выступает в роли **опытного наставника и Senior C++ разработчика**:
1. Мягко разбирает с вами физическую суть и математическую модель до написания первой строчки кода.
2. Генерирует наглядные схемы, графы и структуру блочных матриц.
3. Проводит разработку по строгому **3-стадийному протоколу кафедры ИСИТ** (ТЗ $\to$ Архитектура $\to$ План $\to$ Код $\to$ GoogleTest).
4. Защищает от фатальных ошибок численных методов (сингулярность матриц, расходимость метода Ньютона, инверсия `A.inverse()`, забытый $P$-узел).
5. Проводит жесткий тренировочный прогон перед защитой лабораторной преподавателю (**Mock Defense**).

---

## 🗂 Структура репозитория

```text
hydraulics-brain/
├── README.md                           # Главное руководство и документация
├── .gitignore                          # Исключение артефактов сборки и кэшей
│
└── computational-hydraulics/           # Автономный инженерный AI Skill
    ├── SKILL.md                        # Главные инструкции агента (Сократический диалог, C++, валидация)
    ├── scripts/
    │   └── hydraulics_calculator.py    # Интерактивный CLI-калькулятор единиц, Re, lambda, потерь и гидроудара
    ├── templates/                      # Готовые шаблоны артефактов для лабораторных
    │   ├── AGENTS.md                   # Правила проекта для корня репозитория студента (Doxygen, Code Style, Git)
    │   ├── tz_template.md              # Шаблон ТЗ и физико-математической постановки
    │   ├── architecture_template.md    # Шаблон C++ архитектуры (типы, солверы, лаконичный Doxygen)
    │   └── plan_template.md            # Шаблон пошагового плана и чек-листа
    └── references/                     # Фундаментальная инженерная база знаний
        ├── hydraulics_core.md          # 1D гидравлика: плотность ρ(T,p), вязкость, Re, Дарси-Вейсбах, гидроудар
        ├── sem2_guide.md               # 2 семестр: Бернулли, QP/PP задачи, профилирование, насосы, Task-паттерн
        ├── sem3_guide.md               # 3 семестр: ТГЦ, Eigen C++, PA=LU, МУД, блочные матрицы ККТ, графы
        ├── circuits_and_agentic.md     # Теория гидравлических цепей по Южанину + Агентский протокол ИСИТ
        ├── pitfalls_and_antipatterns.md# Топ-15 критических ловушек и антипаттернов (математика и C++)
        ├── googletest_verification_guide.md # 4-уровневая пирамида GoogleTest и независимые бенчмарки
        └── mock_defense_protocol.md    # Интерактивный симулятор защиты лабораторной (4 раунда)
```

---

## 🚀 Пошаговое руководство по установке навыка

<p align="center">
  <img src="assets/logos/openai.svg" width="40" height="40" alt="OpenAI" title="OpenAI Codex & ChatGPT" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/logos/google.svg" width="40" height="40" alt="Google" title="Google Antigravity & Open Agent Skills" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/logos/claude.svg" width="40" height="40" alt="Anthropic Claude" title="Anthropic Claude Code" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/logos/cursor.svg" width="40" height="40" alt="Cursor AI" title="Cursor AI IDE" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/logos/windsurf.svg" width="40" height="40" alt="Windsurf Codeium" title="Windsurf (Codeium)" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/logos/vscode.svg" width="40" height="40" alt="Roo Code & Cline" title="Roo Code & Cline" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/logos/copilot.svg" width="40" height="40" alt="GitHub Copilot" title="GitHub Copilot" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/logos/terminal.svg" width="40" height="40" alt="Aider CLI" title="Aider Terminal CLI" />
</p>

Навык `computational-hydraulics` разработан по открытому стандарту **Open Agent Skills** и нативно поддерживается всеми ведущими средами разработки на **Linux**, **macOS** и **Windows**.

---

### Шаг 1. Получите репозиторий на свой компьютер

Перед установкой необходимо скачать файлы навыка к себе на диск:

- **Вариант А: Через Git (рекомендуется):**
  Откройте терминал (на Windows — PowerShell, на Linux/macOS — Terminal) и выполните:
  ```bash
  git clone https://github.com/BugFix-develop/hydraulics-brainstorm.git
  cd hydraulics-brainstorm
  ```

- **Вариант Б: Без Git (скачать ZIP-архив):**
  1. Нажмите зеленую кнопку **`< > Code`** в самом верху этой страницы GitHub и выберите **`Download ZIP`**.
  2. Распакуйте скачанный архив в удобную папку (например, `C:\Coding\` или в домашнюю директорию).
  3. Откройте терминал в распакованной папке `hydraulics-brainstorm`:
     - *Windows:* зажмите клавишу `Shift` + правый клик внутри папки $\to$ выберите *«Открыть окно PowerShell здесь»*.
     - *Linux / macOS:* правый клик в папке $\to$ *«Открыть в терминале»* (либо перейдите командой `cd путь/к/папке`).

---

### Шаг 2. Выберите способ установки

Выберите, как вам удобнее подключить навык: **автоматически в 1 команду** или **вручную под вашу любимую ИИ-модель**.

#### ⚡ Способ А. Автоматическая установка (в 1 клик через скрипт)
Находясь в папке `hydraulics-brainstorm`, просто запустите готовый скрипт:

- 🐧 **Linux** / 🍏 **macOS** (Bash / Zsh):
  ```bash
  ./computational-hydraulics/scripts/install_skill.sh
  ```
- 🪟 **Windows** (PowerShell):
  ```powershell
  .\computational-hydraulics\scripts\install_skill.ps1
  ```
*Скрипт откроет интерактивное меню: введите номер нужного агента (или `9`, чтобы настроить всё и сразу).*

*(Также поддерживаются флаги тихого режима: `--codex`, `--antigravity`, `--claude`, `--cursor`, `--windsurf`, `--cline`, `--aider`, `--copilot`, `--all`).*

---

#### 📦 Способ Б. Ручная установка под каждого агента

Каждый ИИ-агент хранит навыки в своей системной папке на вашем компьютере. Разверните спойлер нужной программы и скопируйте команды для вашей ОС:

<details open>
<summary><img src="assets/logos/openai.svg" width="24" height="24" align="center" /> &nbsp;<b><font size="+1">OpenAI (Codex Agent & ChatGPT)</font></b></summary>

#### OpenAI Codex Agent (автономный агент разработки)
Копирует папку навыка в системный каталог `.codex/skills/`:

- 🐧 **Linux** / 🍏 **macOS** (Bash / Zsh):
  ```bash
  mkdir -p ~/.codex/skills
  cp -r computational-hydraulics ~/.codex/skills/
  ```
- 🪟 **Windows** (PowerShell):
  ```powershell
  New-Item -ItemType Directory -Force -Path "$HOME\.codex\skills"
  Copy-Item -Recurse -Force computational-hydraulics "$HOME\.codex\skills\"
  ```

#### OpenAI ChatGPT (Web / Plus / Team / Projects / Custom GPTs)
- **В ChatGPT Projects (на chatgpt.com):** создайте проект *«Вычислительная гидравлика»*, вставьте в поле *Custom Instructions* текст из [`computational-hydraulics/SKILL.md`](computational-hydraulics/SKILL.md), а в раздел *Files / Knowledge* загрузите файлы из [`computational-hydraulics/references/`](computational-hydraulics/references/).
- **В Custom GPT (GPT Builder):** укажите имя «Губкинский Гидравлик», вставьте инструкции из `SKILL.md` и прикрепите файлы базы знаний и калькулятор `hydraulics_calculator.py`.
</details>

<details>
<summary><img src="assets/logos/google.svg" width="24" height="24" align="center" /> &nbsp;<b><font size="+1">Google Antigravity & Open Agent Skills</font></b></summary>

Автоматически считывает навыки из стандартной глобальной папки `~/.agents/skills/`:

- 🐧 **Linux** / 🍏 **macOS** (Bash / Zsh):
  ```bash
  # Глобально для всех проектов пользователя
  mkdir -p ~/.agents/skills
  cp -r computational-hydraulics ~/.agents/skills/

  # Или локально в репозиторий с лабораторной
  mkdir -p /path/to/my-lab/.agents/skills
  cp -r computational-hydraulics /path/to/my-lab/.agents/skills/
  cp computational-hydraulics/templates/AGENTS.md /path/to/my-lab/AGENTS.md
  ```
- 🪟 **Windows** (PowerShell):
  ```powershell
  # Глобально для всех проектов пользователя
  New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills"
  Copy-Item -Recurse -Force computational-hydraulics "$HOME\.agents\skills\"

  # Или локально в репозиторий с лабораторной
  New-Item -ItemType Directory -Force -Path "C:\path\to\my-lab\.agents\skills"
  Copy-Item -Recurse -Force computational-hydraulics "C:\path\to\my-lab\.agents\skills\"
  Copy-Item -Force computational-hydraulics\templates\AGENTS.md "C:\path\to\my-lab\AGENTS.md"
  ```
</details>

<details>
<summary><img src="assets/logos/claude.svg" width="24" height="24" align="center" /> &nbsp;<b><font size="+1">Anthropic Claude Code (CLI)</font></b></summary>

Считывает инструкции из глобального файла `CLAUDE.md` или локального файла проекта:

- 🐧 **Linux** / 🍏 **macOS** (Bash / Zsh):
  ```bash
  # Глобальная установка
  mkdir -p ~/.claude/skills
  cp -r computational-hydraulics ~/.claude/skills/
  echo -e "\n# Computational Hydraulics Skill\nAlways refer to ~/.claude/skills/computational-hydraulics/SKILL.md when solving pipeline hydraulics, TGC circuits, and C++ numerical tasks.\n" >> ~/.claude/CLAUDE.md

  # Или в проект с лабораторной
  cp computational-hydraulics/templates/AGENTS.md /path/to/my-lab/CLAUDE.md
  ```
- 🪟 **Windows** (PowerShell):
  ```powershell
  # Глобальная установка
  New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills"
  Copy-Item -Recurse -Force computational-hydraulics "$HOME\.claude\skills\"
  Add-Content -Path "$HOME\.claude\CLAUDE.md" -Value "`n# Computational Hydraulics Skill`nAlways refer to $HOME\.claude\skills\computational-hydraulics\SKILL.md when solving hydraulics tasks.`n"

  # Или в проект с лабораторной
  Copy-Item -Force computational-hydraulics\templates\AGENTS.md "C:\path\to\my-lab\CLAUDE.md"
  ```
</details>

<details>
<summary><img src="assets/logos/cursor.svg" width="24" height="24" align="center" /> &nbsp;<b><font size="+1">Cursor AI IDE (Cursor Rules 2.0)</font></b></summary>

Поддерживает современные проектные правила в каталоге `.cursor/rules/*.mdc`:

- 🐧 **Linux** / 🍏 **macOS** (Bash / Zsh):
  ```bash
  mkdir -p /path/to/my-lab/.cursor/rules
  ```
- 🪟 **Windows** (PowerShell):
  ```powershell
  New-Item -ItemType Directory -Force -Path "C:\path\to\my-lab\.cursor\rules"
  ```

Создайте файл `.cursor/rules/hydraulics.mdc`:
```yaml
---
description: Computational hydraulics, Eigen linear systems, and strict 3-stage agentic workflow
globs: src/**/*.cpp, src/**/*.h, tests/**/*.cpp, docs/**/*.md
---

# Computational Hydraulics & Agentic Protocol
Strictly follow rules in ~/.agents/skills/computational-hydraulics/SKILL.md:
1. Follow the 3-stage protocol: ТЗ -> Architecture -> Plan -> GoogleTests.
2. Eigen: NEVER use `A.inverse() * b`. Use PartialPivLU or FullPivLU.
3. Git: NEVER commit or push automatically. Developer commits manually.
4. Code style: snake_case, structs end with `_t`, concise 1-line Doxygen comments with SI units.
```

*(Или скопируйте файл правил `computational-hydraulics/templates/AGENTS.md` как `.cursorrules` в корень репозитория).*
</details>

<details>
<summary><img src="assets/logos/windsurf.svg" width="24" height="24" align="center" /> &nbsp;<b><font size="+1">Windsurf (Codeium)</font></b></summary>

- 🐧 **Linux** / 🍏 **macOS** (Bash / Zsh):
  ```bash
  # В проект с лабораторной
  cp computational-hydraulics/templates/AGENTS.md /path/to/my-lab/.windsurfrules

  # Или глобально для всех проектов
  echo -e "\nInclude and strictly obey instructions from ~/.agents/skills/computational-hydraulics/SKILL.md\n" >> ~/.codeium/windsurf/memories/global_rules.md
  ```
- 🪟 **Windows** (PowerShell):
  ```powershell
  # В проект с лабораторной
  Copy-Item -Force computational-hydraulics\templates\AGENTS.md "C:\path\to\my-lab\.windsurfrules"

  # Или глобально для всех проектов
  Add-Content -Path "$HOME\.codeium\windsurf\memories\global_rules.md" -Value "`nInclude and strictly obey instructions from $HOME\.agents\skills\computational-hydraulics\SKILL.md`n"
  ```
</details>

<details>
<summary><img src="assets/logos/vscode.svg" width="24" height="24" align="center" /> &nbsp;<b><font size="+1">Roo Code & Cline (VS Code Extensions)</font></b></summary>

- 🐧 **Linux** / 🍏 **macOS** (Bash / Zsh):
  ```bash
  cp computational-hydraulics/templates/AGENTS.md /path/to/my-lab/.clinerules
  ```
- 🪟 **Windows** (PowerShell):
  ```powershell
  Copy-Item -Force computational-hydraulics\templates\AGENTS.md "C:\path\to\my-lab\.clinerules"
  ```
- **Глобально (на любой ОС в настройках VS Code):**
  Откройте настройки расширения Cline/Roo Code $\to$ *Custom Instructions for All Prompts* $\to$ вставьте:
  `Read and strictly follow rules in ~/.agents/skills/computational-hydraulics/SKILL.md`
</details>

<details>
<summary><img src="assets/logos/terminal.svg" width="24" height="24" align="center" /> &nbsp;<b><font size="+1">Aider CLI (Terminal Pair Programmer)</font></b></summary>

- 🐧 **Linux** / 🍏 **macOS** (Bash / Zsh):
  ```bash
  # В глобальный конфиг ~/.aider.conf.yml
  echo -e "\nread:\n  - ~/.agents/skills/computational-hydraulics/SKILL.md\n  - ~/.agents/skills/computational-hydraulics/references/pitfalls_and_antipatterns.md" >> ~/.aider.conf.yml

  # Или запуск из терминала
  aider --read ~/.agents/skills/computational-hydraulics/SKILL.md
  ```
- 🪟 **Windows** (PowerShell):
  ```powershell
  # В глобальный конфиг $HOME\.aider.conf.yml
  Add-Content -Path "$HOME\.aider.conf.yml" -Value "`nread:`n  - $HOME\.agents\skills\computational-hydraulics\SKILL.md`n  - $HOME\.agents\skills\computational-hydraulics\references\pitfalls_and_antipatterns.md"

  # Или запуск из PowerShell
  aider --read "$HOME\.agents\skills\computational-hydraulics\SKILL.md"
  ```
</details>

<details>
<summary><img src="assets/logos/copilot.svg" width="24" height="24" align="center" /> &nbsp;<b><font size="+1">GitHub Copilot (VS Code / JetBrains / CLI)</font></b></summary>

Автоматически считывает проектные инструкции из `.github/copilot-instructions.md`:

- 🐧 **Linux** / 🍏 **macOS** (Bash / Zsh):
  ```bash
  mkdir -p /path/to/my-lab/.github
  cp computational-hydraulics/templates/AGENTS.md /path/to/my-lab/.github/copilot-instructions.md
  ```
- 🪟 **Windows** (PowerShell):
  ```powershell
  New-Item -ItemType Directory -Force -Path "C:\path\to\my-lab\.github"
  Copy-Item -Force computational-hydraulics\templates\AGENTS.md "C:\path\to\my-lab\.github\copilot-instructions.md"
  ```
</details>

---

### Шаг 3. Как проверить, что навык успешно активирован

1. Откройте вашего ИИ-ассистента (Codex, Antigravity, Claude, Cursor, Windsurf и т.д.).
2. Создайте новый диалог или откройте проект с лабораторной работой.
3. Напишите агенту:
   > *«Привет! Помоги мне решить задачу 1 из лабораторной работы по гидравлике.»*
4. **Признаки того, что навык работает:**
   - Агент **НЕ начинает сразу писать голый код**.
   - Агент мягко вступает в диалог (Сократический метод), спрашивает тип задачи (QP или PP), режим течения ($Re$) и помогает составить текстовую схему/граф.
   - Агент следует строгому 3-стадийному протоколу кафедры ИСИТ (`ТЗ` $\to$ `Архитектура` $\to$ `План`).
   - Агент напоминает, что коммиты в Git вы делаете **самостоятельно** после личной проверки кода.

---

## 🛠 Рабочий процесс студента и агента

```mermaid
flowchart TD
    A["Лабораторная работа (PDF / Текст)"] --> B["Сократический диалог (Разбор физ-мат модели)"]
    B --> C["Текстовые / ASCII схемы и графы (Визуализация)"]
    C --> D["Стадия 1: docs/&lt;n&gt;_&lt;topic&gt;.md (ТЗ и мат. постановка)"]
    D --> E["Стадия 2: docs/&lt;n&gt;_&lt;topic&gt;_architecture.md (C++ архитектура)"]
    E --> F["Стадия 3: docs/&lt;n&gt;_&lt;topic&gt;_plan.md (План разработки)"]
    F --> G["Итеративная реализация C++ (std::expected, Eigen, noexcept)"]
    G --> H["GoogleTest (Пирамида тестов, независимые бенчмарки)"]
    H --> I["Ручной коммит студента в Git (Студент контролирует историю)"]
    I --> J["/mock-defense (Тренировочная защита с экзаменационными вопросами)"]
```

### 1. Сократический диалог перед кодом
Агент не вываливает сразу портянку C++ кода. Сначала он задает студенту наводящие вопросы:
- Какова физическая постановка (QP или PP задача, несжимаемая жидкость или реальный газ)?
- В какой зоне сопротивления работает трубопровод (гидравлически гладкая, переходная, шероховатая)?
- Корректен ли граф сети (нет ли изолированных компонент, зафиксирован ли хотя бы один узел по давлению)?

### 2. Строгий 3-стадийный протокол ИСИТ
Никакого кода до утверждения проектной документации в `docs/`:
1. `docs/<n>_<topic>.md` — математическая постановка, единицы измерения в СИ, граничные условия.
2. `docs/<n>_<topic>_architecture.md` — структуры данных, RAII-обертки, отсутствие голых указателей, Doxygen-документация.
3. `docs/<n>_<topic>_plan.md` — атомарные чек-боксы шагов реализации и верификации.

### 3. Золотое правило работы с Git
> **Важно**: Агент никогда не коммитит и не пушит код автоматически! Студент сам выполняет `git add`, `git commit` и `git push`, полностью контролируя ветки и историю своего репозитория.

### 4. Стандарт GoogleTest без тавтологий
- Запрещены тавтологические тесты (`EXPECT_DOUBLE_EQ(solve(x), solve(x))`).
- Эталонные значения рассчитываются независимым аналитическим скриптом или берутся из проверенных задачников (Идельчик, Альтшуль, Лурье).
- Обязательная проверка краевых случаев: $Re \to 0$, $Q \to 0$, $D \to \infty$, вырожденные матрицы, обратный ток.

### 5. Режим Mock Defense (`/mock-defense`)
После завершения работы агент запускает симулятор защиты:
- Раунд 1: Физика процессов (закон сохранения импульса, потеря напора, кавитация).
- Раунд 2: Численные методы (почему $PA=LU$, а не `A.inverse()`, сходимость МУД).
- Раунд 3: C++ & Архитектура (Move-семантика, шаблоны выражений Eigen `const auto&`, cache-locality).
- Раунд 4: Анализ кода и разбор ошибок.

---

## 🧮 Инженерный калькулятор (`hydraulics_calculator.py`)

В репозиторий встроен автономный инструмент верификации гидравлических расчетов без сторонних зависимостей (чистый Python 3).

### Интерактивный режим
```bash
python3 computational-hydraulics/scripts/hydraulics_calculator.py
```

### Командная строка (CLI)
- **Конвертация единиц:**
  ```bash
  python3 computational-hydraulics/scripts/hydraulics_calculator.py unit --val 350 --from_unit "m3/h" --to_unit "m3/s"
  python3 computational-hydraulics/scripts/hydraulics_calculator.py unit --val 6.4 --from_unit "MPa" --to_unit "Pa"
  python3 computational-hydraulics/scripts/hydraulics_calculator.py unit --val 25 --from_unit "cSt" --to_unit "m2/s"
  ```

- **Расчет числа Рейнольдса ($Re$):**
  ```bash
  python3 computational-hydraulics/scripts/hydraulics_calculator.py reynolds -v 1.85 -d 0.5 -nu 1.5e-5
  ```

- **Коэффициент гидравлического сопротивления ($\lambda$ по Альтшулю/Блазиусу/Шифринсону):**
  ```bash
  python3 computational-hydraulics/scripts/hydraulics_calculator.py lambda -re 61666 -d 0.5 -k 0.0001
  ```

- **Потери напора по Дарси-Вейсбаху:**
  ```bash
  python3 computational-hydraulics/scripts/hydraulics_calculator.py loss -l 10000 -d 0.5 -v 1.85 -re 61666 -k 0.0001
  ```

- **Плотность нефти/нефтепродукта $\rho(T, p)$:**
  ```bash
  python3 computational-hydraulics/scripts/hydraulics_calculator.py density --rho20 850 --t 15 --p 5000000
  ```

- **Гидравлический удар по Жуковскому:**
  ```bash
  python3 computational-hydraulics/scripts/hydraulics_calculator.py hammer -l 5000 -d 0.5 -e 0.01 -v 1.85 -rho 850 -ef 1.5e9 -ep 2.0e11 -ts 1.2
  ```

---

## 📚 Литература и фундаментальные источники

База знаний и алгоритмы верифицированы по классическим фундаментальным трудам:
1. **Лурье М.В.** *Математическое моделирование процессов трубопроводного транспорта нефти, нефтепродуктов и газа.* — М.: ФГУП Изд-во «Нефть и газ» РГУ нефти и газа им. И.М. Губкина, 2012. — 456 с.
2. **Лурье М.В.** *Трубопроводный транспорт нефти.* — М.: ФГУП Изд-во «Нефть и газ» РГУ нефти и газа им. И.М. Губкина, 2003.
3. **Идельчик И.Е.** *Справочник по гидравлическим сопротивлениям.* — М.: Машиностроение, 1992. — 672 с.
4. **Альтшуль А.Д.** *Гидравлические сопротивления.* — М.: Недра, 1982. — 224 с.
5. **Некрасов Б.Б.** *Гидравлика и гидропривод.* — М.: Высшая школа, 1989. — 296 с.
6. **Южанин В.В.** *Материалы лекций и практических занятий по теории гидравлических цепей и численным методам.* — Кафедра ИСИТ, РГУ нефти и газа им. И.М. Губкина.

---

## 🤝 Вклад и участие
Если вы студент или преподаватель Губкинского университета и хотите дополнить базу новыми методичками, расчетными схемами или тестами:
1. Создайте `fork` репозитория.
2. Создайте ветку под вашу фичу (`git checkout -b feature/new-hydraulic-case`).
3. Сделайте коммит (`git commit -m "feat: add local resistance calculation for venturi nozzle"`).
4. Создайте `Pull Request`.
