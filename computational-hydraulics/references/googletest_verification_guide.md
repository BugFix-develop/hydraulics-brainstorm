# Verification & GoogleTest Methodology in Computational Hydraulics
## Test Quality & Defense Guidelines for Developers & AI Agents (`googletest_verification_guide.md`)

> **Purpose:** Ensure a rigorous engineering methodology for unit and integration testing of computational hydraulics C++ modules. Eliminate "tautological curve-fitting tests" and prepare the student to defend the test suite during oral examination.

---

## 1. Testing Philosophy for Fluid Systems

### 1.1. Verification vs. Validation
* **Verification:** *"Are we solving the mathematical equations correctly?"* — Confirms that numerical algorithms accurately and stably solve the discrete equations (residual $\|\mathcal{A}z - b\|_\infty < 10^{-8}$, agreement with independent benchmark).
* **Validation:** *"Are we solving the right equations?"* — Confirms that the mathematical model represents physical reality (mass conservation, positive energy dissipation, monotonic head loss).

### 1.2. Strict Prohibition of Tautological Tests
> **Common AI Failure Mode:** An agent executes flawed code, obtains an erroneous numerical result (e.g., $Q = 0.0314$), and writes: `EXPECT_NEAR(flow, 0.0314, 1e-4)`. The test passes, but it permanently enshrines the error in the codebase.

#### Independent Benchmark Rule:
All reference benchmark values must originate from **strictly independent sources**:
1. Hand analytical calculations from the specification (`docs/<n>_<topic>.md`);
2. Independent reference scripts (`scripts/solve_reference.py`);
3. Fundamental physical conservation laws (nodal mass balance $\sum Q = 0$).

### 1.3. Mandatory Discussion Pause Before Creating Tests
The agent is **strictly prohibited** from immediately generating test files (`tests/*_tests.cpp`). Before writing test code, the agent must pause in chat and review with the student:
* The 4 tiers of the test pyramid and why specific scenarios were chosen;
* The lineage of benchmark values and how they were derived;
* Physical invariants (Kirchhoff balance, dissipation monotonicity, zero friction at zero flow) and edge cases (rank deficiency);
* Rationale for tolerances ($\Vert Ax - Q \Vert_\infty < 10^{-8}\text{ m}^3/\text{s}$, relative SLAE residual $< 10^{-12}$, relative pressure tolerance $\text{rtol} \le 10^{-4}$);
* Confirmation that the student understands every test assertion and is prepared to defend it.
Test code generation proceeds **only after explicit student confirmation**.

---

## 2. Four-Tier Testing Pyramid

Test suites for calculation modules are structured into 4 mandatory tiers:

```
                      ┌──────────────────────────────────────────────┐
                      │ Tier 4: Contract Validation & Exceptions     │
                      │ (EXPECT_THROW: r <= 0, d <= 0, rho <= 0)     │
                      ├──────────────────────────────────────────────┤
                      │ Tier 3: Boundary Conditions & Topology       │
                      │ (Disconnected P-node, rank deficiency)       │
                      ├──────────────────────────────────────────────┤
                      │ Tier 2: Qualitative Physical Invariants      │
                      │ (Kirchhoff ||Ax - Q|| < 1e-8, monotonicity,  │
                      │ directional Q|Q|, zero flow h_f(0) = 0)      │
                      ├──────────────────────────────────────────────┤
                      │ Tier 1: Quantitative Accuracy                │
                      │ (Independent benchmark: rtol <= 1e-4,        │
                      │ SLAE residual ||Az-b|| / ||A||||z|| < 1e-12) │
                      └──────────────────────────────────────────────┘
```

---

## 3. Numerical Rules for Floating-Point Precision (`double`)

### 3.1. Prohibition of `EXPECT_EQ` for Floating-Point Values
Floating-point values (`float`, `double`) contain machine round-off errors. Comparing via `EXPECT_EQ(a, b)` produces unpredictable failures across compilers, platforms, or optimization levels (`-O0` vs `-O3`).

### 3.2. Assertion Macros & Tolerance Justifications ($\varepsilon$)
* **`EXPECT_NEAR(actual, expected, tolerance)` — Primary Assertion Tool:**
  * Tolerances require physical and mathematical justification:
    * For linear systems in Eigen ($PA = LU$ direct solve): $\varepsilon = 10^{-8}$;
    * For nonlinear Newton solvers: tolerance matches iteration stopping criteria ($\varepsilon = 10^{-6} - 10^{-8}$).
* **`EXPECT_LT(val, threshold)` — Residual Norm Checks:**
  * Validating infinity-norm of equation residuals:
    ```cpp
    double residual = (A_block * z - b_vec).lpNorm<Eigen::Infinity>();
    EXPECT_LT(residual, 1e-8) << "Residual exceeds tolerance: " << residual;
    ```
* **`EXPECT_DOUBLE_EQ(a, b)`:**
  * Permissible only when values stem from an identical sequence of operations (within 4 ULPs).

---

## 4. GoogleTest Suite Templates (C++20)

### 4.1. Tier 1: Quantitative Accuracy on Variant Benchmark
```cpp
#include <gtest/gtest.h>
#include <Eigen/Dense>
#include "linear_nodal_solver.h"

TEST(LinearNodalSolverTest, NumericalBenchmarkVariant) {
    // 1. Initialize parameters according to approved specification
    linear_nodal_properties_t props;
    // ... populate graph, resistances r, heads H, flows Q, pressures P_p ...

    // 2. Reference values derived independently (in specification or analytical derivation)
    const std::vector<double> expected_flows = { 0.04251234, -0.01523412, 0.02727822 };
    const std::vector<double> expected_pressures = { 512345.0, 489120.0 };

    // 3. Invoke solver
    linear_nodal_solver_t solver(props);
    linear_nodal_result_t result = solver.solve();

    // 4. Verify convergence and KKT residual
    EXPECT_TRUE(result.is_converged);
    EXPECT_LT(result.max_equation_residual, 1e-8)
        << "KKT system equation failed to converge: residual = " << result.max_equation_residual;

    // 5. Component-wise branch flow check (absolute tolerance)
    ASSERT_EQ(result.branch_flow_rates.size(), expected_flows.size());
    for (std::size_t i = 0; i < expected_flows.size(); ++i) {
        EXPECT_NEAR(result.branch_flow_rates[i], expected_flows[i], 1e-8)
            << "Discrepancy in branch flow " << i;
    }

    // 6. Component-wise nodal pressure check (relative tolerance)
    ASSERT_EQ(result.nodal_pressures.size(), expected_pressures.size());
    for (std::size_t j = 0; j < expected_pressures.size(); ++j) {
        double relative_error = std::abs(result.nodal_pressures[j] - expected_pressures[j]) / std::abs(expected_pressures[j]);
        EXPECT_LT(relative_error, 1e-4)
            << "Relative error in nodal pressure " << j << " exceeded 1e-4";
    }
}
```

---

### 4.2. Tier 2: Physical Network Invariants
```cpp
// Verification of Kirchhoff's First Law (mass balance at internal nodes)
TEST(LinearNodalSolverTest, InvariantFirstKirchhoffLaw) {
    linear_nodal_properties_t props = create_test_network_properties();
    linear_nodal_solver_t solver(props);
    linear_nodal_result_t result = solver.solve();

    // Kirchhoff's First Law residual: ||A * x - Q||_inf < 1e-8
    EXPECT_LT(result.max_kirchhoff_residual, 1e-8)
        << "Conservation of mass violated at internal network nodes!";
}

// Verification of flow reversal behavior (Q|Q| vs Q^2)
TEST(PipelineHydraulicsTest, InvariantReverseFlowDissipation) {
    pipe_properties_t pipe{1000.0, 0.5, 0.0001, 0.0, 0.0};
    fluid_properties_t oil{850.0, 15e-6};
    pipe_task_t task(pipe, oil);

    double flow_forward = 0.2;  // m3/s
    double flow_reverse = -0.2; // m3/s
    double p_inlet = 2.0e6;     // 2 MPa

    double p_outlet_forward = task.solve_qp(flow_forward, p_inlet);
    double p_outlet_reverse = task.solve_qp(flow_reverse, p_inlet);

    // Forward flow: downstream pressure is lower than inlet pressure
    EXPECT_LT(p_outlet_forward, p_inlet);

    // Reverse flow (fluid travels from outlet to inlet):
    // Upstream cross-section acts as receiver, so outlet pressure must EXCEED inlet pressure:
    EXPECT_GT(p_outlet_reverse, p_inlet);

    // Magnitude of differential pressure must be symmetric:
    double delta_p_fwd = std::abs(p_inlet - p_outlet_forward);
    double delta_p_rev = std::abs(p_inlet - p_outlet_reverse);
    EXPECT_NEAR(delta_p_fwd, delta_p_rev, 1e-8);
}
```

---

### 4.3. Tiers 3 & 4: Boundary Conditions, Rank Deficiency & Contract Exceptions
```cpp
// Verification of floating network detection (missing reference P-node)
TEST(LinearNodalSolverTest, ExceptionWhenNoPressureNodes) {
    linear_nodal_properties_t props = create_test_network_properties();
    // Clear reference pressures vector
    props.boundary_pressures.clear();

    linear_nodal_solver_t solver(props);
    // Solver must detect rank deficiency and throw runtime_error:
    EXPECT_THROW(solver.solve(), std::runtime_error)
        << "Solver must throw std::runtime_error when no reference pressure nodes exist!";
}

// Verification of domain contract validation (negative branch resistance)
TEST(LinearNodalSolverTest, ExceptionOnNegativeResistance) {
    linear_nodal_properties_t props = create_test_network_properties();
    props.branch_resistances[0] = -100.0; // Unphysical negative resistance

    EXPECT_THROW({
        linear_nodal_solver_t solver(props);
        solver.solve();
    }, std::invalid_argument)
        << "Negative branch resistance must throw std::invalid_argument!";
}
```

---

## 5. Defense Questions on Test Suites (Cheat Sheet for Oral Exam)

Faculty members frequently test code comprehension through test cases:

1. **Question:** *"Which test confirms that your solver satisfies Kirchhoff's First Law?"*
   * **Answer:** *"In `test_invariants.cpp`, test `InvariantFirstKirchhoffLaw`. It multiplies the calculated branch flow vector $x$ by incidence matrix $A$ and validates the infinity-norm $\Vert Ax - Q \Vert_\infty < 10^{-8}$. This verifies that nodal mass balance closes across all $Q$-nodes."*
2. **Question:** *"Why does flow rate verification use an absolute tolerance of $10^{-8}$, while pressure verification uses a relative tolerance of `1e-4`, and why is `EXPECT_EQ` forbidden?"*
   * **Answer:** *"`EXPECT_EQ` cannot be used on floating-point values due to machine precision limitations. For volumetric discharge [$\text{m}^3/\text{s}$], absolute tolerance $10^{-8}$ ensures convergence of mass conservation under direct LU factorization. For pressure [$\text{Pa}$], an absolute tolerance of $10^{-8}$ at operational pressures of $10^6\text{ Pa}$ would demand an impossible $10^{-14}$ precision near the limit of double precision. Reference pressures are hand-calculated with 4-5 significant figures, justifying a relative tolerance of $\text{rtol} \le 10^{-4}$."*
3. **Question:** *"How does your test suite prove that fluid does not spontaneously accelerate under flow reversal?"*
   * **Answer:** *"Through test `InvariantReverseFlowDissipation`. We impose negative flow rate $Q = -0.2$ and assert that the signed formulation $Q |Q|$ dissipates energy, with the differential pressure magnitude matching forward flow."*
4. **Question:** *"What does `ExceptionWhenNoPressureNodes` test?"*
   * **Answer:** *"It models an unanchored hydraulic network without connection to an external reservoir. It verifies that `FullPivLU::isInvertible()` detects matrix singularity and throws a controlled `std::runtime_error` rather than producing `NaN` or unhandled numerical corruption."*
