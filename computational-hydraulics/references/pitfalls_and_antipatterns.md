# Repository of Common Pitfalls & Anti-Patterns in Hydraulics & TGC
## Error Prevention Guide for Developers & AI Agents (`pitfalls_and_antipatterns.md`)

This guide accumulates practical lessons and troubleshooting patterns from pipeline hydraulic modeling, C++ numerical solver implementations, and the Theory of Hydraulic Circuits (TGC).

---

## 1. Physical and Hydrodynamic Pitfalls

### Pitfall 1.1: Using $Q^2$ Instead of $Q |Q|$ (Reverse Flow Pitfall)
* **The Root Cause:** In Darcy–Weisbach and minor loss formulations, head drop is often colloquially written as $\Delta p = s Q^2$. In closed loops or under shifting boundary heads, flow can reverse direction ($Q < 0$), but $Q^2 > 0$.
* **The Consequence:** Friction losses begin injecting energy into the fluid instead of dissipating it (creating an unphysical "perpetual motion machine"), causing Newton or GGM solvers to instantly diverge.
* **The Fix:** ALWAYS preserve the sign of velocity and discharge:
  $$\Delta p_f = s \cdot Q |Q| \qquad \text{or} \qquad \Delta h_f = \lambda \frac{L}{d} \frac{v |v|}{2g}$$

---

### Pitfall 1.2: Confusing Active Head Dimensions ($H$) in TGC
* **The Root Cause:** In classical hydraulics, head $H$ is measured in **meters of liquid column** [$\text{m}$]. In the Theory of Hydraulic Circuits (Merenkov, Yuzhanin), active branch head $H_i$ is expressed in **Pascals** [$\text{Pa}$].
* **The Consequence:** Substituting pump head $a$ [$\text{m}$] directly into Kirchhoff's Second Law $A^T P = F(x)$ without multiplying by $\rho g$ underestimates pressure rise by a factor of $\sim 8500 - 9800$ ($\rho g$).
* **The Fix:**
  $$H_{\text{TGC}} = \rho \cdot g \cdot H_{\text{pump, m}} \quad [\text{Pa}]$$

---

### Pitfall 1.3: Elevation Difference Sign Reversal ($\Delta z$)
* **The Root Cause:** In the Bernoulli equation from upstream node 1 to downstream node 2:
  $$p_1 - p_2 = \rho g (z_2 - z_1) + \Delta p_f$$
  When fluid moves uphill ($z_2 > z_1$), outlet pressure $p_2$ drops, increasing required differential $p_1 - p_2$.
* **The Consequence:** Sign errors cause fluid to flow "uphill" without potential energy expenditure.
* **The Fix:** In branch closure relation $y_i = f_i(x_i) - H_i$:
  $$H_i = \rho g (z_{\text{inlet}} - z_{\text{outlet}})$$
  When the pipe ascends ($z_{\text{inlet}} < z_{\text{outlet}}$), $H_i < 0$, and required pressure drop $y_i = f_i - (-|H|) = f_i + |H|$ increases.

---

### Pitfall 1.4: Confusing Dynamic ($\mu$) and Kinematic ($\nu$) Viscosity
* **The Root Cause:** Dynamic viscosity $\mu$ is measured in $[\text{Pa}\cdot\text{s}]$ (or centipoise, $\text{cP}$). Kinematic viscosity $\nu = \mu / \rho$ is measured in $[\text{m}^2/\text{s}]$ (or centistokes, $\text{cSt}$).
* **The Consequence:** Passing dynamic viscosity into the Reynolds formula $\text{Re} = \frac{v d}{\nu}$ underestimates Reynolds number by a factor of $\rho$ ($\approx 800 - 1000\times$). A turbulent stream with $\text{Re} = 50\,000$ gets misclassified as laminar ($\text{Re} = 50$), invoking Poiseuille instead of Altshul.
* **The Fix:**
  $$\nu = \frac{\mu}{\rho}, \qquad 1\text{ cSt} = 10^{-6}\text{ m}^2/\text{s}, \qquad 1\text{ cP} = 10^{-3}\text{ Pa}\cdot\text{s}$$

---

### Pitfall 1.5: Using Friction Formulas Outside Valid Reynolds Ranges
* **The Root Cause:** Applying the Blasius formula $\lambda = 0.3164 / \text{Re}^{0.25}$ to aged, corroded commercial steel pipes with large relative roughness $k_e / d$.
* **The Consequence:** Blasius is valid strictly for **hydraulically smooth pipes** ($\text{Re} < 10 d/k_e$). In commercial pipelines, flow is in the mixed or fully rough regime, where Blasius underestimates friction by $30 - 50\%$.
* **The Fix:** Check $\text{Re}$ bounds and apply the Altshul or Swamee–Jain correlation:
  $$\lambda = 0.11 \left(\frac{k_e}{d} + \frac{68}{\text{Re}}\right)^{0.25}$$

---

## 2. Topological and Graph Pitfalls in TGC

### Pitfall 2.1: Floating Hydrostatic Datum (Missing $P$-Node)
* **The Root Cause:** Attempting to solve flow distribution in a network where only inflows/outflows are defined at nodes ($Q$-nodes), with no fixed-pressure node ($m_P = 0$).
* **The Consequence:** The incidence matrix has rank $m - 1$. Node pressures are determined only up to an arbitrary additive constant $P + C$. The SLAE becomes singular ($\operatorname{rank} < N$), determinant vanishes, and solvers fail or yield `NaN`.
* **The Fix:** Every physically realizable hydraulic network must specify **at least one** reference $P$-node ($m_P \ge 1$) anchoring absolute pressure datum (storage tank, reservoir, header connection).

---

### Pitfall 2.2: Sign Confusion in Incidence Matrix $\bar{A}$
* **The Root Cause:** Inconsistent definition of $+1$ and $-1$ signs.
* **ATP / TGC Standard:**
  $$
  \bar{A}_{j, i} = \begin{cases}
  +1, & \text{branch } i \text{ LEAVES node } j \text{ (outflow)}; \\
  -1, & \text{branch } i \text{ ENTERS node } j \text{ (inflow)}.
  \end{cases}
  $$
* **The Consequence:** Inverting signs in $\bar{A} x = Q$ turns sources into consumers and deliveries into leaks.
* **The Invariant Check:** Every column sum of the full incidence matrix must equal zero:
  $$\sum_{j=1}^m \bar{A}_{j, i} = 0 \quad \text{for every column } i$$

---

### Pitfall 2.3: Unhandled $PP$-Branches (Connecting Two Fixed-Pressure Nodes)
* **The Root Cause:** A branch connects node $A$ and node $B$, where *both* endpoints have fixed pressures ($P_A = P_{p1}$, $P_B = P_{p2}$).
* **The Consequence:** Such a branch operates independently of interior nodes. Retaining it in standard reduced matrix $A$ creates row/column mismatches and singular sub-blocks.
* **The Fix:** Decouple $PP$-branches during topological preprocessing. Flow along a $PP$-branch is solved independently: $x_{pp} = F^{-1}(P_{p1} - P_{p2})$.

---

## 3. Numerical and Matrix Pitfalls in Eigen

### Pitfall 3.1: Explicit Matrix Inversion `A.inverse() * b`
* **The Root Cause:** Writing `auto x = A.inverse() * b;` to solve a system.
* **Why It Is Prohibited:**
  1. **Algorithmic Complexity:** Computing $A^{-1}$ takes $\sim 2 n^3$ operations, whereas $PA = LU$ factorization in `PartialPivLU` takes $\sim \frac{2}{3} n^3$ operations ($3\times$ faster).
  2. **Numerical Instability:** Explicit inversion accumulates round-off error when the condition number is high ($\operatorname{cond}(A) \gg 1$).
* **The Fix:**
  ```cpp
  Eigen::PartialPivLU<Eigen::MatrixXd> solver(A);
  Eigen::VectorXd x = solver.solve(b);
  ```

---

### Pitfall 3.2: Checking Rank via `PartialPivLU` Instead of `FullPivLU`
* **The Root Cause:** Attempting to query rank from a `PartialPivLU` object.
* **Why It Fails:** `PartialPivLU` pivots only along columns. It cannot reliably determine numerical rank for rank-deficient systems and lacks thresholding for small singular values.
* **The Fix:**
  ```cpp
  // Rank and invertibility checks ALWAYS use FullPivLU:
  Eigen::FullPivLU<Eigen::MatrixXd> lu(A);
  if (!lu.isInvertible()) {
      throw std::runtime_error("System matrix is singular or rank-deficient!");
  }
  Eigen::VectorXd x = lu.solve(b);
  ```

---

### Pitfall 3.3: Applying Cholesky (`LLT` / `LDLT`) to Indefinite KKT Block Matrix
* **The Root Cause:** The block matrix $\mathcal{A} = \begin{pmatrix} R & A^T \\ A & 0 \end{pmatrix}$ is symmetric, tempting developers to use `Eigen::LLT`.
* **Why It Fails:** Cholesky factorization requires **strictly positive-definite** matrices. The KKT saddle-point matrix is **indefinite** (possesses both positive and negative eigenvalues, with a zero lower-right block). `LLT` fails or outputs garbage.
* **The Fix:** Use `Eigen::FullPivLU`, `Eigen::PartialPivLU`, or Schur complement block elimination.

---

### Pitfall 3.4: Division by Zero in Nodal Pressure Method (NPM) when $Q \to 0$
* **The Root Cause:** In NPM, derivative of inverse characteristic is:
  $$\frac{\partial \psi_i}{\partial \Delta P_i} = \frac{1}{\frac{d f_i}{d x_i}} = \frac{1}{2 s_i |x_i|}$$
  When flow in any branch approaches zero ($x_i \approx 0$), the derivative blows up ($1 / 0 \to \infty$).
* **The Consequence:** Jacobian matrix entries become `Inf` or `NaN`, causing Newton solvers to fail.
* **The Fix:**
  1. In NPM, apply analytical regularization near origin: $\frac{d f_i}{d x_i} \approx 2 s_i \sqrt{x_i^2 + \varepsilon^2}$.
  2. In GGM, regularize diagonal of resistance Jacobian: $d_i = \max(2 s_i |x_i|, d_{\min})$ with $d_{\min} \sim 10^{-6}\dots 10^{-8}$, and initialize with non-zero flow velocity ($v_0 = 1.0\text{ m/s}$).

---

## 4. Software & Architectural Anti-Patterns in C++

### Anti-Pattern 4.1: Stateful Solvers ("Solver Owns Problem State")
* **Bad:** Storing mesh vectors and pipe parameters as mutable fields inside the solver class, retaining state across invocations.
* **Good:** Follow the stateless Task Pattern:
  * Input data resides in immutable `*_properties_t` structs;
  * The solver is lightweight and returns a clean `*_result_t` struct.

### Anti-Pattern 4.2: Magic Numbers in Calculation Code
* **Bad:** `double head = dp / (850 * 9.81);`
* **Good:**
  ```cpp
  constexpr double standard_gravity = 9.80665;
  double head = pressure_drop / (density * standard_gravity);
  ```

### Anti-Pattern 4.3: Violating "Pass Only What You Need"
* **Bad:** Passing the entire network graph into a local function that computes head loss across a single bend.
* **Good:** The local resistance function takes only local diameter, velocity, and bend curvature radius.
