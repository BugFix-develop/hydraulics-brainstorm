# Pipeline Hydraulics & Modern C++ (Semester 2 Guide)
## Systematic Reference for Lectures & Laboratory Assignments (`sem2_guide.md`)

> Primary references:
> * Lecture Course: `sem2/lecture` (Lectures 01–11)
> * Practical Assignments: `sem2/lab` (Labs 04–10)
> * Literature: M. V. Lurie (2003, 2012), I. E. Idelchik (1992), A. D. Altshul (1982), B. B. Nekrasov (1989).

---

## 1. Course Concept & Engineering Code Quality Standards

### 1.1. The Developer as a Domain Specialist
1. **Business Logic** in computational hydraulics software embodies the physical laws of nature (conservation of mass, momentum, and energy, fluid rheology, performance characteristics of pumps and fittings).
2. Code must simultaneously satisfy two pillars:
   * **(I) General Software Engineering Best Practices:** modularity, encapsulation, separation of concerns, testability, RAII.
   * **(II) Domain Specificity:** physically meaningful naming, strict SI unit consistency, physical invariant verification (monotonicity, conservation, boundary conditions).

### 1.2. Code Style & Naming Conventions
* **Style:** Strict `snake_case` across all identifiers (structures, classes, methods, functions, variables, files).
* **Type Suffix:** All structs, classes, and type aliases must end with `_t` (e.g., `pipe_geometry_t`, `fluid_properties_t`, `pipe_task_t`).
* **Expressive Physical Names:** Ambiguous single-letter abbreviations are strictly prohibited:
   * `density` instead of `rho` or `r`;
   * `kinematic_viscosity` instead of `nu` or `v`;
   * `dynamic_viscosity` instead of `mu`;
   * `flow_rate` or `volumetric_flow_rate` instead of `q`;
   * Single-letter variables are allowed only as standard mathematical parameters inside local closed-form formulas (`d`, `l`, `g`).
* **Rule of 7 Entities:** Function bodies should not handle excessive unrelated entities; complex algorithms must be decomposed into pure helper functions.

---

## 2. Build Architecture & Modern C++ Tooling

### 2.1. Compilation and Linking Stages
1. **Preprocessor (`cpp`):** Handles `#include`, `#define`, `#ifdef`, macro expansions, and comment removal. Header guards are enforced via `#pragma once`.
2. **Compilation (`c++` / `clang++`):** Lexical and syntax analysis, AST generation, semantic checks, translation to target assembly.
3. **Assembly (`as`):** Converts assembly code into relocatable object files (`.o` / `.obj`) with symbol tables (`symtab`).
4. **Linking (`ld`):** Resolves symbols across object files and libraries:
   * **ODR (One Definition Rule):** Any variable or non-`inline` function must have exactly one definition across the whole program.
   * Resolves external symbols, catching `undefined reference` and `multiple definition` errors.
   * `inline` specifier (in C++17 for functions and variables): permits identical definitions in different translation units to be merged by the linker.

### 2.2. Modern Target-Based CMake
Builds are performed strictly **Out-of-Source**:

```cmake
cmake_minimum_required(VERSION 3.20)
project(HydraulicCalc LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Computation core static library
add_library(calc_core STATIC
    src/pipe_task.cpp
    src/pump_task.cpp
    src/local_resistance_task.cpp
)
target_include_directories(calc_core PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# GoogleTest unit test executable
enable_testing()
add_executable(unit_tests
    tests/test_main.cpp
    tests/test_pipe_qp_pp.cpp
    tests/test_pumps.cpp
)
target_link_libraries(unit_tests PRIVATE
    calc_core
    GTest::gtest_main
)
include(GoogleTest)
gtest_discover_tests(unit_tests)
```

---

## 3. Mathematical Framework of Pipeline Hydraulics

### 3.1. Fundamental Flow Parameters
* **Volumetric Flow Rate** $Q$ [$\text{m}^3/\text{s}$]:
  $$Q = \frac{\Delta V}{\Delta t} = v \cdot S = v \cdot \frac{\pi d^2}{4}$$
* **Mass Flow Rate** $G$ [$\text{kg/s}$]:
  $$G = \frac{\Delta m}{\Delta t} = \rho Q = \rho v S$$
* **Mean Velocity** $v$ [$\text{m/s}$]:
  $$v = \frac{4 Q}{\pi d^2}$$

### 3.2. Bernoulli Equation for Real (Viscous) Fluids
Between upstream section 1 and downstream section 2:

$$z_1 + \frac{p_1}{\rho g} + \frac{\alpha_1 v_1^2}{2g} = z_2 + \frac{p_2}{\rho g} + \frac{\alpha_2 v_2^2}{2g} + h_{\text{loss}}$$

where:
* $z$ — elevation head [$\text{m}$].
* $\frac{p}{\rho g}$ — pressure head [$\text{m}$] ($p$ is static pressure in $\text{Pa}$).
* $H_{\text{piezo}} = z + \frac{p}{\rho g}$ — piezometric head [$\text{m}$].
* $H = z + \frac{p}{\rho g} + \frac{\alpha v^2}{2g}$ — total hydrodynamic head [$\text{m}$].
* $\alpha$ — Coriolis kinetic energy correction coefficient:
  * $\alpha = 2.0$ — laminar flow;
  * $\alpha \approx 1.05 - 1.1$ — turbulent flow (for long pipelines where $v_1 \approx v_2$, kinetic energy difference is neglected).
* $h_{\text{loss}} = h_f + \sum h_m$ — total head loss [$\text{m}$].

### 3.3. Friction Head Loss (Darcy–Weisbach)
$$h_f = \lambda \frac{L}{d} \frac{v |v|}{2g} = \frac{8 \lambda L}{\pi^2 g d^5} Q |Q|$$

Pressure drop due to friction:
$$\Delta p_f = \rho g h_f = \frac{8 \lambda L \rho}{\pi^2 d^5} Q |Q|$$

Hydraulic gradient:
$$i = \frac{h_f}{L} = \frac{\lambda}{d} \frac{v^2}{2g}$$

### 3.4. Reynolds Number and Flow Regimes
$$\text{Re} = \frac{v d}{\nu} = \frac{4 |Q|}{\pi d \nu} = \frac{4 |G|}{\pi d \mu}$$

Critical transition Reynolds number: $\text{Re}_{\text{crit}} \approx 2320$.

#### Friction Factor Laws $\lambda(\text{Re}, k_e/d)$:
1. **Laminar Regime ($\text{Re} < 2320$):**
   $$\lambda = \frac{64}{\text{Re}}$$
   Head loss is **strictly linear** with respect to discharge:
   $$h_f = \frac{128 \nu L}{\pi g d^4} Q$$
2. **Turbulent Flow in Smooth Pipes ($2320 \le \text{Re} < 10 \frac{d}{k_e}$):**
   * Blasius formula ($\text{Re} < 10^5$):
     $$\lambda = \frac{0.3164}{\text{Re}^{0.25}}$$
   * Head loss is proportional to $Q^{1.75}$.
3. **Transition / Mixed Friction Zone ($10 \frac{d}{k_e} \le \text{Re} \le 500 \frac{d}{k_e}$):**
   * Altshul formula (industry standard):
     $$\lambda = 0.11 \left( \frac{k_e}{d} + \frac{68}{\text{Re}} \right)^{0.25}$$
4. **Fully Rough Quadratic Zone ($\text{Re} > 500 \frac{d}{k_e}$):**
   * Shifrinson formula (self-similar regime, $\lambda$ independent of $\text{Re}$):
     $$\lambda = 0.11 \left( \frac{k_e}{d} \right)^{0.25}$$
   * Head loss is **strictly quadratic**: $h_f = s \cdot Q |Q|$.

---

## 4. Pipeline Problem Classification: QP and PP Formulations

### 4.1. Lumped QP Problem (Flow Rate → Pressure)
* **Given:** Pipe geometry ($L, d, k_e$), fluid properties ($\rho, \nu$), flow rate $Q$, inlet pressure $p_1$ (or outlet pressure $p_2$).
* **Target:** Pressure at the opposite end ($p_2$ or $p_1$).
* **Direct Analytical Algorithm:**
  1. Calculate velocity $v = \frac{4 Q}{\pi d^2}$ and Reynolds number $\text{Re} = \frac{v d}{\nu}$.
  2. Determine flow regime and compute $\lambda$.
  3. Calculate friction head loss $h_f = \lambda \frac{L}{d} \frac{v^2}{2g}$.
  4. Compute downstream pressure:
     $$p_2 = p_1 - \rho g (z_2 - z_1) - \rho g h_f$$
  *(For reverse problem with known $p_2$: $p_1 = p_2 + \rho g (z_2 - z_1) + \rho g h_f$)*.

### 4.2. Distributed QP Problem (Elevation Profiling)
* **Given:** Pipeline profile coordinates $x = \{x_0, x_1, \dots, x_{n-1}\}$, elevation coordinates $z = \{z_0, z_1, \dots, z_{n-1}\}$, inlet pressure $p_{\text{inlet}}$, flow rate $Q$.
* **Objective:** Compute pressure distribution $p(x)$ to verify pipe yield limits and prevent cavitation ($p(x) > p_{\text{vapor}}$).
* **Step-by-Step Integration Algorithm ($\Delta x_j = x_{j+1} - x_j$):**
  1. Determine inlet total head:
     $$H_0 = z_0 + \frac{p_{\text{inlet}}}{\rho g} + \frac{\alpha v^2}{2g}$$
  2. Calculate head profile using hydraulic slope $i$:
     $$H_{j+1} = H_j - i \cdot \Delta x_j$$
  3. Reconstruct static pressure profile:
     $$p_j = \rho g \left( H_j - z_j - \frac{\alpha v^2}{2g} \right)$$
  4. Export profile array $\{x_j, z_j, H_j, p_j\}$ to CSV for validation and plotting.

### 4.3. Lumped PP Problem (Pressures → Flow Rate)
* **Given:** Pipe geometry, fluid properties, pressures at both ends $p_1, p_2$.
* **Target:** Volumetric flow rate $Q$.
* **Mathematical Complexity:**
  $$\frac{p_1 - p_2}{\rho g} + (z_1 - z_2) = \lambda(\text{Re}(Q)) \cdot \frac{L}{d} \cdot \frac{8 Q |Q|}{\pi^2 g d^5}$$
  Because $\lambda$ depends on $\text{Re}$, which itself is proportional to $Q$, the equation is **nonlinear algebraic**.
* **Numerical Formulation:** Define residual function:
  $$r(Q) = p_{2, \text{calc}}(p_1, Q) - p_{2, \text{target}} = 0$$
  Solve root finding problem $r(Q) = 0$ via Bisection or Safeguarded Newton methods.

---

## 5. Minor Losses and Pumping Stations

### 5.1. Weisbach Law for Minor Losses
$$\Delta h_m = \zeta \frac{v |v|}{2g}$$

Because minor losses are localized ($z_{\text{in}} = z_{\text{out}}$), piezometric head drop equals total head drop: $\Delta h_m = \Delta H$.

* **Borda–Carnot Sudden Expansion ($d_1 \to d_2$):**
  $$\zeta = \left( 1 - \frac{d_1^2}{d_2^2} \right)^2 \quad (\text{referenced to } v_1)$$
* **Orifice in Pipe ($n = d_{\text{orifice}}/d_{\text{pipe}}$):**
  $$\zeta = \left( \frac{1}{n \cdot \varepsilon} - 1 \right)^2, \quad \varepsilon = 0.57 + \frac{0.043}{1.1 - n}$$

### 5.2. Centrifugal Pump Modeling
Pump differential head curve ($Q\text{-}H$ characteristic):
$$\Delta H_{\text{pump}}(Q) = a - b \cdot Q |Q| \quad (\text{or quadratic form } a - b Q^2)$$

where $a$ is shutoff head and $b$ is characteristic slope.

* **QP Problem for Pump:**
  $$p_{\text{outlet}} = p_{\text{inlet}} + \rho g \cdot \Delta H_{\text{pump}}(Q)$$
* **PP Problem for Pump:**
  $$Q(\Delta H) = \operatorname{sign}(a - \Delta H) \sqrt{\left| \frac{a - \Delta H}{b} \right|}, \quad \text{where } \Delta H = \frac{p_{\text{outlet}} - p_{\text{inlet}}}{\rho g}$$

### 5.3. Multiple Pump Stations
1. **Series Configuration ($Q = \text{const}$):**
   Heads sum up:
   $$\Delta H_{\Sigma}(Q) = \sum_{k=1}^m \Delta H_k(Q) = \left( \sum a_k \right) - \left( \sum b_k \right) Q^2$$
2. **Parallel Configuration ($\Delta H = \text{const}$):**
   Flow rates sum up:
   $$Q_{\Sigma}(\Delta H) = \sum_{k=1}^m Q_k(\Delta H)$$

### 5.4. Operating Point Determination
Head balance equation:
$$H_{\text{pump}}(Q) = \Delta z_{\text{elev}} + h_f(Q) + h_{\text{res}}$$
$$a - b Q^2 = (z_{\text{outlet}} - z_{\text{inlet}}) + s \cdot Q^2 + h_{\text{res}}$$

Analytical solution for quadratic region:
$$Q_{\text{op}} = \sqrt{\frac{a - (z_{\text{outlet}} - z_{\text{inlet}}) - h_{\text{res}}}{b + s}}$$

---

## 6. Numerical Solvers for Nonlinear Equations

### 6.1. Bisection Method
* Grounded in the Bolzano–Cauchy theorem: if $r(a) \cdot r(b) < 0$, a root is guaranteed on $[a, b]$.
* Midpoint updated at each iteration: $c = \frac{a + b}{2}$.
* Convergence error reduces strictly by factor of 2 per step:
  $$\varepsilon_k = \frac{b_0 - a_0}{2^k}$$

#### Standard C++ Signature:
```cpp
double solve_bisection(
    const std::function<double(double)>& residual_func,
    double left,
    double right,
    double tolerance = 1e-8,
    std::size_t max_iterations = 100
);
```

### 6.2. Newton–Raphson Method and Safeguarded Newton
* Quadratic rate of convergence in the neighborhood of the root:
  $$x_{k+1} = x_k - \frac{r(x_k)}{r'(x_k)}$$
* Derivative $r'(x)$ can be analytical or evaluated via central difference:
  $$r'(x) \approx \frac{r(x + \delta) - r(x - \delta)}{2 \delta}$$

> [!TIP] Safeguarded Newton Method in Hydraulic Problems
> The piecewise function $\lambda(\text{Re})$ features a jump discontinuity of $\approx +65\%$ at $\text{Re} = 2320$. Pure Newton steps near this boundary can oscillate or produce unphysical steps ($Q < 0$ when $p_1 > p_2$).
>
> **Best Practices:**
> 1. **Bracketing & Hybrid Step:** Identify interval $[Q_{\min}, Q_{\max}]$ where $r(Q_{\min}) \cdot r(Q_{\max}) \le 0$. If the proposed Newton iterate falls outside this bracket or fails to achieve sufficient decrease, fallback to a bisection step.
> 2. **Churchill Smooth Correlation (1977):** When continuous differentiability across all $\text{Re} > 0$ is required, Churchill's correlation seamlessly spans laminar, transitional, and turbulent regimes without derivative discontinuities.

#### Standard C++ Signatures:
```cpp
double solve_newton(
    const std::function<double(double)>& residual_func,
    const std::function<double(double)>& residual_derivative_func,
    double initial_guess,
    double tolerance = 1e-8,
    std::size_t max_iterations = 100
);

// Hybrid safeguarded solver with guaranteed global convergence
double solve_safeguarded_newton(
    const std::function<double(double)>& residual_func,
    const std::function<double(double)>& residual_derivative_func,
    double bracket_low,
    double bracket_high,
    double tolerance = 1e-8,
    std::size_t max_iterations = 100
);
```

---

## 7. Evolution of OOP Calculation Core Architecture

```
Lab 5: Free functions -> 
Lab 6: Domain property structs -> 
Lab 8: Task Pattern encapsulation -> 
Lab 10: Polymorphic hydraulic pipelines
```

### 7.1. Domain Data Model
```cpp
struct pipe_geometry_t {
    double length{0.0};               ///< Pipe length [m]
    double diameter{0.0};             ///< Internal diameter [m]
    double equivalent_roughness{0.0}; ///< Equivalent roughness [m]
    double z_inlet{0.0};              ///< Upstream elevation [m]
    double z_outlet{0.0};             ///< Downstream elevation [m]
};

struct oil_properties_t {
    double density{0.0};             ///< Fluid density [kg/m3]
    double kinematic_viscosity{0.0}; ///< Kinematic viscosity [m2/s]
};

struct hydraulic_state_t {
    double flow_rate{0.0};       ///< Volumetric flow rate [m3/s]
    double inlet_pressure{0.0};  ///< Inlet static pressure [Pa]
    double outlet_pressure{0.0}; ///< Outlet static pressure [Pa]
    double head_loss{0.0};       ///< Total head loss [m]
};
```

### 7.2. Task Architectural Pattern
Each physical domain entity encapsulates its parameters and solver logic:
```cpp
class pipe_task_t {
private:
    pipe_geometry_t geometry_;
    oil_properties_t fluid_;

public:
    pipe_task_t(const pipe_geometry_t& geom, const oil_properties_t& fluid)
        : geometry_(geom), fluid_(fluid) {}

    /// @brief Solves QP formulation (known flow rate and inlet pressure)
    /// @param flow_rate Volumetric flow rate [m3/s]
    /// @param p_inlet Upstream pressure [Pa]
    /// @return Downstream pressure [Pa]
    double solve_qp(double flow_rate, double p_inlet) const;

    /// @brief Solves PP formulation (known endpoint pressures)
    /// @param p_inlet Upstream pressure [Pa]
    /// @param p_outlet Downstream pressure [Pa]
    /// @return Volumetric flow rate [m3/s]
    double solve_pp(double p_inlet, double p_outlet) const;
};
```

### 7.3. Polymorphism for Composite Pipeline Networks
A unified polymorphic base class calculates head losses across heterogeneous elements (pipes, valves, pumps):

```cpp
class hydraulic_element_t {
public:
    virtual ~hydraulic_element_t() = default;

    /// @brief Calculates head loss across element at given flow rate
    /// @param flow_rate Volumetric flow rate [m3/s]
    /// @return Head loss [m] (negative for pumps representing head rise)
    virtual double calc_head_loss(double flow_rate) const = 0;
};

// QP evaluation along polymorphic pipeline chain
double solve_chain_qp(
    const std::vector<std::shared_ptr<hydraulic_element_t>>& chain,
    double flow_rate,
    double p_inlet,
    double density,
    double delta_z_total
) {
    constexpr double standard_gravity = 9.80665;
    double total_head_loss = 0.0;
    for (const auto& element : chain) {
        total_head_loss += element->calc_head_loss(flow_rate);
    }
    double h_inlet = p_inlet / (density * standard_gravity);
    double h_outlet = h_inlet - delta_z_total - total_head_loss;
    return h_outlet * (density * standard_gravity);
}
```

The PP problem for the composite chain is solved by wrapping `solve_chain_qp` in a numerical root finder.

---

## 8. GoogleTest Verification & Validation Guidelines

1. **Quantitative Verification:**
   * Benchmark against manual analytical calculations:
     ```cpp
     EXPECT_NEAR(result, benchmark, 1e-4);
     ```
2. **Qualitative Physical Validation:**
   * In QP formulations: as flow rate $Q$ increases, downstream pressure $p_2$ must strictly decrease ($\partial p_2 / \partial Q < 0$).
   * In PP formulations: as inlet pressure $p_1$ increases, flow rate $Q$ must strictly increase ($\partial Q / \partial p_1 > 0$).
   * At zero flow $Q = 0$: friction loss is identically zero; differential pressure is purely hydrostatic $p_1 - p_2 = \rho g (z_2 - z_1)$.
   * For pumps: increasing system backpressure must decrease operating flow rate.
