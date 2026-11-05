# Linear Algebra in Eigen, Graph Theory & Hydraulic Networks (Semester 3 Guide)
## Systematic Reference for Lectures, Labs & Circuit Theory (`sem3_guide.md`)

> Primary references:
> * Lecture Course: `sem3/lecture` (Lectures 4, 5, 6)
> * Practical Assignments: `sem3/lab` (Labs 0, 1, 2)
> * Theory of Hydraulic Circuits: `yuzhanin-circuits-essentials.md` (V. V. Yuzhanin)
> * Agentic Development Requirements: `agentic_development_requirements.md`

---

## 1. Agentic Development Regulation & Context Management

### 1.1. Developer as Context Manager
In agentic pair programming, the developer's core responsibility is **mitigating cognitive risks**.
The risk is that AI-generated code might solve an isolated scenario incorrectly or violate core physical invariants. The developer must formalize the physics, mathematics, and architecture before code implementation begins.

### 1.2. Project Documentation Separation Standard
All project documentation is strictly decomposed into three independent artifacts:

| Artifact | File Path | Content | Strictly Prohibited |
|---|---|---|---|
| **Business Logic & Mathematics (Spec)** | `docs/*-tz.md` or `docs/*-math.md` | Mathematical model, problem formulation, physical equations, conservation laws, SI units, physical ranges, boundary conditions | C++ implementation details, class declarations, file layouts |
| **Architectural Design** | `docs/*-architecture.md` | Data structures (`*_properties_t`, `*_result_t`), solver classes, memory ownership, Doxygen method signatures, call contracts, exception handling | Mathematical formula derivations |
| **Implementation Plan** | `docs/*-plan.md` | Step-by-step atomic checklist, modified files list, testing and verification checkpoints | Redundant theoretical narratives |
| **Agent Regulation** | `AGENTS.md` (root) | Code formatting rules, safety standards, verification and test requirements for AI agents | — |

---

## 2. Linear Algebra and the Eigen Library

### 2.1. Systems of Linear Algebraic Equations (SLAE)
In matrix form:
$$A x = b$$
where $A \in \mathbb{R}^{m \times n}$ is the coefficient matrix, $x \in \mathbb{R}^n$ is the unknown vector, and $b \in \mathbb{R}^m$ is the right-hand side vector.

### 2.2. Gaussian Elimination vs. Matrix Inversion: Algorithmic Complexity
1. **Gaussian Elimination (LU Factorization):**
   * Forward elimination (reduction to upper triangular form): $\sim \frac{2}{3} n^3$ operations (FMA — fused multiply-add).
   * Back substitution: $\sim n^2$ operations.
   * Total complexity: $\sim \frac{2}{3} n^3$.
2. **Solution via Explicit Matrix Inversion ($x = A^{-1} b$):**
   * Computing $A^{-1}$ is equivalent to solving $n$ systems with identity RHS vectors: $\sim 2 n^3$ operations.
   * Matrix-vector multiplication $A^{-1} b$: $\sim 2 n^2$ operations.
   * **Conclusion:** Solving via explicit $A^{-1}$ is **3 times slower** and induces catastrophic round-off error accumulation.
   > **STRICT BAN:** Calls like `A.inverse() * b` are **strictly prohibited** in solver code.

### 2.3. $LU$ Factorization with Partial Pivoting ($PA = LU$)
For repeated solutions with constant matrix $A$ and varying RHS vectors $b$:
$$A = L \cdot U$$
where $L$ is unit lower triangular and $U$ is upper triangular.
* **Pivoting for numerical stability:** Row permutations using permutation matrix $P$ avoid zero/small pivots and division by near-zero:
  $$P A = L \cdot U$$
* **Two-step rapid back/forward solve ($O(n^2)$ operations):**
  1. $L y = P b$ (forward substitution);
  2. $U x = y$ (back substitution).

### 2.4. Well-Posedness and Rank Analysis of SLAE
Before solving an $n \times n$ system, the solver verifies the rank of coefficient matrix $A$ and augmented matrix $(A \mid b)$:

```
                  ┌─── rank(A) == n ───────────────────> WELL-POSED SYSTEM
                  │                                      (Unique solution via PartialPivLU::solve)
                  │
Square SLAE ──────┼─── rank(A) < n && rank(A) == rank(A|b) ─> UNDERDETERMINED SYSTEM
(n x n)           │                                           (Infinite solutions, reject)
                  │
                  └─── rank(A) != rank(A|b) ───────────> INCONSISTENT / CONFLICTING SYSTEM
                                                         (No solution, physical mass/head imbalance, reject)
```

#### Proper Eigen Classes Usage:
* `Eigen::FullPivLU<Eigen::MatrixXd> lu(A);`
  * `lu.isInvertible()` and `lu.rank()` determine system well-posedness with complete pivoting and singular value thresholding.
* In single-pass execution:
  ```cpp
  Eigen::FullPivLU<Eigen::MatrixXd> lu(A);
  if (!lu.isInvertible()) {
      throw std::runtime_error("Singular system: non-invertible matrix");
  }
  Eigen::VectorXd x = lu.solve(b);
  ```

### 2.5. Architectural Bridge to `fixed_solvers`
The project codebase may include a specialized header `fixed_linear_solver.h`, implementing closed-form Cramer's rule solutions for fixed dimensions $N=2$ and $N=3$ using `std::array<std::array<double, N>, N>`.
* The solver architecture supports a cross-verification adapter bridge: for dimensions $N \le 3$, results can be cross-checked between `Eigen::FullPivLU` and `fixed_solvers::solve_linear_system`.

---

## 3. Graph Theory in Hydraulic Network Simulation

### 3.1. Directed Network Graph Structure
A hydraulic circuit is modeled as a connected directed graph $G = (V, E)$, where:
* $V$ — set of vertices (network nodes), $|V| = m$;
* $E$ — set of directed edges (branches: pipes, pumps, valves), $|E| = n$.
* Graph representation leverages `basic_graph_t` from `graph_solvers`.

### 3.2. Incidence Matrices
1. **Full Incidence Matrix $\bar{A}$ ($m \times n$):**
   Defined according to edge orientation:
   $$
   \bar{A}_{j, i} = \begin{cases}
   +1, & \text{if edge } i \text{ leaves node } j; \\
   -1, & \text{if edge } i \text{ enters node } j; \\
   0, & \text{if edge } i \text{ is not incident to node } j.
   \end{cases}
   $$
   * **Linear Dependence Property:** Every column sum is zero ($\sum_{j=1}^m \bar{A}_{j, i} = 0$), so rows are linearly dependent and $\operatorname{rank}(\bar{A}) = m - 1$.
2. **Node Classification by Boundary Condition:**
   * **$Q$-nodes ($m_Q$ count):** Internal nodes with prescribed inflows/outflows $Q_j$ [$\text{m}^3/\text{s}$], where pressures $P_j$ are **unknowns**.
   * **$P$-nodes ($m_P$ count):** Boundary reference nodes with fixed pressures $P_{p, k}$, where mass balance closes through external boundary supplies.
   * Total nodes: $m = m_Q + m_P$. To eliminate hydrostatic singularity, at least one $P$-node is mandatory ($m_P \ge 1$).
3. **Partitioned Incidence Matrices:**
   Matrix $\bar{A}$ partitions row-wise into two blocks:
   $$\bar{A} = \begin{pmatrix} A \\ A_p \end{pmatrix}$$
   * $A \in \mathbb{R}^{m_Q \times n}$ — incidence matrix of internal $Q$-nodes.
   * $A_p \in \mathbb{R}^{m_P \times n}$ — incidence matrix of boundary reference $P$-nodes.

---

## 4. Linear Nodal Boundary Value Flow Distribution Problem

### 4.1. Kirchhoff's Laws for Hydraulic Networks
1. **Kirchhoff's First Law (Mass Conservation at $Q$-nodes):**
   $$A x = Q$$
   where $x \in \mathbb{R}^n$ is branch volumetric flow rates, and $Q \in \mathbb{R}^{m_Q}$ is nodal demand/supply vector (inflow $> 0$, outflow $< 0$).
2. **Kirchhoff's Second Law (Head/Pressure Balance along Branches):**
   Potential difference across branch endpoints equals head drop:
   $$\Delta P_{\text{branch}} = \bar{A}^T \begin{pmatrix} P \\ P_p \end{pmatrix} = A^T P + A_p^T P_p$$
   Branch momentum relation:
   $$A^T P + A_p^T P_p = F(x)$$
   where $F(x) \in \mathbb{R}^n$ is branch closure relationship vector.

### 4.2. Linear Closure Relations
For laminar flow or linearized pipe elements, pressure drop is strictly linear with flow:
$$F_i(x_i) = -r_i x_i + H_i$$
where:
* $r_i > 0$ — hydraulic branch resistance (by Poiseuille: $r_i = \frac{128 \mu L_i}{\pi d_i^4}$);
* $H_i$ — active head (pump differential pressure in branch $i$).

In matrix form:
$$F(x) = -R x + H$$
where $R = \operatorname{diag}(r_1, r_2, \dots, r_n)$ is a positive definite diagonal resistance matrix.

### 4.3. Unified Block KKT Linear Nodal System
Substituting closure relations into Kirchhoff's Second Law:
$$A^T P + A_p^T P_p = -R x + H \quad \iff \quad R x + A^T P = H - A_p^T P_p$$

Combined with Kirchhoff's First Law ($A x = Q$), we obtain the coupled $N \times N$ block system ($N = n + m_Q$):

$$\begin{pmatrix} R & A^T \\ A & 0 \end{pmatrix} \begin{pmatrix} x \\ P \end{pmatrix} = \begin{pmatrix} H - A_p^T P_p \\ Q \end{pmatrix}$$

#### Structure of Block System $\mathcal{A} z = b$:
* Block coefficient matrix $\mathcal{A}$:
  $$\mathcal{A} = \begin{pmatrix} R_{n \times n} & A^T_{n \times m_Q} \\ A_{m_Q \times n} & 0_{m_Q \times m_Q} \end{pmatrix}$$
  *(Symmetric Karush–Kuhn–Tucker / KKT saddle-point matrix)*.
* Unknown vector $z$:
  $$z = \begin{pmatrix} x \\ P \end{pmatrix} \in \mathbb{R}^{n + m_Q}$$
* Right-hand side vector $b$:
  $$b = \begin{pmatrix} H - A_p^T P_p \\ Q \end{pmatrix} \in \mathbb{R}^{n + m_Q}$$

### 4.4. C++ Architecture Pattern for Linear Nodal Solver
```cpp
struct linear_nodal_properties_t {
    basic_graph_t graph;                     ///< Circuit topology
    std::vector<double> resistances;          ///< Resistance vector r_i > 0
    std::vector<double> active_heads;         ///< Active head vector H_i
    std::vector<double> nodal_flows;          ///< Inflow/outflow vector Q_j at Q-nodes
    std::vector<double> boundary_pressures;   ///< Boundary pressure vector P_{p, k} at P-nodes
};

struct linear_nodal_result_t {
    std::vector<double> branch_flows;         ///< Solved branch flow vector x
    std::vector<double> nodal_pressures;      ///< Solved nodal pressure vector P
    double max_residual{0.0};                 ///< Residual ||A*z - b||_inf
};

class linear_nodal_solver_t {
public:
    explicit linear_nodal_solver_t(const linear_nodal_properties_t& props);
    linear_nodal_result_t solve() const;

private:
    void assemble_system(Eigen::MatrixXd& A_block, Eigen::VectorXd& b_vec) const;
};
```

---

## 5. Theory of Hydraulic Circuits (Yuzhanin Formulation)

In turbulent network regimes, branch closure equations are **nonlinear**:
$$F_i(x_i) = -s_i |x_i| x_i + H_i(x_i)$$
where $s_i = \frac{8 \lambda_i L_i \rho}{\pi^2 d_i^5}$ is hydraulic resistance modulus.

Two primary solution methods are applied:

### 5.1. Nodal Pressure Method (NPM)
1. Express branch flows via nodal pressure differences $\Delta P_i = (A^T P + A_p^T P_p)_i$:
   $$x_i = f_i(\Delta P_i) = \operatorname{sign}(\Delta P_i - H_i) \sqrt{\frac{|\Delta P_i - H_i|}{s_i}}$$
2. Substitute $x_i(P)$ into Kirchhoff's First Law to obtain $m_Q$ nonlinear equations in terms of unknown pressures $P$:
   $$r(P) = A \cdot x(P) - Q = 0$$
3. Solve via Newton–Raphson iteration:
   $$P^{(k+1)} = P^{(k)} - J(P^{(k)})^{-1} r(P^{(k)})$$
   with analytical Jacobian:
   $$J = \frac{\partial r}{\partial P} = A \cdot \operatorname{diag}\left( \frac{\partial x_i}{\partial \Delta P_i} \right) \cdot A^T$$

### 5.2. Todini Global Gradient Method (GGM)
The Global Gradient Method linearizes both Kirchhoff laws simultaneously at each iteration.
At step $k$, flow correction vector $\Delta x$ and pressure vector $P^{(k+1)}$ are solved from the block KKT system:
$$\begin{pmatrix} D^{(k)} & A^T \\ A & 0 \end{pmatrix} \begin{pmatrix} \Delta x \\ P^{(k+1)} \end{pmatrix} = \begin{pmatrix} -F(x^{(k)}) + A_p^T P_p \\ Q - A x^{(k)} \end{pmatrix}$$
where $D^{(k)} = \operatorname{diag}\left( \frac{\partial F_i}{\partial x_i} \right)_{x = x^{(k)}}$. For quadratic friction $F_i(x_i) = s_i x_i |x_i|$, diagonal entries are $d_i = 2 s_i |x_i|$.

> [!WARNING] Division-by-Zero Regularization in GGM
> Classical reduction to pressure equations forms matrix $M = A D^{-1} A^T$. When flow in any pipe approaches zero ($x_i \to 0$), diagonal entry $d_i \to 0$, causing $D^{-1}$ to trigger **division-by-zero** (`NaN`/`Inf`).
>
> **Mandatory Implementation Requirements:**
> 1. **Diagonal Regularization:** Diagonal entries of $D$ must be bounded from below:
>    $$d_i = \max\left(2 s_i |x_i|,\, d_{\min}\right), \quad d_{\min} \sim 10^{-6} \dots 10^{-8}$$
>    or via smooth regularization $d_i = 2 s_i \sqrt{x_i^2 + \varepsilon^2}$.
> 2. **Non-Zero Initial Guess:** Never set $x^{(0)} = 0$. Initialize flow rates based on nominal flow velocity $v_0 \approx 1.0 - 1.5\text{ m/s}$ ($x_i^{(0)} = v_0 \cdot \frac{\pi d_i^2}{4}$).

### 5.3. Pendant Edges Formalism
An engineering generalization of hydraulic network theory eliminating node classification:
* **Regular Edges:** Internal pipes, pumps, valves connecting internal nodes.
* **Pendant $P$-Edges:** External branches connected to constant pressure reservoirs/wells.
* **Pendant $Q$-Edges:** External branches connected to prescribed nodal demand/inflow sources.
* **Benefit:** Circuit topology is represented by a single universal incidence matrix, and switching boundary conditions requires no graph restructuring.

---

## 6. Verification Requirements & Automated Tests

1. **SLAE Solution Residual:**
   * Relative normalized residual of block saddle-point system:
     $$\frac{\|\mathcal{A} z - b\|_{\infty}}{\|\mathcal{A}\|_{\infty} \|z\|_{\infty} + \|b\|_{\infty}} < 10^{-12}$$
   * Rank verification and solve are executed in a single pass via `Eigen::FullPivLU<MatrixXd>` (no duplicate factorizations, no `.inverse()`).
2. **Kirchhoff Mass Balance at Nodes:**
   * Absolute residual of volumetric flow conservation: $\|A x - Q\|_{\infty} < 10^{-8}\text{ m}^3/\text{s}$.
3. **Relative Tolerance for Nodal Pressures:**
   * Verification against manual analytical benchmarks uses relative tolerance:
     $$\frac{|P_{\text{calc}} - P_{\text{bench}}|}{P_{\text{bench}}} < 10^{-4} \dots 10^{-5}$$
     (absolute tolerance $10^{-8}$ for pressures of order $10^6\text{ Pa}$ is numerically invalid, as it demands $10^{-14}$ precision near the limit of double precision).
4. **Network Physical Invariants:**
   * Flow vector $x$ directs towards decreasing piezometric head for passive branches.
   * At zero flow ($x_i = 0$), friction head loss is identically zero ($\Delta h_i = 0$).
   * Disconnecting all $P$-nodes causes matrix $\mathcal{A}$ to become singular ($\operatorname{rank} < N$), which the solver must detect and report via diagnostic exception (`std::invalid_argument` / `std::runtime_error`).
