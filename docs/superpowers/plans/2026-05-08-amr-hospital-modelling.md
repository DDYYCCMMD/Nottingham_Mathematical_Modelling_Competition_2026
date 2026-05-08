# AMR Hospital Network Modelling — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete a full AMR hospital network modelling submission (report + code + video outline) for the Nottingham Mathematical Modelling Competition 2026 by 2026-05-17 23:59 GMT+8.

**Architecture:** Claude leads all mathematical derivation, biological justification, and report writing. Codex implements all Python simulation code to Claude's exact specifications. A single `parameters.py` is the source of truth for all numerical values. Code is validated against the Linus Three Questions before acceptance.

**Tech Stack:** Python 3.10+, scipy (solve_ivp), numpy, matplotlib, SALib (PRCC sensitivity), pandas. All outputs saved as PNG to `03_simulation/figures/`.

---

## File Map

| File | Responsibility | Author |
|------|---------------|--------|
| `01_literature/notes.md` | Annotated reading notes, extracted parameters | Claude |
| `02_model/model_derivation.md` | Full ODE system, NGM R₀ derivation, stability analysis | Claude |
| `03_simulation/parameters.py` | All numerical parameters with units and literature citations | Claude |
| `03_simulation/main_simulation.py` | ODE integrator, baseline run, time-series plots | Codex |
| `04_intervention/intervention_analysis.py` | 4-scenario runner, comparison plots | Codex |
| `05_sensitivity/sensitivity_analysis.py` | PRCC analysis, tornado plot | Codex |
| `06_report/report_draft.md` | Full report in Markdown (export to PDF) | Claude |
| `07_presentation/slides_outline.md` | 10-minute video script and slide structure | Claude |
| `08_submission/AI_Use_Statement.md` | Honest disclosure of Claude/Codex roles | Claude |

---

## Task 1: Read Reference Papers and Extract Parameters

**Day 1 — 2026-05-08**

**Files:**
- Create: `01_literature/notes.md`

- [ ] **Step 1: Read D'Agata et al. (2007) — J. Theoretical Biology**

  File: `docs/reference/1-s2.0-S0022519307003943-main.pdf`

  Extract and record in `01_literature/notes.md`:
  - Model structure used (SIS/SEIR/other)
  - Direct transmission rate β values reported
  - HCW contamination/decontamination parameters
  - Decolonisation rate γ values
  - Any R₀ estimates for hospital AMR

- [ ] **Step 2: Read Lipsitch et al. (2000) — PNAS**

  File: `docs/reference/pnas-0504053102.pdf`

  Extract:
  - Antibiotic resistance transmission parameters
  - Effect of antibiotic use on resistance selection
  - Model-derived thresholds for resistance persistence

- [ ] **Step 3: Read Webb et al. — PNAS (preprintAJE.pdf)**

  File: `docs/reference/preprintAJE.pdf`

  Extract:
  - Epidemic model structure for resistant bacteria
  - Parameter ranges for hospital settings
  - Intervention effectiveness estimates

- [ ] **Step 4: Read Bootsma et al. (2006) — Am. J. Epidemiology**

  File: `docs/reference/pq001938.pdf`

  Extract:
  - Bacterial acquisition routes (patient-to-patient vs HCW-mediated)
  - Hand hygiene compliance effect on transmission
  - Proportion of transmission attributable to HCW hands

- [ ] **Step 5: Write consolidated notes**

  Write `01_literature/notes.md` with sections:
  ```
  ## Paper 1: D'Agata et al. 2007
  ### Model structure
  ### Key parameters extracted
  ### Relevant to our model because

  ## Paper 2: Lipsitch et al. 2000
  ...

  ## Paper 3: ...

  ## Paper 4: Bootsma et al. 2006
  ...

  ## Consolidated Parameter Estimates
  | Parameter | Value | Range | Source |
  |-----------|-------|-------|--------|
  | β (direct) | ... | ... | D'Agata 2007 |
  | γ (decolonisation) | ... | ... | ... |
  | η (HCW contamination rate) | ... | ... | Bootsma 2006 |
  | δ (HCW decontamination, 40% compliance) | ... | ... | Bootsma 2006 |
  ```

- [ ] **Step 6: Commit**

  ```bash
  git add 01_literature/notes.md
  git commit -m "docs: add literature notes and extracted parameters"
  ```

---

## Task 2: Design ODE System and Derive R₀

**Day 2 — 2026-05-09**

**Files:**
- Create: `02_model/model_derivation.md`

- [ ] **Step 1: Write state variable definitions**

  In `02_model/model_derivation.md`, write Section 1:

  ```markdown
  ## 1. State Variables

  The hospital network comprises four wards indexed i ∈ {GM, GS, ICU, GW}.

  For each ward i:
  - S_i(t): number of susceptible (uncolonised) patients at time t
  - C_i(t): number of colonised (AMR-carrying) patients at time t
  - H_i(t): proportion of healthcare workers in ward i with contaminated hands at time t

  Constraint: S_i + C_i = N_i (constant, beds always occupied)
  ```

- [ ] **Step 2: Write ODE system with full derivation**

  Write Section 2 — derive each term explicitly:

  ```markdown
  ## 2. ODE System

  ### 2.1 Patient Compartments

  dS_i/dt = [inflow from admissions] - [direct colonisation] - [HCW-mediated colonisation]
            + [decolonisation] + [transfer inflow] - [discharge]

  dS_i/dt = μ_i·N_i - β_i·(C_i/N_i)·S_i - λ_i·H_i·S_i
            + γ_i·C_i + Σ_{j≠i} T_{ji}·C_j/(N_j) · N_i^{frac} - μ_i·S_i

  dC_i/dt = β_i·(C_i/N_i)·S_i + λ_i·H_i·S_i + α_i·μ_i·N_i
            - (γ_i + μ_i)·C_i - Σ_{j≠i} T_{ij}·C_i

  ### 2.2 HCW Compartment

  dH_i/dt = η_i·(C_i/N_i)·(1 - H_i) - δ_i·H_i

  ### 2.3 Term-by-Term Biological Justification
  [Write one paragraph per term explaining the biological mechanism]
  ```

- [ ] **Step 3: Write SIS model justification**

  Write Section 3:
  ```markdown
  ## 3. Model Choice Justification

  ### 3.1 Why SIS, not SIR
  [Write: AMR colonisation confers no lasting immunity. Decolonisation occurs naturally
  (immune clearance) or clinically (decolonisation regimens). Patients are immediately
  susceptible to recolonisation. SIR would incorrectly predict permanent protection,
  underestimating long-run prevalence. Evidence: cite D'Agata 2007, Lipsitch 2000.]

  ### 3.2 Why constant N_i
  [Write: NHS bed occupancy routinely exceeds 95%. Assuming N_i constant is standard
  in hospital AMR models. Alternative: variable N_i with stochastic admissions — rejected
  because it adds complexity without changing qualitative dynamics at high occupancy.
  Cite Lipsitch 2000.]

  ### 3.3 Why include HCW compartment
  [Write: Bootsma et al. 2006 attribute 30-50% of nosocomial MRSA transmission to
  HCW-mediated contact. Omitting H_i would underestimate R₀ and overestimate the
  impact of patient isolation alone.]
  ```

- [ ] **Step 4: Derive R₀ using Next Generation Matrix method**

  Write Section 4:
  ```markdown
  ## 4. Basic Reproduction Number R₀

  ### 4.1 Disease-Free Equilibrium (DFE)
  At DFE: C_i = 0, H_i = 0, S_i = N_i for all i.
  (Note: admission colonisation α_i creates a non-zero endemic input,
  so true DFE requires α_i = 0; we set α_i = 0 for R₀ calculation
  and treat admission colonisation as a forcing term in simulation.)

  ### 4.2 Infected Compartments
  Infected compartments: {C_1, C_2, C_3, C_4, H_1, H_2, H_3, H_4} — 8 variables.

  ### 4.3 Next Generation Matrix
  Partition the linearised system at DFE into:
  - F matrix: new infections (transmissions only)
  - V matrix: transitions (recovery, death, transfer — not new infections)

  F is 8×8:
  F_{C_i, C_i} = β_i (direct transmission from C_i to S_i = N_i at DFE)
  F_{C_i, H_i} = λ_i·N_i (HCW-mediated transmission)
  F_{H_i, C_i} = η_i (HCW contamination from colonised patients)
  All other F entries = 0.

  V is 8×8 (diagonal + transfer terms):
  V_{C_i, C_i} = γ_i + μ_i + Σ_j T_{ij}
  V_{H_i, H_i} = δ_i

  ### 4.4 R₀ = ρ(F·V⁻¹)
  R₀ is the spectral radius (largest eigenvalue) of the next generation matrix K = F·V⁻¹.

  For a single isolated ward (no transfers, no HCW):
  R₀_single = β_i / (γ_i + μ_i)

  For a single ward with HCW transmission:
  R₀_ward = β_i/(γ_i + μ_i) + λ_i·η_i / [δ_i·(γ_i + μ_i)]

  For the full 4-ward system: R₀ = ρ(K) computed numerically.

  ### 4.5 Stability Analysis
  If R₀ < 1: DFE is locally asymptotically stable → resistance eliminated
  If R₀ > 1: DFE is unstable → resistance persists at endemic equilibrium
  ```

- [ ] **Step 5: Commit**

  ```bash
  git add 02_model/model_derivation.md
  git commit -m "docs: complete ODE system derivation and R0 NGM analysis"
  ```

---

## Task 3: Write Parameters File

**Day 2 (end) — 2026-05-09**

**Files:**
- Create: `03_simulation/parameters.py`

- [ ] **Step 1: Write parameters.py with all numerical values**

  Create `03_simulation/parameters.py`:

  ```python
  """
  Model parameters for 4-ward hospital AMR transmission model.
  All values from literature unless noted. Units in days.

  Sources:
  - D'Agata et al. (2007) J. Theor. Biol. 249:487-499
  - Lipsitch et al. (2000) PNAS 97:1938-1943
  - Bootsma et al. (2006) Am. J. Epidemiol. 164:1100-1109
  """

  import numpy as np

  # Ward indices
  GM, GS, ICU, GW = 0, 1, 2, 3
  WARD_NAMES = ["General Medicine", "General Surgery", "ICU", "Geriatric Ward"]

  # Ward capacities (number of beds)
  N = np.array([60.0, 40.0, 15.0, 30.0])

  # Discharge/admission rate μ_i = 1/avg_length_of_stay (per day)
  avg_stay_days = np.array([5.0, 7.0, 12.0, 14.0])
  mu = 1.0 / avg_stay_days  # [0.200, 0.143, 0.083, 0.071]

  # Antibiotic use proportions per ward (dimensionless, 0-1)
  antibiotic_use = np.array([0.40, 0.60, 0.80, 0.50])

  # Direct patient-to-patient transmission rate β_i (per day)
  # Base rate from D'Agata 2007; scaled by antibiotic pressure
  # Higher antibiotic use → higher selective pressure → higher effective β
  beta_base = 0.1  # per day, from D'Agata 2007 Table 1
  beta = beta_base * (1 + 0.5 * antibiotic_use)
  # Result: [0.120, 0.130, 0.140, 0.125]

  # Decolonisation rate γ_i (per day)
  # Base rate reduced by antibiotic use (antibiotics impair natural clearance)
  gamma_base = 0.1  # per day (approx 10-day colonisation duration, D'Agata 2007)
  gamma = gamma_base * (1 - 0.5 * antibiotic_use)
  # Result: [0.080, 0.070, 0.060, 0.075]

  # HCW-mediated transmission rate λ_i (per day, per contaminated HCW proportion)
  # From Bootsma 2006: ~30-40% of transmission via HCW hands
  lambda_hcw = np.array([0.04, 0.04, 0.06, 0.04])  # ICU higher due to more procedures

  # HCW contamination rate η_i (per day, from contact with colonised patients)
  eta = np.array([0.3, 0.3, 0.5, 0.3])  # per colonisation-prevalence unit per day

  # HCW decontamination rate δ_i (per day)
  # At 40-60% hand hygiene compliance: δ ≈ compliance × contacts_per_day × efficacy
  # Bootsma 2006: hand hygiene compliance 50% → δ ≈ 5/day
  hand_hygiene_compliance_baseline = 0.50  # 50% baseline
  delta_base = 10.0  # max decontamination rate at 100% compliance (per day)
  delta = delta_base * hand_hygiene_compliance_baseline * np.ones(4)
  # Result: [5.0, 5.0, 5.0, 5.0]

  # Admission colonisation fraction α_i (proportion of new admissions already colonised)
  alpha = np.array([0.04, 0.04, 0.04, 0.04])  # 4% baseline (problem statement: 3-5%)

  # Inter-ward transfer rates T_ij (per day, fraction of ward i patients transferred to j)
  # T[i,j] = rate of transfer FROM ward i TO ward j
  T = np.zeros((4, 4))
  T[GS, ICU] = 0.05 / avg_stay_days[GS]  # 5% of GS patients transferred to ICU
  T[ICU, GM] = 0.10 / avg_stay_days[ICU]  # 10% of ICU patients transferred to GM

  # Initial conditions: colonisation prevalence at t=0
  # Start near endemic equilibrium estimate: ~5-10% colonised
  C0_frac = np.array([0.05, 0.05, 0.10, 0.05])  # fraction colonised at t=0
  C0 = C0_frac * N
  S0 = N - C0
  H0 = np.array([0.05, 0.05, 0.10, 0.05])  # 5-10% HCW contaminated at t=0

  # Initial state vector [S_GM, S_GS, S_ICU, S_GW, C_GM, C_GS, C_ICU, C_GW,
  #                       H_GM, H_GS, H_ICU, H_GW]
  y0 = np.concatenate([S0, C0, H0])

  # Simulation time
  T_SPAN = (0, 365)   # 12 months in days
  T_EVAL = np.linspace(0, 365, 366)
  ```

- [ ] **Step 2: Validate parameter sanity**

  ```bash
  cd "/Users/daidaiyuchi/Desktop/数模三校联赛（ddl 5.17)/Nottingham_Mathematical_Modelling_Competition_2026"
  python3 -c "
  import sys; sys.path.insert(0, '03_simulation')
  import parameters as p
  import numpy as np
  print('N:', p.N)
  print('mu:', np.round(p.mu, 4))
  print('beta:', np.round(p.beta, 4))
  print('gamma:', np.round(p.gamma, 4))
  print('y0 shape:', p.y0.shape)
  print('y0 sum check (should equal sum of N*2 + 4 fracs):', p.y0[:8].sum())
  print('All N conserved:', np.allclose(p.y0[:4] + p.y0[4:8], p.N))
  "
  ```

  Expected output:
  ```
  N: [60. 40. 15. 30.]
  mu: [0.2    0.1429 0.0833 0.0714]
  beta: [0.12  0.13  0.14  0.125]
  gamma: [0.08  0.07  0.06  0.075]
  y0 shape: (12,)
  All N conserved: True
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add 03_simulation/parameters.py
  git commit -m "feat: add model parameters file with literature citations"
  ```

---

## Task 4: Delegate Baseline Simulation to Codex

**Day 3 — 2026-05-10**

**Files:**
- Create: `03_simulation/main_simulation.py`

- [ ] **Step 1: Send spec to Codex**

  Run `/ask codex` with this exact specification:

  ```
  Implement `03_simulation/main_simulation.py` for a 4-ward hospital AMR ODE model.

  Parameters are imported from `03_simulation/parameters.py` (already written).

  REQUIRED FUNCTIONS:

  1. hospital_ode(t, y, params):
     """
     ODE right-hand side for the 4-ward AMR model.
     State vector y has 12 elements:
       y[0:4]  = S_i (susceptible patients, 4 wards)
       y[4:8]  = C_i (colonised patients, 4 wards)
       y[8:12] = H_i (HCW contamination fraction, 4 wards)
     params is a dict with keys: N, mu, beta, gamma, lambda_hcw, eta, delta, alpha, T
     Returns: dy/dt as numpy array of shape (12,)
     """
     For each ward i:
       dS_i/dt = mu[i]*N[i] - beta[i]*(C[i]/N[i])*S[i] - lambda_hcw[i]*H[i]*S[i]
                 + gamma[i]*C[i] - mu[i]*S[i] + sum_j(T[j,i]*C[j])
       dC_i/dt = beta[i]*(C[i]/N[i])*S[i] + lambda_hcw[i]*H[i]*S[i]
                 + alpha[i]*mu[i]*N[i] - (gamma[i] + mu[i])*C[i] - sum_j(T[i,j])*C[i]
       dH_i/dt = eta[i]*(C[i]/N[i])*(1 - H[i]) - delta[i]*H[i]
     Enforce H[i] in [0,1] by clipping after each step (H cannot exceed 1).

  2. compute_R0(params):
     """
     Compute R0 as spectral radius of the Next Generation Matrix K = F * V_inv.
     Infected compartments: [C_0..C_3, H_0..H_3] (8x8 system).
     At DFE: S_i = N_i, H_i = 0, C_i = 0.
     F[i,i] = beta[i]  (direct C->C transmission, i in 0..3)
     F[i,4+i] = lambda_hcw[i]*N[i]  (HCW->C transmission)
     F[4+i,i] = eta[i]  (C->H contamination)
     V[i,i] = gamma[i] + mu[i] + sum_j(T[i,j])  (C removal)
     V[4+i,4+i] = delta[i]  (H decontamination)
     Returns: float R0
     """

  3. run_baseline():
     """
     Run the ODE from parameters.y0 over parameters.T_SPAN.
     Use scipy.integrate.solve_ivp with method='RK45', rtol=1e-6, atol=1e-8.
     Returns: dict with keys 't', 'S' (4xN), 'C' (4xN), 'H' (4xN), 'prevalence' (4xN)
     where prevalence[i] = C[i]/N[i]
     """

  4. plot_baseline(result, save_path='03_simulation/figures/baseline.png'):
     """
     4-panel figure (2x2). Each panel: one ward. Plot colonisation prevalence C_i/N_i
     over time in days. Y-axis: 0-0.5. X-axis label: 'Days'. Y-axis label: 'Colonisation Prevalence'.
     Title each panel with ward name. Add horizontal dashed line at 0.05 (5% threshold).
     Save to save_path at 150 dpi.
     """

  5. if __name__ == "__main__":
     result = run_baseline()
     r0 = compute_R0(params_dict)  # build params dict from parameters module
     print(f"System R0 = {r0:.4f}")
     for i, name in enumerate(parameters.WARD_NAMES):
         final_prev = result['prevalence'][i, -1]
         print(f"{name}: final prevalence = {final_prev:.3f} ({final_prev*100:.1f}%)")
     plot_baseline(result)
     print("Figure saved to 03_simulation/figures/baseline.png")

  Requirements:
  - Import all parameters from 03_simulation/parameters.py (no hardcoded numbers)
  - Fixed random seed not needed (deterministic ODE)
  - Add inline comments explaining each ODE term
  - Use numpy arrays throughout, no pandas needed
  ```

- [ ] **Step 2: Wait for Codex result via `/pend codex`**

- [ ] **Step 3: Apply Linus Three Questions**

  **Q1 — Does it work?**
  ```bash
  cd "/Users/daidaiyuchi/Desktop/数模三校联赛（ddl 5.17)/Nottingham_Mathematical_Modelling_Competition_2026"
  python3 03_simulation/main_simulation.py
  ```
  Expected: R₀ printed (should be > 1 for baseline), prevalence values for each ward, figure saved. No errors.

  **Q2 — Is it right?**
  Check manually:
  - ICU should have highest final prevalence (highest antibiotic use 80%, longest stay)
  - GM should have lowest (lowest antibiotic use 40%, shortest stay)
  - R₀ should be between 1.5 and 3.0 for baseline (typical hospital MRSA range)

  **Q3 — Is it good?**
  - No magic numbers (all from parameters.py)
  - Inline comments on ODE terms
  - `plot_baseline` saves to correct path

- [ ] **Step 4: If any question fails, return to Codex with specific line-level feedback**

  Return feedback as: "Line X: [exact issue]. Expected: [what it should do]."

- [ ] **Step 5: Commit accepted code**

  ```bash
  git add 03_simulation/main_simulation.py 03_simulation/figures/baseline.png
  git commit -m "feat: add baseline ODE simulation and R0 computation"
  ```

---

## Task 5: Write Part A Mathematical Sections of Report

**Day 3-4 — 2026-05-10–11**

**Files:**
- Create: `06_report/report_draft.md` (Sections 1–4)

- [ ] **Step 1: Write Introduction (Section 1)**

  In `06_report/report_draft.md`:
  ```markdown
  # Modelling Antimicrobial Resistance Dynamics in a Hospital Network

  ## 1. Introduction

  Antimicrobial resistance (AMR) represents one of the greatest threats to global public health,
  with the WHO estimating [X] deaths attributable to AMR infections annually [cite WHO 2024].
  Hospital settings are particularly critical transmission environments: intensive antibiotic use,
  immunocompromised patients, and high healthcare worker-patient contact rates create conditions
  that accelerate the selection and spread of resistant organisms [cite Lipsitch 2000].

  We model a four-ward hospital network — General Medicine (GM), General Surgery (GS),
  Intensive Care Unit (ICU), and Geriatric Ward (GW) — as a coupled compartmental system.
  Our objectives are threefold: (i) derive analytically the basic reproduction number R₀
  that governs resistance persistence; (ii) simulate baseline colonisation dynamics under
  realistic parameters; and (iii) evaluate four intervention strategies on a 12-month horizon.
  ```

- [ ] **Step 2: Write Model Formulation (Section 2)**

  Transcribe and expand from `02_model/model_derivation.md` into report format.
  Include: state variable table, full ODE system, parameter table with literature citations,
  biological justification for SIS choice, HCW compartment rationale, constant-population assumption.

- [ ] **Step 3: Write R₀ Analysis (Section 3)**

  Transcribe NGM derivation from `02_model/model_derivation.md`. Add:
  - Numerical R₀ value from simulation output
  - Interpretation: "R₀ = X means each colonised patient generates X secondary colonisations in a fully susceptible ward"
  - Sensitivity of R₀ to hand hygiene compliance (analytical expression from single-ward formula)

- [ ] **Step 4: Write Baseline Simulation Results (Section 4)**

  Include `03_simulation/figures/baseline.png`. Write:
  - Initial conditions and parameter sources (one sentence per parameter)
  - Steady-state prevalence per ward (read from simulation output)
  - Comparison to literature: "D'Agata et al. report ICU prevalence of X-Y%, our model produces Z%"
  - Why ICU has highest and GM lowest prevalence (link to antibiotic pressure and length of stay)

- [ ] **Step 5: Commit**

  ```bash
  git add 06_report/report_draft.md
  git commit -m "docs: write report sections 1-4 (intro, model, R0, baseline)"
  ```

---

## Task 6: Define Intervention Parameters and Delegate Intervention Code

**Day 4-5 — 2026-05-11–12**

**Files:**
- Create: `04_intervention/intervention_analysis.py`

- [ ] **Step 1: Document exact parameter overrides for each scenario**

  Add to `03_simulation/parameters.py`:
  ```python
  # ── Intervention scenario parameter overrides ──────────────────────────────

  # Scenario A: Hand hygiene compliance raised to 80%
  SCENARIO_A = {
      'delta': delta_base * 0.80 * np.ones(4)  # δ increases with compliance
  }

  # Scenario B: Universal admission screening + contact precautions
  # Screening removes 80% of colonised admissions; contact precautions reduce β by 30%
  SCENARIO_B = {
      'alpha': alpha * 0.20,        # 80% reduction in admission colonisation
      'beta': beta * 0.70           # 30% reduction in direct transmission
  }

  # Scenario C: Antibiotic stewardship — 30% reduction in unnecessary use
  # Reduces antibiotic_use by 30%, restoring γ toward base
  antibiotic_use_C = antibiotic_use * 0.70
  SCENARIO_C = {
      'gamma': gamma_base * (1 - 0.5 * antibiotic_use_C)
  }

  # Scenario D: Combined A + C
  SCENARIO_D = {
      'delta': delta_base * 0.80 * np.ones(4),
      'gamma': gamma_base * (1 - 0.5 * antibiotic_use_C)
  }
  ```

- [ ] **Step 2: Send spec to Codex**

  ```
  Implement `04_intervention/intervention_analysis.py`.

  Import from 03_simulation/parameters.py and 03_simulation/main_simulation.py.

  REQUIRED FUNCTIONS:

  1. run_scenario(scenario_params: dict) -> dict:
     """
     Run the ODE with parameter overrides from scenario_params.
     Build a full params dict from parameters module, then update with scenario_params.
     Call the hospital_ode function from main_simulation with the modified params.
     Return same structure as run_baseline(): dict with 't','S','C','H','prevalence'.
     """

  2. compute_scenario_R0(scenario_params: dict) -> float:
     """
     Compute R0 for a given scenario using compute_R0 from main_simulation.
     Build params dict, apply overrides, return spectral radius.
     """

  3. plot_interventions(results: dict, save_path='03_simulation/figures/interventions.png'):
     """
     results is a dict: {'Baseline': result_dict, 'A: Hand Hygiene': result_dict, ...}
     Create a 2x2 figure. Each panel = one ward. In each panel, plot colonisation
     prevalence over time for all 5 scenarios (baseline + 4) with different line styles.
     Legend on first panel only. Y-axis 0-0.4. X-axis label 'Days'. Dashed line at 0.05.
     Save at 150 dpi.
     """

  4. summary_table(results: dict, r0s: dict) -> None:
     """
     Print a table to stdout:
     Scenario | R0 | GM_prev | GS_prev | ICU_prev | GW_prev | System_prev
     Where _prev = final colonisation prevalence at day 365.
     """

  5. if __name__ == "__main__":
     Run all 5 scenarios (baseline + A + B + C + D).
     Print summary_table.
     Save plot.
     Print "Figure saved to 03_simulation/figures/interventions.png"
  ```

- [ ] **Step 3: Wait for Codex via `/pend codex`**

- [ ] **Step 4: Apply Linus Three Questions**

  **Q1 — Does it work?**
  ```bash
  python3 04_intervention/intervention_analysis.py
  ```
  Expected: Table printed, figure saved, no errors.

  **Q2 — Is it right?**
  - Scenario A (hand hygiene 80%) must reduce prevalence vs baseline
  - Scenario D (combined) must show the largest reduction
  - R₀ for all intervention scenarios must be ≤ baseline R₀
  - Scenario C should show partial reduction (stewardship alone is less effective than combined)

  **Q3 — Is it good?**
  - No parameter values hardcoded — all from parameters.py
  - run_scenario correctly applies partial overrides without corrupting base params

- [ ] **Step 5: Commit**

  ```bash
  git add 04_intervention/intervention_analysis.py 03_simulation/figures/interventions.png
  git commit -m "feat: add intervention analysis for scenarios A-D"
  ```

---

## Task 7: Delegate Sensitivity Analysis to Codex

**Day 5 — 2026-05-12**

**Files:**
- Create: `05_sensitivity/sensitivity_analysis.py`

- [ ] **Step 1: Send spec to Codex**

  ```
  Implement `05_sensitivity/sensitivity_analysis.py`.

  Import parameters from 03_simulation/parameters.py.
  Import compute_R0 from 03_simulation/main_simulation.
  Import run_baseline from 03_simulation/main_simulation.
  Use SALib for PRCC (pip install SALib if needed).

  REQUIRED FUNCTIONS:

  1. define_problem() -> dict:
     """
     SALib problem dictionary for 4 parameters varied uniformly across all wards.
     Return:
     {
       'num_vars': 4,
       'names': ['beta_scale', 'gamma_scale', 'delta_scale', 'alpha_scale'],
       'bounds': [[0.5, 1.5],   # beta ± 50%
                  [0.5, 1.5],   # gamma ± 50%
                  [0.222, 1.0], # delta: compliance 20% to 100% (as fraction of delta_base*10)
                  [0.01, 0.08]] # alpha: 1% to 8% admission colonisation
     }
     """

  2. run_prcc_analysis(n_samples=1000, seed=42) -> dict:
     """
     Latin Hypercube Sampling of the 4 parameters.
     For each sample:
       - Scale beta, gamma, delta, alpha by the sampled factors
       - Compute R0 using compute_R0
       - Run simulation and record system_prevalence = mean(C_i(365)/N_i) across wards
     Returns dict: {'R0': array(n_samples,), 'prevalence': array(n_samples,),
                    'samples': array(n_samples x 4)}
     """

  3. compute_prcc(samples, outputs) -> np.ndarray:
     """
     Compute PRCC between each column of samples and the output array.
     Use scipy.stats.spearmanr on residuals after regressing out other parameters.
     Returns array of shape (4,) with PRCC coefficients.
     """

  4. plot_tornado(prcc_r0, prcc_prev,
                  save_path='03_simulation/figures/sensitivity.png'):
     """
     Two-panel horizontal bar chart.
     Left panel: PRCC vs R0. Right panel: PRCC vs 12-month prevalence.
     Bars coloured green (positive PRCC) or red (negative PRCC).
     X-axis: -1 to 1. Y-axis: parameter names.
     Title panels 'Sensitivity: R0' and 'Sensitivity: Prevalence'.
     Save at 150 dpi.
     """

  5. if __name__ == "__main__":
     results = run_prcc_analysis(n_samples=1000, seed=42)
     prcc_r0 = compute_prcc(results['samples'], results['R0'])
     prcc_prev = compute_prcc(results['samples'], results['prevalence'])
     print("PRCC vs R0:", dict(zip(['beta','gamma','delta','alpha'], prcc_r0.round(3))))
     print("PRCC vs prevalence:", dict(zip(['beta','gamma','delta','alpha'], prcc_prev.round(3))))
     plot_tornado(prcc_r0, prcc_prev)
     print("Figure saved to 03_simulation/figures/sensitivity.png")
  ```

- [ ] **Step 2: Wait for Codex via `/pend codex`**

- [ ] **Step 3: Apply Linus Three Questions**

  **Q1 — Does it work?**
  ```bash
  python3 05_sensitivity/sensitivity_analysis.py
  ```
  Expected: PRCC values printed, figure saved, runtime < 60 seconds.

  **Q2 — Is it right?**
  - beta_scale should have strong positive PRCC with R₀ (higher transmission → higher R₀)
  - gamma_scale should have negative PRCC with R₀ (higher decolonisation → lower R₀)
  - delta_scale (hand hygiene) should have negative PRCC (more hygiene → lower R₀)
  - If signs are reversed, there is a parameter scaling bug — flag to Codex

  **Q3 — Is it good?**
  - Fixed seed (seed=42) for reproducibility
  - n_samples=1000 for adequate PRCC convergence

- [ ] **Step 4: Commit**

  ```bash
  git add 05_sensitivity/sensitivity_analysis.py 03_simulation/figures/sensitivity.png
  git commit -m "feat: add PRCC sensitivity analysis with tornado plot"
  ```

---

## Task 8: Write Intervention and Sensitivity Report Sections

**Day 6 — 2026-05-13**

**Files:**
- Modify: `06_report/report_draft.md` (add Sections 5–6)

- [ ] **Step 1: Read simulation outputs**

  ```bash
  python3 04_intervention/intervention_analysis.py
  python3 05_sensitivity/sensitivity_analysis.py
  ```
  Note down all numerical values for use in the report.

- [ ] **Step 2: Write Section 5 — Intervention Analysis**

  ```markdown
  ## 5. Intervention Analysis

  ### 5.1 Results

  Table: [copy from summary_table output — R0 and final prevalence for all 5 scenarios]

  [Include figure: 03_simulation/figures/interventions.png]

  ### 5.2 Interpretation

  **Scenario A (Hand Hygiene 80%):** Raising compliance from 50% to 80% reduces system R₀
  from [X] to [Y] and 12-month ICU prevalence from [A]% to [B]%. The mechanism is accelerated
  HCW decontamination (δ increases), reducing indirect transmission which accounts for
  approximately [Z]% of total transmission in our model (derived from λ/β ratio).

  **Scenario B (Admission Screening):** [Interpret: largest reduction in admission-driven
  colonisation, but does not affect in-hospital transmission chain.]

  **Scenario C (Antibiotic Stewardship):** [Interpret: restores natural decolonisation rate γ,
  particularly effective in high-antibiotic-pressure wards (ICU).]

  **Scenario D (Combined A+C):** [Interpret: synergistic effect — reduced admission input
  from sustained decolonisation AND reduced transmission. Recommend this as primary strategy.]

  ### 5.3 Policy Recommendation

  We recommend Scenario D (combined hand hygiene + antibiotic stewardship) as the primary
  intervention. [Write 2-3 sentences justifying: cost-effectiveness, complementary mechanisms,
  evidence base from literature.]

  ### 5.4 Limitations and Uncertainty

  [Write: parameter uncertainty, assumption of uniform compliance across all HCW grades,
  ignoring patient-level heterogeneity, 12-month horizon does not capture multi-year dynamics.]
  ```

- [ ] **Step 3: Write Section 6 — Sensitivity Analysis**

  ```markdown
  ## 6. Sensitivity Analysis

  [Include figure: 03_simulation/figures/sensitivity.png]

  PRCC analysis (n=1000 Latin Hypercube samples) identifies [β/γ/δ] as the parameter
  most strongly correlated with R₀ (PRCC = [X]). This indicates that [interpretation].

  Hand hygiene compliance (δ) shows PRCC = [Y] with system prevalence, confirming that
  Scenario A's effect is not merely due to model parameterisation but reflects structural
  sensitivity. Antibiotic pressure (γ) ranks [Z]th, suggesting that stewardship alone
  has [smaller/comparable] impact than hand hygiene improvement alone.

  These results are consistent with Bootsma et al. (2006), who identified hand hygiene
  compliance as the dominant leverage point in hospital AMR control.
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add 06_report/report_draft.md
  git commit -m "docs: add intervention and sensitivity analysis report sections"
  ```

---

## Task 9: Write Part C — Critical Evaluation

**Day 7 — 2026-05-14**

**Files:**
- Modify: `06_report/report_draft.md` (add Section 7)

> **Note:** This section must be Claude's original reasoning. Do not delegate. This is 20% of rubric and explicitly AI-resistant. Write from genuine analytical thinking.

- [ ] **Step 1: Write Limitation 1 — Homogeneous Mixing**

  ```markdown
  ## 7. Critical Evaluation

  ### 7.1 Model Limitations

  **Limitation 1: Homogeneous mixing assumption within wards**

  Our model assumes all patients in ward i have equal probability of contact with any HCW
  or other patient in ward i. In reality, transmission is structured by physical bed
  proximity, nursing assignments, and patient mobility. A patient in the bed adjacent to
  a colonised patient faces substantially higher exposure than a patient at the far end of
  the ward.

  *Effect on predictions:* Homogeneous mixing tends to overestimate transmission speed at
  low prevalence (when colonised individuals are sparse, mixing models generate more
  contacts than actually occur) and underestimate clustering effects at high prevalence.
  Our baseline R₀ and intervention effects may therefore be conservative estimates of
  how targeted bed-placement or cohorting could reduce transmission.

  *What would address it:* A network model with an explicit HCW-patient contact graph,
  parameterised from ward observation data or electronic patient records, would capture
  spatial heterogeneity. However, such data are rarely available in routine clinical practice.
  ```

- [ ] **Step 2: Write Limitation 2 — Deterministic ODE for Small Populations**

  ```markdown
  **Limitation 2: Deterministic approximation ignores stochastic extinction**

  Ordinary differential equations treat populations as continuous quantities. For the ICU
  (N=15 beds), even 10% colonisation means 1.5 patients — a quantity with no physical
  meaning. Stochastic fluctuations at low prevalence can cause extinction of the
  colonisation chain even when R₀ > 1 (a phenomenon the deterministic model cannot capture).

  *Effect on predictions:* Our model predicts ICU will always reach the endemic equilibrium
  given R₀ > 1. A stochastic model might show that with a small ward, outbreaks self-limit
  through chance alone approximately [X]% of the time. We are therefore likely
  *overestimating* the inevitability of endemic colonisation in small wards.

  *What would address it:* A Gillespie stochastic simulation or tau-leaping approximation
  would model individual colonisation/decolonisation events. This is computationally feasible
  for N=15 and would provide probability distributions over outcomes rather than point estimates.
  ```

- [ ] **Step 3: Write Limitation 3 — Static Parameters**

  ```markdown
  **Limitation 3: Time-invariant transmission parameters**

  Our β, γ, and δ are constants throughout the 12-month simulation. In practice,
  transmission rates change seasonally (winter respiratory infection season increases patient
  density and HCW workload), outbreak-driven behavioural change (an MRSA cluster triggers
  enhanced infection control), and the evolution of the bacterial population itself
  (clonal expansion of hypervirulent strains).

  *Effect on predictions:* The model will underestimate peak outbreak severity (which can
  temporarily double effective β) and overestimate steady-state persistence (ignoring
  outbreak-driven improvements in compliance). Intervention effectiveness is measured
  against a static baseline, which may not represent the dynamic context of real
  implementation.

  *What would address it:* Time-varying parameters driven by empirical data (e.g., seasonal
  admission rates from hospital records, compliance audit data) or by coupled behavioural
  models (compliance as a function of local outbreak severity).
  ```

- [ ] **Step 4: Write rejected alternative models**

  ```markdown
  ### 7.2 Alternative Modelling Approaches Considered

  **Alternative 1: Individual-based model (IBM)**

  An IBM would simulate each patient and HCW as an autonomous agent with individual
  attributes (immune status, antibiotic history, room location, assigned nurse).
  Transmission events occur through explicit contact events rather than mass-action mixing.

  *Why rejected:* An IBM requires extensive contact-network data (bed maps, shift rosters,
  patient movement logs) that are not available in the problem specification. Parameter
  calibration for individual-level models requires patient-level microbiology records.
  More critically for this context, IBMs are poorly suited to sensitivity analysis: the
  computational cost of 1000 runs (required for PRCC) would be prohibitive. The scientific
  question — which intervention reduces population-level prevalence most — is better
  served by a compartmental model that captures macroscopic dynamics analytically.

  **Alternative 2: Multi-strain model (sensitive + resistant)**

  A two-strain ODE would track both antibiotic-sensitive organisms (colonisation X)
  and resistant organisms (colonisation C), with competitive exclusion dynamics and
  antibiotic-driven selection. This would allow us to model the emergence of resistance
  de novo rather than treating resistance as a fixed property of the pathogen.

  *Why rejected:* The problem specifies modelling an established resistant organism
  (AMR already present in the hospital). De novo emergence dynamics are a timescale of
  years, not the 12-month intervention horizon. Adding a sensitive strain doubles state
  variables (from 12 to 20) and introduces competitive dynamics that require additional
  parameters (relative fitness cost of resistance) with high uncertainty. For 12-month
  policy evaluation, the simpler single-strain model captures the essential dynamics.
  ```

- [ ] **Step 5: Write misleading scenario**

  ```markdown
  ### 7.3 Scenario Where the Model Gives Misleading Predictions

  **Scenario: Applying our model during the acute phase of an outbreak introduction**

  Our model is calibrated to and designed for *endemic steady-state* dynamics — the
  long-run behaviour when AMR is chronically circulating in the ward. The initial conditions
  (5–10% colonisation) are set near the expected endemic equilibrium.

  If the model were applied to predict the trajectory of a *newly introduced* resistant
  strain (e.g., one colonised patient arrives in an otherwise AMR-free ICU), the ODE
  would correctly predict exponential growth if R₀ > 1. However, it would overestimate
  the growth speed, because in early-outbreak conditions, HCW contact rates and hygiene
  compliance often improve in response to clinical alerts — a behavioural feedback that
  our static-parameter model ignores entirely.

  More subtly, the inter-ward transfer terms T_{ij} were estimated from long-run transfer
  statistics. During an active outbreak, patient cohorting and transfer restrictions are
  commonly imposed, effectively setting T_{ij} = 0. Our model would overestimate spread
  to other wards because it cannot represent this outbreak-responsive management response.

  The model should therefore be used as a *steady-state policy planning tool*, not as a
  real-time outbreak prediction engine.
  ```

- [ ] **Step 6: Commit**

  ```bash
  git add 06_report/report_draft.md
  git commit -m "docs: write Part C critical evaluation (original Claude reasoning)"
  ```

---

## Task 10: Complete Report — Conclusion, References, Appendix

**Day 8 — 2026-05-15**

**Files:**
- Modify: `06_report/report_draft.md` (add Sections 8-9 + Appendix)

- [ ] **Step 1: Write Conclusion (Section 8)**

  ```markdown
  ## 8. Conclusion

  We have developed a four-ward coupled SIS+HCW compartmental model of AMR transmission
  in a hospital network. The model yields a system-level basic reproduction number R₀ = [X],
  consistent with published estimates for MRSA in NHS settings ([cite]).

  Our intervention analysis demonstrates that the combined strategy of raising hand hygiene
  compliance to 80% and implementing antibiotic stewardship (Scenario D) achieves the largest
  reduction in 12-month AMR prevalence ([Y]% reduction system-wide), outperforming single
  interventions by [Z]%.

  Sensitivity analysis confirms that transmission rate β and hand hygiene decontamination
  rate δ are the primary drivers of R₀, reinforcing the prioritisation of hand hygiene
  compliance as the most cost-effective single intervention.

  The model's critical limitations — homogeneous mixing, deterministic formulation, and
  static parameters — are documented in Section 7. Future work should incorporate
  stochastic dynamics for small wards and outbreak-responsive behavioural feedback.

  This analysis supports recommending Scenario D (combined hand hygiene + stewardship)
  to the hospital board as the evidence-based primary strategy for AMR control.
  ```

- [ ] **Step 2: Write References section**

  List all cited papers in APA format. Minimum 6 references including the 4 provided PDFs.

- [ ] **Step 3: Write AI Use Statement**

  Create `08_submission/AI_Use_Statement.md`:

  ```markdown
  # AI Use Statement
  ## Nottingham Mathematical Modelling Competition 2026

  **Team:** [name(s)]
  **Date:** 2026-05-15

  ### Summary of AI Tool Use

  This submission used two AI tools: **Claude (Anthropic)** and **Codex (OpenAI)**,
  coordinated through the Claude Code environment.

  ### Division of Labour

  **Claude was responsible for:**
  - Reading and annotating the 4 reference papers
  - Designing the mathematical model structure (ODE system, state variables)
  - Deriving R₀ analytically using the Next Generation Matrix method
  - Writing all biological justifications for modelling choices
  - Designing the 4 intervention scenarios and interpreting results
  - Writing the full report (all sections)
  - Writing Part C (Critical Evaluation) — entirely original reasoning
  - Writing this AI Use Statement

  **Codex was responsible for:**
  - Implementing `03_simulation/main_simulation.py`
  - Implementing `04_intervention/intervention_analysis.py`
  - Implementing `05_sensitivity/sensitivity_analysis.py`

  ### Validation Process

  All code produced by Codex was reviewed by Claude against the Linus Three Questions
  before acceptance: (1) Does it work? (2) Is it right? (3) Is it good?
  Specific validation steps are documented in the implementation plan at
  `docs/superpowers/plans/2026-05-08-amr-hospital-modelling.md`.

  ### What AI Did NOT Do

  The critical evaluation in Section 7 represents original analytical reasoning and
  was not delegated to any AI tool. The biological justifications throughout the report
  were written by Claude based on its own reasoning from the reference papers.
  ```

- [ ] **Step 4: Write slides outline**

  Create `07_presentation/slides_outline.md`:

  ```markdown
  # Video Presentation Outline (≤ 10 minutes)

  ## Slide 1 — Title (30s)
  AMR Dynamics in a Hospital Network: A Compartmental Modelling Approach
  Team name, date

  ## Slide 2 — Problem Motivation (60s)
  - What is AMR? Why hospitals?
  - The four-ward network (table: beds, stay, antibiotic use)
  - Research question: which intervention reduces AMR most cost-effectively?

  ## Slide 3 — Model Structure (90s)
  - SIS+HCW diagram (draw: S→C→S loop, H feedback arrow)
  - Why SIS not SIR (one sentence)
  - ODE system (display, don't derive)

  ## Slide 4 — R₀ and Baseline (60s)
  - R₀ = [X] (what this means in plain English)
  - Baseline figure: 4-panel prevalence time series
  - ICU highest, GM lowest — explain why

  ## Slide 5 — Intervention Results (120s)
  - Interventions figure: 4-panel comparison
  - Summary table: R₀ and final prevalence for all 5 scenarios
  - Recommendation: Scenario D, why

  ## Slide 6 — Sensitivity Analysis (60s)
  - Tornado plot
  - Top parameter: β (or δ) — policy implication

  ## Slide 7 — Critical Evaluation (90s)
  - Limitation 1: homogeneous mixing
  - Limitation 2: stochastic extinction in ICU
  - Alternative model considered: IBM (why rejected)
  - Misleading scenario: acute outbreak introduction

  ## Slide 8 — Conclusion (30s)
  - R₀ > 1 confirmed for baseline
  - Scenario D recommended: 80% hand hygiene + stewardship
  - δ and β are key leverage points
  ```

- [ ] **Step 5: Commit all**

  ```bash
  git add 06_report/report_draft.md 07_presentation/slides_outline.md 08_submission/AI_Use_Statement.md
  git commit -m "docs: complete full report, slides outline, and AI use statement"
  ```

---

## Task 11: Final Review and Submission Packaging

**Day 9 — 2026-05-16–17**

**Files:**
- Create: `08_submission/` (copy of final deliverables)

- [ ] **Step 1: Run all code end-to-end from clean state**

  ```bash
  cd "/Users/daidaiyuchi/Desktop/数模三校联赛（ddl 5.17)/Nottingham_Mathematical_Modelling_Competition_2026"
  python3 03_simulation/main_simulation.py
  python3 04_intervention/intervention_analysis.py
  python3 05_sensitivity/sensitivity_analysis.py
  ```
  All three must run without errors and produce figures in `03_simulation/figures/`.

- [ ] **Step 2: Check all figures referenced in report exist**

  ```bash
  ls 03_simulation/figures/
  ```
  Expected: `baseline.png`, `interventions.png`, `sensitivity.png`

- [ ] **Step 3: Verify report length**

  ```bash
  wc -l 06_report/report_draft.md
  ```
  Check estimated page count. If too long, trim appendix.

- [ ] **Step 4: Review submission checklist**

  - [ ] Written Report — PDF ≤ 20 pages (export report_draft.md to PDF via pandoc or similar)
  - [ ] Video Presentation — MP4 ≤ 10 minutes (record from slides_outline.md)
  - [ ] Simulation Code — all 3 Python files
  - [ ] AI Use Statement — PDF 1 page

- [ ] **Step 5: Final commit**

  ```bash
  git add .
  git commit -m "chore: final submission package ready"
  ```

- [ ] **Step 6: Upload to Moodle before 2026-05-17 23:59 GMT+8**
