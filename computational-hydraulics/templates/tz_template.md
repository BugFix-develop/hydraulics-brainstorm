# Business Logic Specification / Technical Requirements: [Task Name]

> **Document:** `docs/<n>_<topic>.md`  
> **Status:** Draft / Under Review / Approved  
> **Associated Architecture:** `docs/<n>_<topic>_architecture.md`  

---

## 1. Problem Statement and Physical Purpose

* **Technological Purpose:** [1–2 concise paragraphs: technological role of the physical installation, inlet conditions, outlet targets, flow direction, working fluid].
* **Scope of the Current Iteration:**
  * **In Scope:** [exact calculations to be performed, physical laws modeled in this iteration];
  * **Deferred (Out of Scope):** [functionality intentionally deferred, e.g., thermal non-isothermal coupling, transient water hammer dynamics].

---

## 2. Hydraulic Network Topology and Schematic

```text
[Insert compact ASCII or Mermaid network schematic]
Example:
(Node 1: P_fixed) ───[Arc 1: Pipe]───> (Node 2: Q_outflow) ───[Arc 2: Pump]───> (Node 3: Q_inflow)
```

* **Network Graph Attributes:**
  * Node count $m = m_Q + m_P$, where $m_Q = [\dots]$ (internal flow nodes) and $m_P = [\dots]$ (reference pressure nodes, $m_P \ge 1$).
  * Branch count $n = [\dots]$.

---

## 3. Mathematical Formulation and Governing Equations

> *Note:* Equations must be stated strictly and concisely without verbose textbook derivations.

### 3.1. Conservation of Mass at Nodes (1st Kirchhoff Law)
$$A x = Q$$
where $A$ is the reduced incidence matrix ($m_Q \times n$), $x$ is the branch volumetric flow rate vector [$\text{m}^3/\text{s}$], and $Q$ is the nodal consumption/supply vector [$\text{m}^3/\text{s}$].

### 3.2. Branch Momentum Balance (2nd Kirchhoff Law / Head Loss)
$$A^T P = F(x) - A_p^T P_p$$
where:
* $F_i(x_i) = -r_i x_i + H_i$ (linear friction) or $F_i(x_i) = -s_i |x_i| x_i + H_i$ (quadratic friction with signed flow direction);
* $A_p$ is the reference node incidence matrix ($m_P \times n$), and $P_p$ is the fixed boundary pressure vector [Pa].

---

## 4. Input Data Specification (SI Units)

| Parameter | Symbol | SI Unit | Variant Value | Description |
|---|---|---|---|---|
| Fluid Density | $\rho$ | $\text{kg}/\text{m}^3$ | $850.0$ | Commercial crude oil |
| Kinematic Viscosity | $\nu$ | $\text{m}^2/\text{s}$ | $15.0 \cdot 10^{-6}$ | Viscosity ($15\text{ cSt} = 15 \cdot 10^{-6}\text{ m}^2/\text{s}$) |
| Pipe Length | $L$ | m | $1000.0$ | Section length |
| Internal Diameter | $d$ | m | $0.200$ | Internal bore |
| Reference Boundary Pressure | $P_p$ | Pa | $3.5 \cdot 10^6$ | Fixed pressure at $P$-node ($3.5\text{ MPa}$) |
| Nodal Extraction Rate | $Q$ | $\text{m}^3/\text{s}$ | $0.050$ | Volumetric extraction |

---

## 5. Verification Criteria & Benchmark Targets

1. **Analytical Benchmark:**
   * Branch 1 flow rate: $x_1^{\text{ref}} = [\dots]\text{ m}^3/\text{s}$;
   * Node 2 pressure: $P_2^{\text{ref}} = [\dots]\text{ Pa}$.
2. **Acceptable Tolerances and Residuals:**
   * Kirchhoff mass balance residual: $\Vert A x - Q \Vert_\infty < 10^{-8}\text{ m}^3/\text{s}$;
   * Normalized linear system residual: $\frac{\Vert \mathcal{A} z - b \Vert_\infty}{\Vert \mathcal{A} \Vert_\infty \Vert z \Vert_\infty + \Vert b \Vert_\infty} < 10^{-12}$;
   * Relative pressure error against benchmark: $\text{rtol} \le 10^{-4}$.
3. **Physical Invariants:**
   * Energy dissipation monotonicity ($h_f \propto Q |Q|$);
   * Zero friction head loss at zero flow ($Q = 0 \implies \Delta h = 0$);
   * Disconnection of all reference $P$-nodes must result in a singular matrix rank ($\operatorname{rank} < N$).

> [!NOTE]
> This business logic specification contains **strictly physics, governing equations, and calculation requirements**. C++ class declarations, method signatures, and file layouts belong exclusively in `docs/<n>_<topic>_architecture.md`.
