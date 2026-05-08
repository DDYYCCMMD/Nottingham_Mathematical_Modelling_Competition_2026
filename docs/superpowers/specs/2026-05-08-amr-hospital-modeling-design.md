# AMR Hospital Network Modelling — Design Specification

**Date:** 2026-05-08  
**Deadline:** 2026-05-17, 23:59 GMT+8  
**Lead:** Claude (architect, analyst, report author)  
**Coder:** Codex (all Python simulation code)

---

## 1. Project Scope

Model antimicrobial resistance (AMR) transmission dynamics in a 4-ward hospital network for the Nottingham Mathematical Modelling Competition 2026. Deliver:

- Written report (PDF, ≤ 20 pages)
- Simulation code (Python)
- Video presentation (MP4, ≤ 10 minutes)
- AI Use Statement (1 page)

All work led by Claude. Python code delegated to Codex via `/ask codex`. No external teammates.

---

## 2. 9-Day Timeline

| Day | Date | Deliverable |
|-----|------|-------------|
| 1 | 2026-05-08 | Read 4 reference PDFs; extract parameters and model precedents |
| 2 | 2026-05-09 | Complete ODE system + R₀ NGM derivation → `02_model/model_derivation.md` |
| 3 | 2026-05-10 | `/ask codex` baseline simulation; write Part A mathematical sections |
| 4 | 2026-05-11 | Validate simulation output; design intervention parameters; write biological justifications |
| 5 | 2026-05-12 | `/ask codex` intervention analysis + sensitivity analysis |
| 6 | 2026-05-13 | Validate code; interpret all figures; write Part B intervention recommendation |
| 7 | 2026-05-14 | Write Part C (critical evaluation) — Claude original reasoning only |
| 8 | 2026-05-15 | Integrate full report draft; write AI Use Statement; write slides outline |
| 9 | 2026-05-16–17 | Proofread; package submission; upload to Moodle |

---

## 3. Mathematical Model

### 3.1 Ward Configuration

Four wards: General Medicine (GM, 60 beds), General Surgery (GS, 40 beds), ICU (15 beds), Geriatric Ward (GW, 30 beds).

### 3.2 State Variables (per ward i)

- **S_i(t)** — susceptible (uncolonised) patients
- **C_i(t)** — colonised (AMR-carrying) patients
- **H_i(t)** — contaminated healthcare workers (proportion, indirect transmission vector)

Constant population: N_i = S_i + C_i (beds always occupied).

### 3.3 ODE System

For each ward i ∈ {GM, GS, ICU, GW}:

```
dS_i/dt = μ_i·N_i − β_i·(C_i/N_i)·S_i − λ_i·H_i·S_i − μ_i·S_i + γ_i·C_i + Σ_j T_ji·C_j
dC_i/dt = β_i·(C_i/N_i)·S_i + λ_i·H_i·S_i + α_i·μ_i·N_i − (γ_i + μ_i)·C_i − Σ_j T_ij·C_i
dH_i/dt = η_i·(C_i/N_i)·(1 − H_i) − δ_i·H_i
```

### 3.4 Parameter Definitions

| Symbol | Meaning | Source |
|--------|---------|--------|
| μ_i | discharge/admission rate = 1/avg_stay | Problem statement |
| β_i | direct patient-to-patient transmission rate | Literature (D'Agata 2007) |
| λ_i | HCW-mediated transmission rate | Literature |
| γ_i | decolonisation rate (modulated by antibiotic pressure) | Literature |
| α_i | admission colonisation fraction (3–5%) | Problem statement |
| δ_i | HCW hand hygiene decontamination rate | Parameterised from compliance 40–60% |
| η_i | rate HCW becomes contaminated from colonised patients | Literature |
| T_ij | transfer rate from ward i to ward j | Problem statement (ICU→GM 10%, GS→ICU 5%) |

### 3.5 Biological Justifications

- **SIS not SIR:** AMR colonisation confers no lasting immunity; patients can be decolonised and recolonised. SIR would incorrectly model permanent protection.
- **Constant N_i:** NHS bed occupancy routinely >95%; assuming full beds is standard in hospital AMR models (Lipsitch 2000).
- **HCW compartment:** Healthcare workers are the primary transmission vector in nosocomial AMR spread; omitting them would underestimate R₀ by 30–50% (Bootsma 2006).
- **Antibiotic pressure on γ_i:** Higher antibiotic use selects for resistance, effectively reducing the decolonisation rate. This is parameterised per ward using the antibiotic use percentages (GM 40%, GS 60%, ICU 80%, GW 50%).
- **Inter-ward transfers:** Creates epidemic coupling — an endemic ICU can seed decolonised patients in GM, sustaining system-level persistence even when individual ward R₀ < 1.

### 3.6 R₀ Derivation

Use the Next Generation Matrix (NGM) method on the linearised system at the disease-free equilibrium. The NGM K is a 12×12 matrix (4 wards × 3 compartments). R₀ = ρ(K) (spectral radius = dominant eigenvalue).

For a single isolated ward: R₀_i = β_i·N_i / (γ_i + μ_i) + λ_i·η_i·N_i / [δ_i·(γ_i + μ_i)]

---

## 4. Intervention Scenarios (Part B)

Simulated over 12-month horizon. Baseline run as control.

| Scenario | Parameter Change | Mechanism |
|----------|-----------------|-----------|
| A. Hand hygiene → 80% | δ_i increases (compliance 40%→80%) | Faster HCW decontamination, breaks indirect transmission chain |
| B. Admission screening + contact precautions | α_i reduced 80%; β_i reduced 30% | Reduces community input and direct transmission |
| C. Antibiotic stewardship (−30%) | γ_i increases (decolonisation rate restored) | Restores host clearance capacity |
| D. Combined A + C | δ_i + γ_i both improved | Multi-target intervention |

**Evaluation metrics:** 12-month endpoint colonisation prevalence per ward; system R₀; estimated colonised-patient-days averted.

---

## 5. Sensitivity Analysis

Method: PRCC (Partial Rank Correlation Coefficient) for global sensitivity; tornado plot for local one-at-a-time analysis.

| Parameter | Range | Rationale |
|-----------|-------|-----------|
| β_i | ±50% baseline | Primary direct transmission driver |
| δ_i | compliance 20%–90% | Hand hygiene policy lever |
| γ_i | ±50% baseline | Antibiotic pressure effect |
| α_i | 1%–8% | Admission screening impact |

Output: PRCC bar chart ranked by absolute correlation with R₀ and 12-month prevalence.

---

## 6. Report Structure

| Section | Content | Pages (est.) |
|---------|---------|--------------|
| 1. Introduction | AMR burden, hospital network problem, modelling objectives | 1 |
| 2. Model Formulation | ODE system, state variables, parameter table, biological justifications | 3–4 |
| 3. R₀ Analysis | NGM derivation, stability analysis, persistence threshold | 2 |
| 4. Baseline Simulation | Parameter sources, initial conditions, steady-state results | 2 |
| 5. Intervention Analysis | 4-scenario comparison figures, policy recommendation | 3 |
| 6. Sensitivity Analysis | Tornado/PRCC figures, key parameter identification | 2 |
| 7. Critical Evaluation (Part C) | 3 limitations, 2 rejected alternatives, 1 misleading scenario | 3 |
| 8. Conclusion | Policy advice, limitations, future directions | 1 |
| References | APA format | 1 |
| Appendix | Full parameter table, key code snippets | 1–2 |

**Total: ≤ 20 pages**

### Part C (Critical Evaluation) — Claude-only, no delegation

1. **Limitation 1:** Homogeneous mixing within wards (real transmission is network-structured by bed proximity and HCW rosters)
2. **Limitation 2:** Deterministic ODE ignores stochastic extinction at low prevalence (especially relevant for ICU with N=15)
3. **Limitation 3:** Static parameters — β and γ assumed constant, ignoring outbreak-driven behavioural change
4. **Rejected alternative 1:** Individual-based model (IBM) — higher biological fidelity but computationally intractable for policy sensitivity analysis
5. **Rejected alternative 2:** Network model with explicit HCW contact graph — more realistic but requires patient-level contact tracing data not available
6. **Misleading scenario:** Model will overestimate intervention effectiveness during an active outbreak phase (non-equilibrium dynamics), because the ODE assumes quasi-steady demographic flows

---

## 7. Codex Delegation Contracts

Three code tasks, each with a defined interface:

### Task 1 — `03_simulation/main_simulation.py`
- Function: `hospital_ode(t, y, params)` → dy/dt vector
- Function: `run_baseline(params, t_span, t_eval)` → DataFrame of S_i, C_i, H_i over time
- Output: Figure — time series of colonisation prevalence per ward

### Task 2 — `04_intervention/intervention_analysis.py`
- Function: `run_scenario(scenario_name, params_override, baseline_result)` → DataFrame
- Function: `plot_interventions(results_dict)` → 4-panel comparison figure

### Task 3 — `05_sensitivity/sensitivity_analysis.py`
- Function: `prcc_analysis(param_ranges, n_samples=1000)` → PRCC coefficients
- Function: `tornado_plot(prcc_results)` → ranked bar chart

All code: fixed random seeds, no hard-coded paths, parameters imported from `03_simulation/parameters.py`.

---

## 8. Linus Three Questions (acceptance gate for all Codex output)

Before accepting any code:
1. **Does it work?** Correct numerical output, edge cases handled
2. **Is it right?** Mathematical logic faithful to ODE system above
3. **Is it good?** Readable, reproducible, no magic numbers

All three must pass. Otherwise return to Codex with line-level feedback.

---

## 9. Other Deliverables

- `08_submission/AI_Use_Statement.md` — honest account of Claude/Codex roles and validation steps
- `07_presentation/slides_outline.md` — 10-minute video script (intro → model → results → interventions → critical eval → conclusion)
- `03_simulation/parameters.py` — single source of truth for all numerical parameters with literature citations
