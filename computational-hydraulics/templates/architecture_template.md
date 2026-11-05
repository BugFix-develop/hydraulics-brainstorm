# Software Architecture Specification: [Task Name]

> **Document:** `docs/<n>_<topic>_architecture.md`  
> **Status:** Draft / Under Review / Approved  
> **Based on Business Logic / Requirements:** `docs/<n>_<topic>.md`  
> **Target Standard:** C++20 (with Eigen Library)  

---

## 1. Architectural Scope and Boundaries

* **System Component:** Architecture of the computational module for [concise task name], implementing the business logic defined in `docs/<n>_<topic>.md`.
* **Implementation Boundaries (1 Architecture Doc = 1 Cohesive Implementation Unit):**
  * **In Scope:**
    * Input parameter and calculation result structures;
    * Solver / task class implementation;
    * GoogleTest suite (analytical accuracy, physical invariants, boundary singularities).
  * **Deferred (Out of Scope):**
    * [e.g., transient water hammer simulation, non-isothermal thermal hydraulics].

---

## 2. Codebase Inspection & Code Reuse (DRY Rule)

> [!IMPORTANT]
> **Mandatory Rule:** Existing types, mathematical utilities, and classes in the repository **must not be recreated from scratch**. They must be reused directly via `#include`.

* **Reused Entities from Existing Codebase:**
  * `[e.g., include/hydraulic_types.h::fluid_properties_t]` — fluid physical properties (density, viscosity);
  * `[e.g., include/math_utils.h::sign()]` — signed flow direction helper;
  * `[e.g., include/graph_types.h::basic_graph_t]` — network incidence matrix assembly.
* **New Entities (Designed Specifically for this Task):**
  * Described in Section 3 below.

---

## 3. User Data Types (C++20)

### 3.1. Input Properties Structure (`[task_name]_properties_t`)
Stores immutable physical and topological parameters required for computation. Contains no business methods.
* **Contract:** Vector dimensions must strictly match network graph topology ($n$, $m_Q$, $m_P$); branch resistance values must be strictly positive ($r_i > 0$).

```cpp
struct [task_name]_properties_t {
    basic_graph_t graph;                     ///< Directed network graph
    std::vector<double> branch_resistances;   ///< Branch resistance coefficients r_i [Pa/(m3/s)]
    std::vector<double> branch_active_heads;  ///< Active pump heads H_i [Pa]
    std::vector<double> nodal_inflows;        ///< Nodal consumption/supply rates Q_j [m3/s]
    std::vector<double> boundary_pressures;   ///< Fixed reference boundary pressures P_{p, k} [Pa]
};
```

### 3.2. Calculation Result Structure (`[task_name]_result_t`)
Returns computed flow distributions and diagnostic numerical convergence indicators to the caller.
* **Contract:** If `is_converged == false`, output arrays contain `NaN` and must not be used in downstream calculations.

```cpp
struct [task_name]_result_t {
    std::vector<double> branch_flow_rates;    ///< Calculated branch flow rates x [m3/s]
    std::vector<double> nodal_pressures;      ///< Calculated nodal pressures P [Pa]
    double max_equation_residual{0.0};        ///< Maximum normalized linear system residual
    double max_kirchhoff_residual{0.0};       ///< Maximum nodal mass balance residual [m3/s]
    bool is_converged{false};                 ///< Numerical convergence flag
};
```

---

## 4. Class Interfaces & Contracts

### 4.1. Solver Class (`[task_name]_solver_t`)
The solver executes pure mathematical computations and holds no mutable state across calls.

```cpp
class [task_name]_solver_t {
public:
    /**
     * @brief Constructs solver with fail-fast input validation
     * @param properties Immutable problem parameters
     * @throw std::invalid_argument on dimension mismatch or r_i <= 0
     */
    explicit [task_name]_solver_t(const [task_name]_properties_t& properties);

    /**
     * @brief Computes network flow and pressure distribution
     * @return Computed branch flow rates, nodal pressures, and residuals
     * @throw std::runtime_error on singular network matrix (rank deficient)
     */
    [task_name]_result_t solve() const;

private:
    const [task_name]_properties_t& properties_;

    /// @brief Assembles block KKT matrix A_block and right-hand side vector b_vec
    void assemble_system(Eigen::MatrixXd& A_block, Eigen::VectorXd& b_vec) const;
};
```

* **Invocation Invariants:**
  * Prior to calling `solve()`, the object must be successfully initialized with validated `properties_`;
  * `solve()` is `const` and idempotent (repeated invocations yield identical numerical results).

---

## 5. Design Decision Justification

1. **Motivation of Choices:**
   * Singularity rank checking and system solving are conducted in a single pass using `Eigen::FullPivLU` (`lu.isInvertible()`, `lu.solve(b)`). This guarantees numerical stability for ill-conditioned systems and eliminates redundant $O(n^3)$ factorizations.
   * Explicit matrix inversion (`A.inverse() * b`) is strictly prohibited.
2. **Ownership vs Calculation:**
   * Input data is owned by the calling code; the solver holds only a `const` reference and is created on demand.
3. **Pass Only What You Need:**
   * Interfaces accept only minimal required data structures, eliminating coupling to global application state.
4. **Open/Closed Principle (OCP):**
   * If nonlinear friction models are introduced, the public `solve()` signature remains intact; iterations are encapsulated inside private solver routines.

---

## 6. Error Handling & Edge Cases

| Condition / Error | Response | Justification |
|---|---|---|
| Topology vector dimension mismatch | Throw `std::invalid_argument` | Contract precondition violation prior to solve |
| Non-positive branch resistance ($r_i \le 0$) | Throw `std::invalid_argument` | Violation of physical passive dissipation invariant |
| Missing reference $P$-nodes ($m_P = 0$) | Throw `std::invalid_argument` | Network is hydrostatically ungrounded |
| Singular matrix rank ($\operatorname{rank} < N$) | Throw `std::runtime_error` | System lacks a unique mathematical solution |
| Residual exceeds tolerance ($\varepsilon > 10^{-8}$) | Set `is_converged = false` | Warning of numerical precision degradation |

---

## 7. Project File Placement

```text
<lab>/
├── include/
│   ├── [task_name]_types.h            # New property and result structures only
│   └── [task_name]_solver.h           # Solver class declaration with Doxygen contracts
├── src/
│   └── [task_name]_solver.cpp         # System assembly and Eigen numerical routines
└── tests/
    ├── test_[task_name]_numerical.cpp  # Quantitative analytical accuracy benchmarks
    └── test_[task_name]_invariants.cpp # Physical invariants and singularity assertions
```

> [!NOTE]
> Architecture specifications **must not** contain function body implementations or long mathematical derivations. All design options must be firmly resolved (avoiding ambiguous "either this or that" phrases).
