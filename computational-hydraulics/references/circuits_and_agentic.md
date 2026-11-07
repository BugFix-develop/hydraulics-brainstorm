# Hydraulic Circuit Theory (TGC) & Agentic Development Regulation
## Methodological & Mathematical Guide for AI Agents (`circuits_and_agentic.md`)

> Primary references:
> * **V. V. Yuzhanin** — *Introduction to the Theory of Hydraulic Circuits: Nodal Methods, Global Gradient Method, Pendant Formalism* (Gubkin University, 2026).
> * **ATP Department** — *Engineering Standards for Agentic Laboratory Development* (`agentic_development_requirements.md`, 2026).

---

## PART I. THEORY OF HYDRAULIC CIRCUITS (TGC)

### 1. Topological Description of Networks on Graphs
A hydraulic network is modeled as a connected directed graph $G = (V, E)$, containing:
* $m = |V|$ nodes (vertices);
* $n = |E|$ branches (directed edges).

#### 1.1. Full Incidence Matrix $\bar{A}$ ($m \times n$)
Rows correspond to nodes, columns to branches:
$$
\bar{A}_{j, i} = \begin{cases}
+1, & \text{if branch } i \text{ leaves node } j \text{ (outflow)}; \\
-1, & \text{if branch } i \text{ enters node } j \text{ (inflow)}; \\
0, & \text{if branch } i \text{ is not incident to node } j.
\end{cases}
$$

* **Column Sum Invariant:** Each column has exactly one $+1$ and one $-1$. The sum of rows is identically zero ($\sum_{j=1}^m \bar{A}_{j, i} = 0$). Matrix rank is $\operatorname{rank}(\bar{A}) = m - 1$.
* **Kirchhoff's First Law (Mass Balance at all Nodes):**
  $$\bar{A} x = \bar{Q}$$
  where $x \in \mathbb{R}^n$ is branch flow rates and $\bar{Q} \in \mathbb{R}^m$ is external nodal flows vector.
* **Branch Pressure Differences (Inlet minus Outlet):**
  $$y = \bar{A}^T \bar{P}$$
  where $\bar{P} \in \mathbb{R}^m$ is nodal potential (pressure) vector and $y \in \mathbb{R}^n$ is branch pressure drop vector ($y_i = P_{\text{inlet}, i} - P_{\text{outlet}, i}$).

---

### 2. Branch Closure Relationships (Physical Object Models)
The closure relation relates branch pressure drop $y_i$ to volumetric flow rate $x_i$:
$$y_i = F_i(x_i) = f_i(x_i) - H_i$$
where:
* $f_i(x_i)$ — hydraulic friction loss function (odd and strictly monotonically increasing: $f_i(-x) = -f_i(x)$);
* $H_i$ — active head of source (pump boost, elevation hydrostatic difference $\rho g \Delta z$). In TGC, $H_i$ is expressed in **pressure units** [$\text{Pa}$].

#### 2.1. Standard Physical Models:
1. **Minor Resistance (Quadratic Friction):**
   $$y_i = s_i \cdot x_i |x_i|, \qquad s_i = \frac{\rho \zeta_i}{2 S_i^2}$$
2. **Centrifugal Pump (Active Branch):**
   $$y_i = \rho g b \cdot x_i |x_i| - \rho g a$$
   * Linearization near operating point $Q_{\text{nom}} > 0$:
     $$y_i^{\text{lin}} = 2 \rho g b Q_{\text{nom}} \cdot x_i - (\rho g b Q_{\text{nom}}^2 + \rho g a)$$
3. **Pipe with General Darcy–Weisbach Friction:**
   $$y_i = \frac{8 \rho \lambda(\text{Re}) L_i}{\pi^2 d_i^5} x_i |x_i| - \rho g (z_{\text{inlet}} - z_{\text{outlet}})$$
4. **Pipe with Laminar Flow (Poiseuille / Stokes Law):**
   $$y_i = \frac{128 \rho \nu L_i}{\pi d_i^4} x_i - \rho g (z_{\text{inlet}} - z_{\text{outlet}})$$

#### 2.2. Epifanov–Korelshtein Monotonicity Conditions:
To guarantee **existence and uniqueness** of network flow distribution solutions, friction loss functions $f_i(x_i)$ must be **strictly monotonic and continuous**. Monotonicity breakdown causes Newton solvers to diverge.

---

### 3. Classical Flow Distribution Problem (Nodal Formulation)

Partition nodes into:
* $m_Q$ — nodes with prescribed flow rates $Q$ (pressures $P$ unknown);
* $m_P$ — reference nodes with fixed pressures $P_p$.

Partitioned incidence matrix:
$$\bar{A} = \begin{pmatrix} A \\ A_p \end{pmatrix}, \qquad \bar{P} = \begin{pmatrix} P \\ P_p \end{pmatrix}$$

**Nodal Flow Distribution System:**
$$
\begin{cases}
A x = Q & \text{(Kirchhoff's First Law, } m_Q \text{ equations)} \\
A^T P = F(x) - A_p^T P_p & \text{(Kirchhoff's Second Law / momentum, } n \text{ equations)}
\end{cases}
$$
Total equations and unknowns: $N = m_Q + n$.

---

### 4. Numerical Solvers for Nonlinear Network Systems

#### 4.1. Nodal Pressure Method (NPM)
1. Invert branch relations to express flow through nodal pressures: $x_i = \psi_i(P_{F, i}, P_{L, i})$.
2. Substitute into Kirchhoff's First Law yielding residual system for unknown pressures $P$:
   $$r(P) = A \cdot \psi(P) - Q = 0$$
3. Newton–Raphson iteration:
   $$\Delta P_k = - J_r(P_k)^{-1} r(P_k)$$
4. Analytical Jacobian: $J_r(P) = A \cdot J_\psi(P)$, where $J_\psi$ is diagonal branch derivative matrix:
   $$\frac{\partial \psi_i}{\partial P_{F, i}} = -\frac{\partial \psi_i}{\partial P_{L, i}} = \frac{1}{\frac{d f_i(x_i)}{d x_i}}$$

#### 4.2. Todini Global Gradient Method (GGM)
Solves the coupled system simultaneously for flows $x$ and pressures $P$:
$$z = \begin{pmatrix} P \\ x \end{pmatrix}, \qquad r(z) = \begin{pmatrix} A x - Q \\ A^T P - F(x) + A_p^T P_p \end{pmatrix} = 0$$

* Symmetric block Jacobian:
   $$J_r(z) = \begin{pmatrix} 0 & A \\ A^T & -D(x) \end{pmatrix}$$
   where $D(x) = \operatorname{diag}\left( \frac{d F_i}{d x_i} \right)$ ($d_i = 2 s_i |x_i|$).
* **Maxwell Matrix $M(x)$:**
   $$M(x_k) = A D^{-1}(x_k) A^T$$
* **Division-by-Zero Regularization:** At zero flow ($x_i \to 0$), diagonal entry $d_i \to 0$, causing $D^{-1}$ to trigger division by zero (`NaN`). GGM implementations must enforce diagonal bounding $d_i = \max(2 s_i |x_i|,\, d_{\min})$ with $d_{\min} \sim 10^{-6}\dots 10^{-8}$ and initialize with non-zero velocities ($v_0 \approx 1.0\text{ m/s}$).
* GGM Iterative Steps:
   $$\Delta P_{\text{ggm}} = - M^{-1}(x_k) \left( A D^{-1}(x_k) w(P_k, x_k) - u(x_k) \right)$$
   $$\Delta x_{\text{ggm}} = D^{-1}(x_k) \left( w(P_k, x_k) + A^T \Delta P_{\text{ggm}} \right)$$

---

### 5. Pendant Edges Formalism
Engineering concept by Yuzhanin & Fomina unifying boundary conditions and internal circuit topology:

| Edge Type | Designation | Mathematical Description | Physical Meaning |
|---|---|---|---|
| **Non-pendant ($n_2$)** | Regular branches | Connect two interior nodes ($P_{F, i}, P_{L, i}$) | Pipes, valves, in-line pumps |
| **Pendant $Q$-edges** | Demand/source branches | Prescribed constant flow $q_i^s = \text{const}$ | Producing wells, consumers |
| **Pendant $P$-edges** | Pressure reference | Prescribed node pressure $p_i^s = \text{const}$ | Storage tanks, header manifolds |
| **Pendant $\varphi$-edges** | Nonlinear boundary | Characteristic curve $Q_i = \psi(P_D)$ | Reciprocating compressors, wellheads |
| **$PP$-edges** | Boundary connecting | Connects two fixed-pressure nodes | Solved independently |

---

## PART II. AGENTIC DEVELOPMENT REGULATION

### 1. Developer Role: Context Manager
1. The developer manages **cognitive risks** — the risk of generating code that violates physical laws or domain invariants.
2. "Vibecoding" fundamental physics without explicit mathematical specification is strictly forbidden.
3. **Stage 0 — Prerequisite Prior to File Generation (Proactive Discussion):** Upon analyzing the task document, the agent **MUST PROACTIVELY PROPOSE A DISCUSSION** of the physical phenomena, equations, and mathematical formulation. The agent connects the problem to the knowledge base (ATP lecture courses, Lurie, Idelchik, TGC), performs an audit for typos and missing boundary conditions, and waits for explicit user confirmation. Generating files in `docs/` or writing code is strictly forbidden until Stage 0 completes.
4. **Review Pause After `docs/` Creation (Gateway 1):** After generating files in `docs/`, the agent must completely stop so the developer can review and approve the specification, architecture, and plan. Implementation code generation starts only after explicit approval.
5. **One Stage Per Turn Rule (Gateway 2):** The agent is strictly prohibited from combining multiple plan stages into a single response. In each turn, the agent implements files for exactly one plan stage from `plan.md`, then immediately ceases tool calls, reports progress, and yields control. Moving to the next stage occurs only in the subsequent turn after confirmation.
6. **Pause Before Test Generation (Gateway 3):** Before creating GoogleTest files in `tests/`, the agent must stop, present the 4-tier testing pyramid, confirm benchmark sources, and await approval.
7. **Strict Header/Source Directory Separation:** Header files (`.h`, `.hpp`) reside exclusively in `include/`. Implementation files (`.cpp`, `.c`) reside exclusively in `src/`. Mixing headers and source files in the same directory is prohibited.
8. Criterion of Understanding: Creation of **self-contained documentation** understandable to any third-party engineer without external prompts.

---

### 2. Assignment Directory Artifact Structure

```
<lab>/
├── docs/                               # Business logic & math specification (pure logic, no C++)
│   ├── <n>_<topic>.md
│   ├── <n>_<topic>_architecture.md
│   └── <n>_<topic>_plan.md
├── include/                            # C++ headers (.h, .hpp) — strictly isolated!
│   ├── <topic>_types.h
│   └── <topic>_solver.h
├── src/                                # C++ source files (.cpp, .c) — no headers!
│   └── <topic>_solver.cpp
├── tests/                              # GoogleTest unit and integration tests
├── CMakeLists.txt                      # Out-of-source target-based build
└── AGENTS.md                           # Mandatory development regulation in repository root
```

---

### 3. Document Separation of Concerns

#### Business Logic Document (`docs/<n>_<topic>.md`):
* **Contains:** Physical formulation, governing equations, conservation laws, input parameter tables with SI units, boundary conditions, residual formulas, convergence criteria.
* **Strictly Prohibited:** C++ implementation details, class names, method signatures, file layouts.

#### Architecture Document (`docs/<n>_<topic>_architecture.md`):
* **Mandatory Sections:**
  1. *Context Binding:* Reference to business logic document; clear scope division ("in scope" vs "out of scope").
  2. *Data Types:* Property structs (`*_properties_t`), result structs (`*_result_t`), configuration structs. Explicit inventory of reused types vs new types.
  3. *Interfaces & Contracts:* Strict C++ method signatures with concise Doxygen using single-line `///` per line (`@brief`, `@param`, `@return`, `@throw`; multi-line `/** ... */` is strictly forbidden), access specifiers (`public` / `private`), call invariants.
  4. *Error Handling:* Exception strategy (`std::invalid_argument`, `std::runtime_error`) vs return codes.
  5. *File Layout:* Complete list of files to create and edit (`.h`, `.cpp`, `_tests.cpp`).
* **Design Principles:**
  * **Ownership vs Computation:** Task classes (`pipe_task_t`, `linear_nodal_solver_t`) orchestrate data; solvers are stateless and instantiate on demand.
  * **Pass Only What You Need:** Interfaces accept only minimal required parameters.
  * **Open-Closed Principle (OCP):** Extensibility without breaking contracts.
* **To Avoid:** Long mathematical derivations and function body implementations in the architecture document.

---

### 4. Agent Interaction Protocol
* **Permitted:**
  * Discussion and validation of phys-math formulations;
  * Code review and decomposition into clean interfaces;
  * Analysis of edge cases, conditioning, and numerical stability.
* **Prohibited:**
  * Generating entire modules blindly without approved specification and architecture;
  * Inserting unreviewed code without understanding the physical role of every variable;
  * Violating repository `AGENTS.md` rules.
