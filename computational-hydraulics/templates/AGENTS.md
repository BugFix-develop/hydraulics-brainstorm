# Development Protocol and Code Quality Standards for AI Agents (AGENTS.md)

> This file is placed in the root directory of the repository and serves as a mandatory set of rules for all interacting AI agents and developers in the Department of Automation of Technological Processes (ATP). Without this file in the repository history, agentic coursework is considered improperly formatted.

---

## 1. General Development Principles

0. **Assignment Analysis, Proactive Discussion, and Ban on Premature Files:**
   * Upon completing the analysis of an uploaded laboratory assignment, PDF, or problem statement, the agent **MUST proactively propose an in-depth discussion** of the physical phenomena and mathematical formulation.
   * The agent is **strictly prohibited from creating project documentation (`docs/*.md`), architecture, or code files** prior to an interactive dialogue with the developer, an audit of the assignment for potential errors, and explicit confirmation of model comprehension.
   * The only permitted action prior to model agreement is creating the directory structure (`mkdir -p docs include src tests`).
1. **Developer as Context Manager (Cognitive Risk Reduction):**
   * The developer is responsible for mitigating cognitive risks. **It is strictly forbidden to "vibecode" fundamental physical principles** that the developer is encountering for the first time.
   * Context is formalized as a self-contained **"Business Logic Specification"** (`docs/<n>_<topic>.md`), which explains the problem, governing equations, and justification of sufficiency without superfluous filler ("article-style bloat").
   * Writing C++ code, defining classes, or detailing file layouts is **strictly prohibited** inside the business logic document.
2. **Mandatory Repository Root `AGENTS.md` Audit:**
   * At the start of every session, the agent must verify the presence of `AGENTS.md` in the repository root.
   * If the file is missing, the agent immediately creates it from `templates/AGENTS.md`.
   * If the file already exists, the agent reads it and supplements any missing standards without overwriting user-configured settings.
3. **Strict Code Reuse & Integration:**
   * **Recreating existing project functions, data structures, or classes from scratch is strictly prohibited.**
   * Before designing new functionality, the agent must inspect existing files in `include/` and `src/` (from earlier laboratory tasks or modules).
   * All existing domain types (pipe geometry, fluid properties, math utilities, graph structures) must be reused directly via `#include`.
   * The architecture document must explicitly separate reused entities from newly introduced entities.
4. **Mandatory Pause After Generating `docs/` (Gatekeeper 1):**
   * After generating Markdown specifications (`docs/<n>_<topic>.md`, `architecture.md`, `plan.md`), the agent must **HALT COMPLETELY** to allow the developer to review the documentation.
   * Implementing code in `include/` and `src/` is permitted **ONLY** after explicit user approval: *"Documents approved, proceed to implementation"* (*"Документы утвердил, приступаем к реализации"*).
5. **Strict Limit: Exactly One Stage Per Response (One Stage Per Turn):**
   * The agent is **strictly forbidden from combining multiple implementation stages from `plan.md` in a single response** (e.g., generating CMakeLists.txt, base structures, and the solver class in one turn).
   * In each individual turn, the agent implements files belonging to **ONLY ONE** active stage.
   * After creating the files for the current stage, the agent **MUST IMMEDIATELY STOP**, cease calling file-writing tools, report progress, and conclude the response.
   * Advancing to the next stage is permitted **ONLY IN THE SUBSEQUENT RESPONSE** after user confirmation: *"Stage verified, proceed to next stage"* (*"Этап проверил, переходим к следующему"*).
   * *Expert Mode:* If the developer explicitly requests *"expert mode"*, *"without pauses"*, or *"/expert-mode"*, the one-stage-per-turn limit is lifted for the computational core (the test gatekeeper and the ban on automatic Git commits remain active).
6. **Mandatory Pause Before Writing Tests (Gatekeeper 3):**
   * Prior to creating GoogleTest files in `tests/`, the agent must pause in chat, present the test scenarios according to the 4-tier test pyramid, verify independent benchmark values, and await developer confirmation.
   * Tautological tests (`EXPECT_EQ(calc(x), calc(x))`) are strictly prohibited.
7. **Version Control Belongs Exclusively to the Developer:**
   * The AI agent is prohibited from automatically executing `git commit` or `git push` without explicit developer instructions. Commits are performed manually by the developer following personal code review.
8. **Strict Directory File Separation:**
   * `include/`: header files only (`.h`, `.hpp`).
   * `src/`: implementation source files only (`.cpp`, `.c`).
   * `tests/`: test source files (`.cpp`).
   * `docs/`: project documentation (`.md`).
   * **No mixing:** Keeping `.h` and `.cpp` in the same directory is strictly prohibited. Header-only templates and structures are placed in `include/` without creating a `.cpp` file.

---

## 2. C++ Standards & Code Style

1. **Language Standard:** C++20 (or C++17).
2. **Naming Convention:** Strict `snake_case` for all entities (functions, methods, variables, structures, classes, files).
3. **Type Suffix:** All structures, type aliases (`using`), and classes must have the `_t` suffix:
   * `pipe_properties_t`, `fluid_state_t`, `linear_nodal_solver_t`.
4. **Physical Clarity of Identifiers:** Meaningless single-letter abbreviations are forbidden (`density` instead of `rho`, `kinematic_viscosity` instead of `nu`, `flow_rate` instead of `q`).
5. **Physical Constants:** Mathematical and physical constants are defined as `constexpr` with physical units:
   * `constexpr double standard_gravity = 9.80665;`
   * `constexpr double atmospheric_pressure = 101325.0;`
6. **Header Guards:** `#pragma once` as the first line of every header file.
7. **Strict Concise Doxygen Documentation:**
   * Verbose "walls of text" and comments explaining self-evident operations are forbidden.
   * Structure fields are documented strictly in one line with SI units in square brackets:
     ```cpp
     double pipe_diameter{0.0}; ///< Internal pipeline diameter [m]
     ```
   * Class methods feature concise Doxygen blocks:
     * `@brief` — brief 1-line purpose;
     * `@param` — parameter purpose and SI unit in 1 line;
     * `@return` — physical meaning of the return value in 1 line;
     * `@throw` — exception conditions (`std::invalid_argument`, `std::runtime_error`).

---

## 3. Linear Algebra and Eigen Protocol

1. **Strict Prohibition of Explicit Matrix Inversion:**
   * Writing `A.inverse() * b` is strictly prohibited. It is computationally inefficient and numerically unstable.
2. **Single-Pass FullPivLU (Rank Check and Solution):**
   * Singularity analysis, rank determination, and system solution are performed in a single pass using a unified `Eigen::FullPivLU` object:
     ```cpp
     Eigen::FullPivLU<Eigen::MatrixXd> lu(A_block);
     if (!lu.isInvertible()) {
         throw std::runtime_error("Singular network matrix: incomplete rank");
     }
     Eigen::VectorXd z = lu.solve(b_vec);
     ```
   * Redundant factorization via `PartialPivLU` is not required.
3. **Normalized Residual Verification:**
   * After each numerical solve, the normalized residual norm is evaluated:
     $$\frac{\Vert \mathcal{A} z - b \Vert_\infty}{\Vert \mathcal{A} \Vert_\infty \Vert z \Vert_\infty + \Vert b \Vert_\infty} < 10^{-12}$$

---

## 4. Architectural Principles & Task Pattern

1. **Separation of Data and Solvers (Task Pattern):**
   * Input data is stored in immutable property structures (`*_properties_t`);
   * Results are returned in dedicated result structures (`*_result_t`);
   * Solvers do not maintain mutable state between invocations (Stateless).
2. **Encapsulation and Invariant Validation:**
   * Input parameters are validated in constructors;
   * Invalid physical parameters ($d \le 0$, $\rho \le 0$) throw `std::invalid_argument`;
   * Inconsistent or singular mathematical systems throw `std::runtime_error`.
3. **Pass Only What You Need:**
   * Interface boundaries must not accept redundant types from neighboring layers.
