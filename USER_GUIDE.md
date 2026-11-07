# 📘 User Guide: Working with the Computational Hydraulics AI Skill
> **Practical onboarding manual for students and developers: how to interact with the AI agent, pass mandatory control gatekeepers, develop robust C++20 simulation code, and prepare for oral lab defense in the ATP Department.**

---

## 🧭 Navigation
1. [Core Purpose of the Skill](#1-core-purpose-of-the-skill)
2. [Environment Setup (1-Minute Quickstart)](#2-environment-setup-1-minute-quickstart)
3. [How to Communicate with the Agent](#3-how-to-communicate-with-the-agent)
4. [Step-by-Step Workflow: From Assignment to Lab Defense](#4-step-by-step-workflow-from-assignment-to-lab-defense)
   - [Stage 0: Engineering Seminar & Model Analysis (Gatekeeper 0)](#stage-0-engineering-seminar--model-analysis-gatekeeper-0)
   - [Stage 1: Documentation Package in docs/ (Gatekeeper 1)](#stage-1-documentation-package-in-docs-gatekeeper-1)
   - [Stage 2: Step-by-Step C++ Implementation (Gatekeeper 2 — "One Stage Per Turn")](#stage-2-step-by-step-c-implementation-gatekeeper-2--one-stage-per-turn)
   - [Stage 3: GoogleTest Verification Strategy (Gatekeeper 3)](#stage-3-googletest-verification-strategy-gatekeeper-3)
   - [Stage 4: Version Control (Git)](#stage-4-version-control-git)
   - [Stage 5: Pre-Defense Exam Simulator (/mock-defense)](#stage-5-pre-defense-exam-simulator-mock-defense)
5. [Lecture Study and Theoretical Seminar Mode](#5-lecture-study-and-theoretical-seminar-mode)
6. [Quick Phrases Cheat Sheet](#6-quick-phrases-cheat-sheet)
7. [Frequently Asked Questions & Troubleshooting (FAQ)](#7-frequently-asked-questions--troubleshooting-faq)

---

## 1. Core Purpose of the Skill

Standard AI assistants often indulge in "vibecoding": they consume a terse laboratory assignment and immediately dump large blocks of unverified C++ code. This leads to critical failure points:
* Emergence of physically absurd errors (negative friction losses, division by zero in Todini GGM, unstable explicit inversion `A.inverse()`).
* Tautological tests that assert unverified calculations against themselves (`EXPECT_EQ(calc(x), calc(x))`).
* The student fails to understand the underlying mechanics and **fails the oral exam on the very first theoretical question**.

**The Computational Hydraulics Skill radically restructures this process:**
1. The agent acts as an **expert academic mentor and Senior C++ architect**.
2. The agent is **locked against blind code generation**: it will not write implementation code until you have jointly analyzed the governing physical equations.
3. Development proceeds through **strict gatekeepers**: the agent pauses after every milestone to await your review.
4. The agent provides an **interactive oral pre-defense drill (`/mock-defense`)**, asking exam questions one at a time to prepare you for faculty evaluation.

---

## 2. Environment Setup (1-Minute Quickstart)

### Option A. Work Inside This Repository (Fastest)
1. Clone the repository:
   ```bash
   git clone https://github.com/BugFix-develop/hydraulics-brainstorm.git my-hydraulics-lab
   cd my-hydraulics-lab
   ```
2. Open the directory in your agentic IDE (**Cursor, Windsurf, VS Code + Cline/Roo Code, Claude Code**, or **Antigravity**).
3. Ensure standard directories exist:
   ```bash
   mkdir -p docs include src tests
   ```

### Option B. Integrate into an Existing Project
Copy the `computational-hydraulics` folder into your existing repository root:
* **Linux / macOS:** `cp -r computational-hydraulics /path/to/your/lab/`
* **Windows (PowerShell):** `Copy-Item -Recurse -Force computational-hydraulics "C:\path\to\your\lab\"`

> [!IMPORTANT] Directory Layout Standard (`include/` vs `src/`)
> * All header files (`.h`, `.hpp`) reside exclusively in `include/`.
> * All implementation files (`.cpp`, `.c`) reside exclusively in `src/`.
> * Mixing headers and source files in the same directory is prohibited by the project architectural standard (except for self-contained header-only templates).

---

## 3. How to Communicate with the Agent

### Key Principles:
1. **Ask Conceptual Questions:** If you do not understand a term in the Bernoulli equation or why a block in the KKT matrix is zero, ask directly: *"Explain simply: what is the physical meaning of this coefficient?"*
2. **Drive the Transitions:** The agent is programmed to halt at gatekeepers. To proceed, give a clear confirmation phrase.
3. **Demand Design Rationale:** If the agent proposes an algorithm or structure, ask: *"Why do we use FullPivLU here rather than PartialPivLU?"* — this builds your exam readiness.
4. **Control Git Yourself:** The agent never commits or pushes code automatically without your explicit command.

---

## 4. Step-by-Step Workflow: From Assignment to Lab Defense

```text
[Assignment / PDF / Notes]
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Stage 0: Chat Seminar (Physics, Equations, QA Audit)   │ ──► Gatekeeper 0: Confirm model
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Stage 1: Specification in docs/ (Statement & Arch)     │ ──► Gatekeeper 1: Reading pause
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Stage 2: Step-by-Step C++ (EXACTLY 1 Stage Per Turn)   │ ──► Gatekeeper 2: Stage review
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Stage 3: GoogleTest (4-Tier Pyramid, Benchmarks)       │ ──► Gatekeeper 3: Test strategy
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Stage 4: Manual Developer Git Commit and Push          │
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Stage 5: Mock Defense Simulator (/mock-defense)        │
└────────────────────────────────────────────────────────┘
```

---

### Stage 0: Engineering Seminar & Model Analysis (Gatekeeper 0)

#### What to Do:
Attach your laboratory assignment (PDF, photo, or prompt):
> *"Hello! Here is the assignment for Lab 2 (Branched Pipeline Flow Distribution). My variant is #4. Let's analyze the problem."*

#### What the Agent Does:
1. **Takes the Initiative:** The agent will not generate code immediately. It welcomes you and initiates a substantive discussion of the physics.
2. **Performs a QA Audit:** Verifies if all boundary conditions are present (pipe lengths, diameters, roughness, fluid properties $\rho, \nu$, boundary pressures). If the problem statement contains typos or lacks a reference $P$-node, the agent highlights this immediately.
3. **Explains Physics and Formulations:** Sketches the graph, formulates mass conservation (1st Kirchhoff Law) and momentum balance (2nd Kirchhoff Law), and identifies flow regimes ($Re$).
4. **Asks Guiding Questions:** Ensures you grasp core concepts before coding.

#### How to Clear Gatekeeper 0:
When the model is clear to you, command:
> *"I understand the model and governing equations. Please generate the docs/ package."*  
> *(or in Russian: "Физику процесса и математическую модель понял. Формируй пакет документации docs/.")*

---

### Stage 1: Documentation Package in `docs/` (Gatekeeper 1)

#### What the Agent Generates:
1. `docs/<n>_<topic>.md` — **Business Logic Specification:** A concise, self-contained document stating the technological objective, scope of the current iteration, equations, SI parameter tables with examples, and verification tolerances. It contains **no C++ code and no article-style bloat**.
2. `docs/<n>_<topic>_architecture.md` — **C++20 Architecture Specification:** Data types, solver contracts, strict Doxygen signatures, call invariants, and error policies.
   * *Codebase Inspection:* Explicitly separates **reused existing entities** from **new types**. Recreating existing types from scratch is strictly forbidden.
3. `docs/<n>_<topic>_plan.md` — Atomic checklist of implementation stages.

> [!IMPORTANT] Repository Root AGENTS.md
> The agent verifies that `AGENTS.md` exists in the repository root. If missing, it creates it from `templates/AGENTS.md`. Without this file in Git, coursework is considered improperly formatted.

#### Mandatory Pause (Gatekeeper 1):
After creating these documents, the agent **STOPS COMPLETELY**. Code generation in `src/` is locked.

#### How to Clear Gatekeeper 1:
> *"Documents in docs/ reviewed and approved. Proceed with implementation according to the plan."*  
> *(or: "Документы в docs/ проверил и утвердил. Начинаем реализацию по плану.")*

---

### Stage 2: Step-by-Step C++ Implementation (Gatekeeper 2 — "One Stage Per Turn")

#### The One Stage Per Turn Rule:
The agent is strictly prohibited from implementing the entire project in a single response. In each turn, the agent implements **exactly one stage** from `plan.md`.

#### Sequential Progression:
* **Stage 1 (CMake):** Generates `CMakeLists.txt` with strict flags (`-Wall -Wextra -Wpedantic`), C++20 standard, and dependencies.
  * *Pause:* Agent reports and relinquishes control.
  * *Your Response:* *"CMake looks good. Proceed to data structures."*
* **Stage 2 (Types & Headers):** Generates header files in `include/` with concise Doxygen contracts (using single-line `///` per line; `/** ... */` is strictly forbidden).
  * *Pause.*
  * *Your Response:* *"Headers reviewed. Proceed to solver implementation."*
* **Stage 3 (Solver):** Implements solver logic in `src/` (validation, KKT assembly, `FullPivLU` factorization, residual tracking).
  * *Pause.*

> [!TIP] Expert Override (`/expert-mode`)
> If you are an experienced developer and want the computational core generated in a single pass without intermediate pauses, prompt:
> > *"Enable /expert-mode"* or *"Implement computational core without stage pauses"*.
> 
> The agent will synthesize the core in one pass, but **will still halt before writing tests** and will never commit to Git automatically.

---

### Stage 3: GoogleTest Verification Strategy (Gatekeeper 3)

#### Why another mandatory pause?
The most pervasive error in AI code generation is **tautological testing** (asserting a function against its own output: `EXPECT_EQ(calc(x), calc(x))`). Such tests pass blindly but fail to verify physical reality.

#### What the Agent Presents:
A 4-tier testing pyramid:
1. **Level 1 (Analytical Benchmarks):** Comparison against independent hand calculations. For nodal pressures [Pa], relative tolerance $\text{rtol} \le 10^{-4}$ is used; for flow rates [$\text{m}^3/\text{s}$], absolute tolerance $10^{-8}$ is applied. Linear system residual must satisfy $\frac{\Vert \mathcal{A}z - b \Vert_\infty}{\Vert \mathcal{A} \Vert_\infty \Vert z \Vert_\infty + \Vert b \Vert_\infty} < 10^{-12}$.
2. **Level 2 (Physical Invariants):** Kirchhoff mass balance ($\Vert Ax - Q \Vert_\infty < 10^{-8}$), zero loss at zero flow ($Q=0 \implies \Delta h=0$), monotonic dissipation ($h_f \propto Q|Q|$).
3. **Level 3 (Boundary Singularities):** Verifying that removing all $P$-nodes causes `FullPivLU` to detect rank deficiency and throw `std::runtime_error`.
4. **Level 4 (Contracts):** `EXPECT_THROW` on negative diameters, lengths, or non-positive resistances.

#### How to Clear Gatekeeper 3:
> *"Test plan and tolerances approved. Generate GoogleTest files in tests/."*  
> *(or: "Тест-план и допуски согласовал. Генерируй файлы GoogleTest в tests/.")*

---

### Stage 4: Version Control (Git)

Following the **Golden Rule of Git**, the agent never auto-commits. You retain full control over your branch history:

```bash
git status
git add include/ src/ tests/ CMakeLists.txt docs/ AGENTS.md
git commit -m "feat: implement linear nodal solver with single-pass FullPivLU and gtest suite"
git push origin main
```
*(If you want the agent to execute the commit on your behalf, explicitly command: "Commit and push current changes yourself".)*

---

### Stage 5: Pre-Defense Exam Simulator (`/mock-defense`)

When tests are green, initiate your exam rehearsal.

#### How to Launch:
> *"Run /mock-defense"* or *"Let's rehearse the lab defense"*.

#### How It Works:
1. The agent adopts the persona of an exacting professor from the Gubkin ATP Department.
2. Questions are posed **strictly one at a time** across 4 rounds:
   * **Round 1 (Physics):** Bernoulli equation, Darcy-Weisbach 4 friction regimes, cavitation, water hammer waves.
   * **Round 2 (Math & TGC):** Network graph topology, incidence matrix rank $m-1$, KKT saddle blocks, Todini GGM regularization.
   * **Round 3 (C++ & Architecture):** Why LU factorization (`lu.solve()`) rather than `A.inverse() * b`, backward stability, Task pattern, code reuse.
   * **Round 4 (Verification):** Mass conservation proof, why relative tolerance for pressure vs absolute for flow rate, singular rank assertions.
3. You answer in your own words.
4. The agent critiques your response, reinforces accurate phrasing, and issues an objective grade with topics to review.

---

## 5. Lecture Study and Theoretical Seminar Mode

The skill functions not only as a lab solver, but also as a **dedicated private tutor in fluid mechanics and numerical methods**.

### How to Discuss a Lecture:
1. Upload your lecture slides, notes, or board photos.
2. Prompt:
   > *"Here is our lecture on transient pipeline dynamics and Joukowsky shock waves. Let's analyze it: what is the physical meaning of wave speed $c$ and how does pipe wall elasticity affect it?"*
3. The agent reviews the material against foundational literature (M.V. Lurie, I.E. Idelchik) and explains formulas, derivations, and engineering implications step-by-step.

---

## 6. Quick Phrases Cheat Sheet

| Milestone / Situation | What to Say (English) | What to Say (Russian) |
|---|---|---|
| **Start Assignment** | *"Hello! Help me solve this lab assignment. My variant is #3. Let's analyze the physics first."* | *«Привет! Помоги сделать лабораторную работу по этой методичке. Мой вариант №3. Давай сначала обсудим физику.»* |
| **Approve Model (Gate 0)** | *"I understand the model and equations. Proceed to generate docs/."* | *«Физическую картину и уравнения понял. Переходи к формированию docs/.»* |
| **Approve Docs (Gate 1)** | *"Specifications in docs/ approved. Proceed with implementation according to plan."* | *«Документы ТЗ, архитектуру и план в docs/ проверил и утвердил. Начинаем реализацию расчетного ядра.»* |
| **Next Stage (Gate 2)** | *"Current stage verified. Proceed to [Next Stage Name]."* | *«Код текущего этапа проверил. Переходим к этапу [Название следующего этапа].»* |
| **Expert Fast Mode** | *"Enable /expert-mode and implement the computational core without pauses."* | *«Включи /expert-mode и реализуй расчетное ядро целиком до этапа тестов.»* |
| **Approve Tests (Gate 3)** | *"Test plan and tolerances approved. Generate GoogleTest files in tests/."* | *«Тест-план и 4 уровня тестов согласовал. Генерируй код тестов в tests/.»* |
| **Launch Mock Defense** | *"Implementation done. Run /mock-defense and test my knowledge."* | *«Код и тесты готовы. Запусти /mock-defense, погоняй меня по вопросам к защите.»* |
| **Clarify Detail** | *"Explain in detail: why must the diagonal be regularized in the Todini GGM method?"* | *«Объясни подробнее: почему мы обязаны регуляризировать диагональ в методе Тодини?»* |
| **Request Git Commit** | *"Commit and push current changes yourself with a descriptive message."* | *«Закоммить и запушь текущие изменения сам с понятным сообщением.»* |

---

## 7. Frequently Asked Questions & Troubleshooting (FAQ)

### Q: "The agent generated too much code at once and ignored the pause. What should I do?"
**A:** Enforce the quality protocol:
> *"Adhere strictly to the 'One Stage Per Turn' rule. Halt immediately, clean up unreviewed stages, and report only on the current stage!"*

### Q: "The assignment contains a typo in a formula or dimension. How should we proceed?"
**A:** During the Stage 0 QA audit, the agent will flag the inconsistency. Instruct the agent:
> *"Yes, that is an erratum in the manual. Document the correct physical formula according to Lurie in `docs/statement.md` and add a brief note about the typo so I can explain it during lab defense."*

### Q: "A GoogleTest pressure assertion failed unexpectedly. Why?"
**A:** Check the tolerance specification. If an absolute tolerance like `EXPECT_NEAR(..., 1e-8)` was applied to pressures around $10^6\text{ Pa}$, it requires relative precision near $10^{-14}$ (at the edge of machine epsilon for `double`). Update the test to relative tolerance:
```cpp
double rel_err = std::abs(p_calc - p_bench) / std::abs(p_bench);
EXPECT_LT(rel_err, 1e-4);
```

### Q: "Where are the underlying engineering references located?"
**A:** All foundational knowledge is organized inside `computational-hydraulics/references/`:
* [hydraulics_core.md](file:///home/muslim/Coding/hydraulics-brain/computational-hydraulics/references/hydraulics_core.md) — 1D hydraulics, fluid properties, Darcy-Weisbach, Joukowsky water hammer.
* [sem2_guide.md](file:///home/muslim/Coding/hydraulics-brain/computational-hydraulics/references/sem2_guide.md) — profiling, Bernoulli, QP/PP problems, pump curves, Task pattern.
* [sem3_guide.md](file:///home/muslim/Coding/hydraulics-brain/computational-hydraulics/references/sem3_guide.md) — TGC networks, KKT block systems, Todini GGM regularization, FullPivLU solver.
* [circuits_and_agentic.md](file:///home/muslim/Coding/hydraulics-brain/computational-hydraulics/references/circuits_and_agentic.md) — Yuzhanin circuit theory and ATP agentic standards.
* [pitfalls_and_antipatterns.md](file:///home/muslim/Coding/hydraulics-brain/computational-hydraulics/references/pitfalls_and_antipatterns.md) — top-15 hydraulic and C++ antipatterns.
* [mock_defense_protocol.md](file:///home/muslim/Coding/hydraulics-brain/computational-hydraulics/references/mock_defense_protocol.md) — complete oral exam rehearsal questions.
