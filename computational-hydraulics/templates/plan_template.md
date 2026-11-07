# Implementation and Verification Plan: [Task Name]

> **Document:** `docs/<n>_<topic>_plan.md`  
> **Based on:**  
> * Requirements: `docs/<n>_<topic>.md`  
> * Architecture: `docs/<n>_<topic>_architecture.md`  
> * Quality Protocol: `AGENTS.md`  

---

## Implementation Checklist

- [ ] **Stage 1: Domain Types and Interfaces Setup**
  - [ ] Inspect existing codebase for reusable types; do not re-implement existing components.
  - [ ] Create header file `include/[task_name]_types.h` with new `*_properties_t` and `*_result_t` structures.
  - [ ] Create header file `include/[task_name]_solver.h` with method declarations and concise Doxygen contracts (using single-line `///` per line, no `/** ... */`).
  - [ ] Verify adherence to code style (`snake_case`, `_t` suffix, explicit SI parameter names).

- [ ] **Stage 2: Solver Implementation Logic**
  - [ ] Create `src/[task_name]_solver.cpp`.
  - [ ] Implement fail-fast constructor validation (dimension matching, $r_i > 0$, reference $P$-node presence).
  - [ ] Implement private `assemble_system` method: build incidence matrices $A, A_p$, diagonal resistance $R$, block KKT matrix $\mathcal{A}$, and vector $b$.
  - [ ] Implement `solve` method via single-pass `Eigen::FullPivLU`: check `lu.isInvertible()` $\implies$ solve `lu.solve(b)` $\implies$ compute normalized residual $\Vert \mathcal{A}z - b \Vert_\infty$ and mass balance $\Vert Ax - Q \Vert_\infty$.
  - [ ] Verify complete absence of `matrix.inverse() * b`.

- [ ] **Stage 3: Quantitative Verification (GoogleTest Accuracy Benchmarks)**
  - [ ] Create `tests/test_[task_name]_numerical.cpp`.
  - [ ] Implement benchmark test case on simple analytical verification model ($2 \times 2$ or $3 \times 3$).
  - [ ] Implement benchmark test case for complete laboratory variant:
    - Compare branch flow rates $x$ against benchmark (`EXPECT_NEAR(x[i], x_ref[i], 1e-8)`);
    - Compare nodal pressures $P$ against benchmark using relative tolerance (`EXPECT_LT(rel_err, 1e-4)`);
    - Check normalized linear system residual (`EXPECT_LT(norm_residual, 1e-12)`);
    - Check Kirchhoff nodal mass balance (`EXPECT_LT(result.max_kirchhoff_residual, 1e-8)`).

- [ ] **Stage 4: Qualitative Verification (Physical Invariants and Edge Cases)**
  - [ ] Create `tests/test_[task_name]_invariants.cpp`.
  - [ ] Network singularity test: removing the single $P$-node must cause solver to throw `std::runtime_error`.
  - [ ] Input contract assertion: non-positive resistance $r_i \le 0$ throws `std::invalid_argument`.
  - [ ] Flow direction invariant: on passive branches, flow travels strictly along the pressure drop gradient.

- [ ] **Stage 5: Build and CTest Execution**
  - [ ] Update `CMakeLists.txt` to register new source files and test targets.
  - [ ] Execute clean out-of-source build (`cmake -B build && cmake --build build`).
  - [ ] Run `ctest --test-dir build --output-on-failure` and ensure 100% test pass rate.

- [ ] **Stage 6: Review and Manual Git Commit (Performed by Developer)**
  - [ ] Developer runs `git status` and `git diff` to review all code changes.
  - [ ] Developer crafts a clean commit: `git commit -m "feat(solver): implement linear nodal flow distribution solver with gtest verification"`.

- [ ] **Stage 7: Pre-Defense Exam Drill (/mock-defense)**
  - [ ] Trigger `/mock-defense` to undergo an interactive exam rehearsal with the agent.
