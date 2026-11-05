# Fundamentals of Pipeline Hydraulics & Fluid Dynamics
## Engineering Reference Guide for AI Agents (`hydraulics_core.md`)

> Formulated on the foundation of classical monographs:
> 1. **M. V. Lurie** — *Mathematical Modeling of Pipeline Transportation of Oil, Petroleum Products, and Gas* (2012).
> 2. **M. V. Lurie** — *Problems in Pipeline Transportation of Oil and Petroleum Products* (2003).
> 3. **I. E. Idelchik** — *Handbook of Hydraulic Resistance* (1992).
> 4. **A. D. Altshul** — *Hydraulic Calculations and Flow Resistance* (1982).
> 5. **B. B. Nekrasov** — *Hydraulics and Fluid Machinery* (1989).

---

## 1. Physical Properties of Transported Fluids

### 1.1. Density and Barothermal Dependencies of Liquids
Density $\rho$ [$\text{kg/m}^3$] defines fluid mass per unit volume. For crude oils and petroleum products, density varies with temperature $T$ [$^\circ\text{C}$] and absolute pressure $p$ [$\text{Pa}$]:

$$\rho(p, T) = \rho_{20} \left[ 1 + \xi (20 - T) + \frac{p - p_{\text{atm}}}{K} \right]$$

where:
* $\rho_{20}$ — standard density at $T = 20^\circ\text{C}$ and $p_{\text{atm}} = 101325\text{ Pa}$.
* $\xi$ — volumetric thermal expansion coefficient [$1/^\circ\text{C}$].
* $K = \frac{1}{\beta}$ — bulk modulus of elasticity of the fluid [$\text{Pa}$], $\beta$ — coefficient of compressibility [$1/\text{Pa}$].

#### Typical Values of Density and Expansion Coefficient $\xi$:
| Fluid / Product | $\rho_{20}$ ($\text{kg/m}^3$) | $\xi$ ($1/^\circ\text{C}$) | Bulk Modulus $K$ ($\text{MPa}$) |
|---|---|---|---|
| Gasolines | $700 - 760$ | $0.001225 - 0.001054$ | $\approx 1000$ ($1.0 \times 10^9\text{ Pa}$) |
| Kerosenes | $780 - 830$ | $0.000995 - 0.000882$ | $\approx 1300 - 1500$ |
| Diesel fuels | $830 - 860$ | $0.000882 - 0.000782$ | $\approx 1500$ |
| Commercial crude oils | $840 - 920$ | $0.000831 - 0.000688$ | $\approx 1400 - 1600$ |
| Heavy / high-sulfur crudes | $900 - 960$ | $0.000688 - 0.000600$ | $\approx 1600 - 1800$ |
| Water ($20^\circ\text{C}$) | $998.2$ | $0.000210$ | $\approx 2060 - 2100$ |

---

### 1.2. Fluid Viscosity
Viscosity reflects resistance to shear deformation (Newton's law of viscosity: $\tau = \mu \frac{du}{dy}$).

* **Dynamic viscosity** $\mu$ [$\text{Pa}\cdot\text{s}$] = [$\text{N}\cdot\text{s/m}^2$] = [$\text{kg/(m}\cdot\text{s)}$].
  *(Non-SI unit: $1\text{ Poise (P)} = 0.1\text{ Pa}\cdot\text{s}$, $1\text{ cP} = 10^{-3}\text{ Pa}\cdot\text{s}$)*.
* **Kinematic viscosity** $\nu$ [$\text{m}^2/\text{s}$]:
  $$\nu = \frac{\mu}{\rho}$$
  *(Non-SI unit: $1\text{ Stokes (St)} = 10^{-4}\text{ m}^2/\text{s}$, $1\text{ centistokes (cSt)} = 1\text{ mm}^2/\text{s} = 10^{-6}\text{ m}^2/\text{s}$)*.

#### Viscosity vs. Temperature Correlations:
1. **Walther Formula (ASTM D341)** (standard for petroleum products):
   $$\log_{10} \log_{10} (\nu + c) = A - B \log_{10}(T + 273.15)$$
   *(where $c \approx 0.6 - 0.8$, and $A, B$ are constants for a specific oil grade)*.
2. **Reynolds–Filonov Formula**:
   $$\nu(T) = \nu_{20} \cdot e^{-u (T - 20)}$$
   where $u$ is the temperature sensitivity coefficient ($0.02 - 0.06\ 1/^\circ\text{C}$).

---

### 1.3. Physical Properties of Gases
1. **Equation of State of Real Gas (Clapeyron–Mendeleev with Compressibility Factor):**
   $$p = Z \rho R T \quad \iff \quad \rho = \frac{p}{Z R T}$$
   * $p$ — gas pressure [$\text{Pa}$].
   * $T$ — absolute temperature [$\text{K}$].
   * $R = \frac{R_0}{M_{\text{gas}}} = \frac{8314.46}{M_{\text{gas}}}$ — specific gas constant [$\text{J/(kg}\cdot\text{K)}$].
   * $\Delta = \frac{\rho_{\text{gas}}}{\rho_{\text{air}}} = \frac{M_{\text{gas}}}{28.964}$ — relative gas density relative to air.
   * $R \approx \frac{287.05}{\Delta}$. For natural gas ($\Delta \approx 0.58 - 0.65$): $R \approx 440 - 500\text{ J/(kg}\cdot\text{K)}$.
   * $Z(p, T)$ — gas compressibility factor (dimensionless, $Z \in [0.7, 1.1]$).
     * Papay formula: $Z = 1 - 3.52 p_r e^{-2.26 T_r} + 0.274 p_r^2 e^{-1.87 T_r}$, where $p_r = p / p_{\text{crit}}$, $T_r = T / T_{\text{crit}}$.
2. **Speed of Sound in Gas:**
   $$c = \sqrt{\gamma Z R T}$$
   where $\gamma = \frac{C_p}{C_v}$ is the isentropic expansion factor ($\gamma \approx 1.30 - 1.34$ for natural gas).

---

## 2. Fundamental Equations of 1D Hydrodynamics (Lurie, 2012)

For flow in a circular pipe with internal diameter $d$ and cross-sectional area $S = \frac{\pi d^2}{4}$:

### 2.1. Continuity Equation (Conservation of Mass)
$$\frac{\partial (\rho S)}{\partial t} + \frac{\partial (\rho v S)}{\partial x} = 0$$

* For incompressible liquid in a rigid pipe ($\rho = \text{const}, S = \text{const}$):
  $$\frac{\partial v}{\partial x} = 0 \quad \implies \quad Q(t) = v(t) S = \text{const along } x$$
* For weakly compressible liquid in an elastic pipe:
  $$\frac{\partial p}{\partial t} + \rho c^2 \frac{\partial v}{\partial x} = 0$$
  where $c$ is the wave propagation speed.

### 2.2. Momentum Equation (Equation of Motion)
$$\frac{\partial v}{\partial t} + v \frac{\partial v}{\partial x} + \frac{1}{\rho}\frac{\partial p}{\partial x} + g \sin \alpha + \frac{\lambda |v| v}{2 d} = 0$$

where:
* $\sin \alpha = \frac{\partial z}{\partial x}$ — sine of pipe inclination angle relative to horizontal ($z$ — elevation head).
* $\lambda$ — Darcy friction factor.
* $g = 9.80665\text{ m/s}^2$ — standard acceleration of gravity.

### 2.3. Bernoulli Equation (Steady Flow Along a Streamline)
For two cross-sections 1 and 2:

$$z_1 + \frac{p_1}{\rho g} + \frac{\alpha_1 v_1^2}{2g} = z_2 + \frac{p_2}{\rho g} + \frac{\alpha_2 v_2^2}{2g} + h_{1-2}$$

* $H = z + \frac{p}{\rho g}$ — piezometric head [$\text{m}$].
* $H_0 = z + \frac{p}{\rho g} + \frac{\alpha v^2}{2g}$ — total hydrodynamic head [$\text{m}$].
* $\alpha$ — Coriolis kinetic energy correction coefficient:
  * $\alpha = 2.0$ — for laminar (parabolic) profile;
  * $\alpha \approx 1.05 - 1.1$ — for fully turbulent profile (typically taken as $\alpha \approx 1$ in engineering practice).
* $h_{1-2} = h_f + \sum h_m$ — total head loss [$\text{m}$].

---

## 3. Friction Head Loss in Pipes

### 3.1. Darcy–Weisbach Formula
Head loss along a pipe of length $L$:

$$h_f = \lambda \frac{L}{d} \frac{v^2}{2g}$$

Pressure drop due to friction:
$$\Delta p_f = \rho g h_f = \lambda \frac{L}{d} \frac{\rho v^2}{2} = \frac{8 \lambda L \rho}{\pi^2 d^5} Q^2$$

Hydraulic gradient:
$$i = \frac{h_f}{L} = \frac{\lambda}{d} \frac{v^2}{2g} = \frac{8 \lambda}{\pi^2 g d^5} Q^2$$

---

### 3.2. Reynolds Number and Flow Regimes
$$\text{Re} = \frac{v d}{\nu} = \frac{4 Q}{\pi d \nu} = \frac{4 M}{\pi d \mu}$$

* **Critical Reynolds Number:** $\text{Re}_{\text{crit}} \approx 2320$.

---

### 3.3. Resistance Zones and Friction Factor $\lambda$ Formulas

```
Re < 2320         : Laminar regime (Poiseuille)
2320 <= Re < 4000 : Transition zone
Re >= 4000        : Turbulent regime (subdivided into 3 regions):
   ├── 4000 <= Re < 10 d/k_e           : Hydraulically smooth pipes (Blasius)
   ├── 10 d/k_e <= Re <= 500 d/k_e     : Transition / mixed friction zone (Altshul)
   └── Re > 500 d/k_e                  : Fully rough / quadratic zone (Shifrinson)
```

#### 1. Laminar Regime ($\text{Re} < 2320$) — Poiseuille's Law:
$$\lambda = \frac{64}{\text{Re}}$$
Head loss is strictly linear with flow rate:
$$h_f = \frac{64 \nu}{v d} \frac{L}{d} \frac{v^2}{2g} = \frac{32 \nu L v}{g d^2} = \frac{128 \nu L}{\pi g d^4} Q$$

#### 2. Turbulent Flow in Smooth Pipes ($\text{Re} < 10 \frac{d}{k_e}$) — Blasius Formula:
$$\lambda = \frac{0.3164}{\text{Re}^{0.25}} \quad (\text{for } \text{Re} < 10^5)$$
Konakov formula (for smooth pipes at $\text{Re} > 10^5$):
$$\lambda = \frac{1}{(1.8 \log_{10} \text{Re} - 1.5)^2}$$

#### 3. Mixed Roughness Zone ($10 \frac{d}{k_e} \le \text{Re} \le 500 \frac{d}{k_e}$):
* **Altshul Formula (Primary in pipeline engineering):**
  $$\lambda = 0.11 \left( \frac{k_e}{d} + \frac{68}{\text{Re}} \right)^{0.25}$$
* **Colebrook–White Equation (Implicit international standard):**
  $$\frac{1}{\sqrt{\lambda}} = -2 \log_{10} \left( \frac{k_e}{3.7 d} + \frac{2.51}{\text{Re} \sqrt{\lambda}} \right)$$
* **Swamee–Jain Formula (Explicit approximation of Colebrook):**
  $$\lambda = \frac{0.25}{\left[ \log_{10} \left( \frac{k_e}{3.7 d} + \frac{5.74}{\text{Re}^{0.9}} \right) \right]^2}$$

#### 4. Fully Rough Quadratic Zone ($\text{Re} > 500 \frac{d}{k_e}$):
The friction factor $\lambda$ becomes independent of $\text{Re}$ (self-similarity):
* **Shifrinson Formula:**
  $$\lambda = 0.11 \left( \frac{k_e}{d} \right)^{0.25}$$
* **Nikuradse Formula:**
  $$\frac{1}{\sqrt{\lambda}} = 2 \log_{10}\left(\frac{d}{2 k_e}\right) + 1.74$$

#### Standard Equivalent Roughness Values $k_e$ (Idelchik, Lurie):
* New seamless steel pipes: $k_e = 0.02 - 0.05\text{ mm}$.
* Operating oil pipeline steel pipes after several years: $k_e = 0.10 - 0.15\text{ mm}$.
* Corroded / scaled steel pipes: $k_e = 0.20 - 0.50\text{ mm}$.
* Polyethylene / plastic pipes: $k_e = 0.005 - 0.01\text{ mm}$.

---

## 4. Minor Losses (Local Hydraulic Resistance) (Idelchik, 1992)

Head loss at a local resistance:
$$h_m = \zeta \frac{v^2}{2g} \quad \implies \quad \Delta p_m = \zeta \frac{\rho v^2}{2}$$

where $\zeta$ is the dimensionless local resistance coefficient and $v$ is mean velocity in the referenced section.

### 4.1. Key Formulas and Typical Values of $\zeta$:
1. **Sudden Expansion ($S_1 \to S_2$) (Borda–Carnot Theorem):**
   $$\zeta_{\text{exp}} = \left( 1 - \frac{S_1}{S_2} \right)^2 = \left( 1 - \frac{d_1^2}{d_2^2} \right)^2 \quad (\text{referenced to } v_1)$$
2. **Sudden Contraction ($S_1 \to S_2$):**
   $$\zeta_{\text{contr}} \approx 0.5 \left( 1 - \frac{S_2}{S_1} \right) \quad (\text{referenced to } v_2)$$
3. **Pipe Inlet from Reservoir:**
   * Sharp-edged (flush inlet): $\zeta_{\text{in}} \approx 0.5$.
   * Rounded inlet (bellmouth): $\zeta_{\text{in}} \approx 0.05 - 0.10$.
   * Inward-projecting pipe (re-entrant): $\zeta_{\text{in}} \approx 0.8 - 1.0$.
4. **Pipe Discharge into Large Reservoir:**
   $$\zeta_{\text{out}} = 1.0 \quad (\text{kinetic energy dissipated})$$
5. **Bends and Elbows (turning angle $\theta$):**
   * Smooth bend ($R/d \ge 2 - 3$, $\theta = 90^\circ$): $\zeta \approx 0.15 - 0.25$.
   * Miter bend without rounding ($\theta = 90^\circ$): $\zeta \approx 1.1 - 1.3$.
6. **Valves and Fittings:**
   * Gate valve: fully open $\zeta \approx 0.05 - 0.15$; $3/4$ open: $\zeta \approx 0.3 - 0.5$; $1/2$ open: $\zeta \approx 2.0 - 2.5$; $1/4$ open: $\zeta \approx 15 - 20$.
   * Full-port ball valve: $\zeta \approx 0.03 - 0.05$.
   * Swing check valve: $\zeta \approx 1.5 - 3.0$.

---

## 5. Hydraulic Circuit Laws & Network Equivalencing

### 5.1. Branch Resistance Modulus
Generalized relation of head loss vs. volumetric flow rate:
$$h = s \cdot Q^m$$

where:
* $m = 1$ — laminar flow;
* $m = 1.75$ — smooth turbulent flow (Blasius);
* $m = 2.0$ — quadratic turbulent flow (Altshul / Shifrinson):
  $$s = \frac{8 \lambda L}{\pi^2 g d^5} + \frac{8 \sum \zeta}{\pi^2 g d^4}$$

### 5.2. Series Connection of Pipes
* Flow rate is uniform: $Q_1 = Q_2 = \dots = Q$.
* Head losses sum up:
  $$h_{\Sigma} = \sum_{j} h_j = \left( \sum_{j} s_j \right) Q^2 \quad \implies \quad s_{\text{eq}} = \sum_{j} s_j$$

### 5.3. Parallel Connection of Pipes
* Head loss across common nodes is equal: $h_1 = h_2 = \dots = \Delta H$.
* Flow rates sum up: $Q_{\Sigma} = \sum_{k} Q_k$.
* Under quadratic friction ($h_k = s_k Q_k^2 \implies Q_k = \sqrt{\Delta H / s_k}$):
  $$Q_{\Sigma} = \left( \sum_{k} \frac{1}{\sqrt{s_k}} \right) \sqrt{\Delta H} \quad \implies \quad \frac{1}{\sqrt{s_{\text{eq}}}} = \sum_{k} \frac{1}{\sqrt{s_k}}$$

### 5.4. Looping Calculations
A looping is a parallel pipeline branch of length $l_{\text{loop}}$ constructed to decrease overall hydraulic resistance.
Required relative length of looping $x = l_{\text{loop}} / L$ with diameter $d_{\text{loop}}$ to increase flow capacity from $Q_0$ to $Q$ under fixed available head:

$$x = \frac{l_{\text{loop}}}{L} = \frac{1 - (Q_0 / Q)^2}{1 - \frac{1}{\left( 1 + (d_{\text{loop}} / d)^{2.5} \right)^2}}$$

---

## 6. Pumping Stations and Pipeline Interaction

### 6.1. Pump Head Curve ($Q\text{-}H$)
Quadratic approximation of centrifugal pump head characteristic:
$$H_{\text{pump}}(Q) = a - b Q^2 \quad (\text{or } H_{\text{pump}} = a - b Q - c Q^2)$$

where $a$ is shutoff head (at zero discharge) and $b$ is the slope coefficient.

### 6.2. Affinity Laws for Centrifugal Pumps
Under rotational speed variation from $n_1$ to $n_2$:
$$\frac{Q_2}{Q_1} = \frac{n_2}{n_1}, \qquad \frac{H_2}{H_1} = \left(\frac{n_2}{n_1}\right)^2, \qquad \frac{N_2}{N_1} = \left(\frac{n_2}{n_1}\right)^3$$

Under impeller trimming from diameter $D_1$ to $D_2$:
$$\frac{Q_2}{Q_1} \approx \frac{D_2}{D_1}, \qquad \frac{H_2}{H_1} \approx \left(\frac{D_2}{D_1}\right)^2$$

### 6.3. Power and Efficiency
* Useful hydraulic power: $N_{\text{hyd}} = \rho g Q H$ [$\text{W}$].
* Shaft power:
  $$N_{\text{shaft}} = \frac{\rho g Q H}{\eta_{\text{pump}}}$$
* Electric motor power input:
  $$N_{\text{elec}} = \frac{N_{\text{shaft}}}{\eta_{\text{motor}} \cdot \eta_{\text{trans}}} = \frac{\rho g Q H}{\eta_{\text{pump}} \eta_{\text{motor}} \eta_{\text{trans}}}$$

### 6.4. Multiple Pump Configurations
* **Series Connection (Pressure Boosting in Trunk Pipelines):**
  $$Q = \text{const}, \qquad H_{\Sigma}(Q) = \sum_{k=1}^m H_k(Q)$$
* **Parallel Connection (High Discharge Capacity):**
  $$H = \text{const}, \qquad Q_{\Sigma}(H) = \sum_{k=1}^m Q_k(H)$$

### 6.5. Operating Point Determination
The operating point of a "Pump Station — Pipeline" system satisfies head balance:
$$H_{\text{station}}(Q) = \Delta z_{\text{elev}} + h_f(Q) + \sum h_m(Q) + h_{\text{res}}$$
$$a_{\Sigma} - b_{\Sigma} Q^2 = (z_{\text{outlet}} - z_{\text{inlet}}) + s_f Q^2 + h_{\text{res}}$$

Yielding the analytical solution:
$$Q_{\text{op}} = \sqrt{\frac{a_{\Sigma} - (z_{\text{outlet}} - z_{\text{inlet}}) - h_{\text{res}}}{b_{\Sigma} + s_f}}$$

---

## 7. Transient Flows & Water Hammer

### 7.1. Wave Speed (Joukowsky–Korteweg Formula)
$$c = \sqrt{\frac{K / \rho}{1 + \frac{K}{E} \frac{D}{e} \cdot \mu_{\text{restrain}}}}$$

where:
* $K$ — bulk modulus of elasticity of the liquid [$\text{Pa}$] ($K \approx 1.5 \times 10^9\text{ Pa}$).
* $E$ — Young's modulus of pipe wall material [$\text{Pa}$] (for pipeline steel $E \approx 2.06 \times 10^{11}\text{ Pa}$).
* $D$ — internal pipe diameter [$\text{m}$].
* $e$ — pipe wall thickness [$\text{m}$].
* $\mu_{\text{restrain}}$ — pipe restraint factor ($\approx 1 - \mu_{\text{steel}}^2 \approx 0.91$ for anchored ends, or $\approx 1.0$).

**Typical Sound Speeds:**
* Water in steel pipe: $c \approx 1200 - 1400\text{ m/s}$.
* Crude oil / products in steel pipe: $c \approx 1000 - 1150\text{ m/s}$.
* Natural gas: $c \approx 360 - 420\text{ m/s}$.

### 7.2. Joukowsky Formula for Direct Water Hammer
Direct water hammer occurs when valve closure time $t_{\text{close}}$ is less than the phase time $\tau_{\text{phase}} = \frac{2L}{c}$:

$$\Delta p_{\text{wh}} = \rho c \Delta v \quad \iff \quad \Delta H_{\text{wh}} = \frac{c \Delta v}{g}$$

* For slow closure $t_{\text{close}} > \tau_{\text{phase}}$ (indirect water hammer), maximum pressure rise is approximated by the Joukowsky–Michaud formula:
  $$\Delta p_{\text{ind}} \approx \Delta p_{\text{wh}} \cdot \frac{\tau_{\text{phase}}}{t_{\text{close}}} = \rho c \Delta v \frac{2L}{c t_{\text{close}}} = \frac{2 \rho L \Delta v}{t_{\text{close}}}$$

### 7.3. Method of Characteristics (MOC) for Transients
Hyperbolic PDE system transforms into ODEs along characteristic lines:

$$\frac{dx}{dt} = \pm c$$

* Along $C^+$ ($\frac{dx}{dt} = +c$):
  $$p_i^{t+\Delta t} - p_{i-1}^t + \rho c (v_i^{t+\Delta t} - v_{i-1}^t) + \rho c \left( \frac{\lambda |v| v}{2d} + g \sin \alpha \right)_{i-1} \Delta t = 0$$
* Along $C^-$ ($\frac{dx}{dt} = -c$):
  $$p_i^{t+\Delta t} - p_{i+1}^t - \rho c (v_i^{t+\Delta t} - v_{i+1}^t) - \rho c \left( \frac{\lambda |v| v}{2d} + g \sin \alpha \right)_{i+1} \Delta t = 0$$

Courant–Friedrichs–Lewy (CFL) stability criterion:
$$\Delta t \le \frac{\Delta x}{c + |v|} \approx \frac{\Delta x}{c}$$

---

## 8. Isothermal Steady Gas Flow in Transmission Pipelines

### 8.1. Governing Quadratic Gas Flow Equation
For steady flow in a horizontal segment of length $L$ and diameter $d$:

$$p_{\text{inlet}}^2 - p_{\text{outlet}}^2 = \frac{16 \lambda Z_{\text{mean}} R T_{\text{mean}} L}{\pi^2 d^5} M^2$$

where:
* $M$ — constant mass flow rate [$\text{kg/s}$].
* Standard volumetric flow rate $Q_{\text{std}}$ at standard conditions ($p_{\text{std}} = 101325\text{ Pa}$, $T_{\text{std}} = 293.15\text{ K}$):
  $$Q_{\text{std}} = \frac{M}{\rho_{\text{std}}} = \frac{Z_{\text{std}} R T_{\text{std}}}{p_{\text{std}}} M$$

### 8.2. Pressure Distribution Along Gas Pipeline
$$p(x) = \sqrt{p_{\text{inlet}}^2 - \left( p_{\text{inlet}}^2 - p_{\text{outlet}}^2 \right) \frac{x}{L}}$$

> **Important:** Unlike liquid pipelines where pressure distribution along a horizontal pipe is strictly linear, gas pipeline pressure drops along an **upward convex parabola** (gas velocity accelerates towards the exit as density drops, causing $dp/dx$ to increase).

### 8.3. Mean Pressure Along Segment
$$p_{\text{mean}} = \frac{1}{L} \int_0^L p(x) dx = \frac{2}{3} \left( p_{\text{inlet}} + \frac{p_{\text{outlet}}^2}{p_{\text{inlet}} + p_{\text{outlet}}} \right)$$

---

## 9. Non-Newtonian Fluids (Rheology of High-Pour / Waxy Crudes)

For waxy, high-viscosity crude oils below pour point or cloud point ($T < T_{\text{cloud}}$), the Newtonian linear assumption breaks down.

### 9.1. Shvedov–Bingham Plastic Model
$$
\begin{cases}
\frac{du}{dy} = 0, & \text{for } |\tau| \le \tau_0 \quad (\text{solid core / plug flow region}) \\
\tau = \tau_0 \operatorname{sign}\left(\frac{du}{dy}\right) + \mu_p \frac{du}{dy}, & \text{for } |\tau| > \tau_0
\end{cases}
$$

* $\tau_0$ — yield stress [$\text{Pa}$].
* $\mu_p$ — plastic viscosity [$\text{Pa}\cdot\text{s}$].

#### Buckingham Equation for Laminar Discharge:
$$Q = \frac{\pi d^4 \Delta p}{128 \mu_p L} \left[ 1 - \frac{4}{3}\left(\frac{\tau_0}{\tau_w}\right) + \frac{1}{3}\left(\frac{\tau_0}{\tau_w}\right)^4 \right]$$
where $\tau_w = \frac{\Delta p \cdot d}{4 L}$ is wall shear stress.

### 9.2. Hedström and Saint-Venant (Ilyushin) Numbers
Dimensionless similarity criteria for non-Newtonian flow:
$$\text{He} = \frac{\tau_0 d^2 \rho}{\mu_p^2}, \qquad \text{Il} = \frac{\tau_0 d}{\mu_p v}$$

---

## 10. Summary Table of Physical Constants

| Parameter | Symbol | Standard SI Value | Note |
|---|---|---|---|
| Standard gravitational acceleration | $g$ | $9.80665\text{ m/s}^2$ | Standard engineering: $9.81\text{ m/s}^2$ |
| Standard atmospheric pressure | $p_{\text{atm}}$ | $101325\text{ Pa} = 0.101325\text{ MPa}$ | $760\text{ mmHg}$ |
| Universal gas constant | $R_0$ | $8314.46\text{ J/(kmol}\cdot\text{K)}$ | |
| Air molar mass | $M_{\text{air}}$ | $28.964\text{ kg/kmol}$ | |
| Young's modulus of pipeline steel | $E$ | $2.06 \times 10^{11}\text{ Pa}$ ($206\text{ GPa}$) | |
| Poisson's ratio for steel | $\mu_{\text{steel}}$ | $0.28 - 0.30$ | |
| Critical Reynolds number | $\text{Re}_{\text{crit}}$ | $2320$ | Circular cylindrical pipe |
| Velocity limit for oil / petroleum products | $v_{\text{max}}$ | $0.8 - 2.5\text{ m/s}$ | Constrained by erosion and energy cost |
| Velocity limit for natural gas | $v_{\text{gas}}$ | $8 - 20\text{ m/s}$ | Above $20\text{ m/s}$ causes noise and acoustic erosion |

---

## 11. Guidance for Computational Skill

1. **Physical Model Validation:**
   Before running hydraulic solver, verify $\text{Re}$:
   * If $\text{Re} < 2320$ — use strictly linear Poiseuille model.
   * If $\text{Re} \ge 4000$ — evaluate $\lambda$ via Altshul / Swamee–Jain accounting for relative roughness $\frac{k_e}{d}$.
2. **Nonlinear Network Solvers:**
   * Nonlinear hydraulic circuit head losses $\Delta H = s Q |Q|$ require Newton–Raphson or Todini Global Gradient Method (GGA) with safeguards.
3. **Transient Analysis:**
   * When valve closure or pump trips occur, always verify direct water hammer conditions via $\tau_{\text{phase}} = \frac{2L}{c}$.
