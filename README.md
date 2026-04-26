# Nottingham Mathematical Modelling Competition 2026

**Topic:** Modelling Antimicrobial Resistance (AMR) Dynamics in a Hospital Network
**Deadline:** 17 May 2026, 23:59 GMT+8
**Organiser:** Elio Espejo, School of Mathematical Sciences, UNNC (z2019136@nottingham.edu.cn)

---

## Project Structure

```
Nottingham_Mathematical_Modelling_Competition_2026/
│
├── README.md                        ← This file: overview, guidance, and checklist
│
├── 01_literature/                   ← Reading notes and annotated references
│   └── notes.md
│
├── 02_model/                        ← Mathematical derivation and analysis
│   └── model_derivation.md
│
├── 03_simulation/                   ← Numerical simulation code
│   ├── main_simulation.py
│   ├── parameters.py
│   └── figures/                     ← Output plots
│
├── 04_intervention/                 ← Intervention analysis code (Part B)
│   └── intervention_analysis.py
│
├── 05_sensitivity/                  ← Sensitivity analysis code
│   └── sensitivity_analysis.py
│
├── 06_report/                       ← Report drafts (final submission: PDF ≤ 20 pages)
│   └── report_draft.md
│
├── 07_presentation/                 ← Video presentation materials (PPT / script)
│   └── slides_outline.md
│
└── 08_submission/                   ← Final packaged deliverables
    └── AI_Use_Statement.md
```

---

## Problem Summary

You are a team of mathematical modellers advising a hospital network on controlling
antimicrobial resistance (AMR). The hospital has four wards:

| Ward | Beds | Avg Stay (days) | Antibiotic Use |
|------|------|-----------------|----------------|
| General Medicine (GM) | 60 | 5 | 40% |
| General Surgery (GS) | 40 | 7 | 60% |
| Intensive Care Unit (ICU) | 15 | 12 | 80% |
| Geriatric Ward (GW) | 30 | 14 | 50% |

Key system features: patient transfers between wards, healthcare worker (HCW) movement,
differential antibiotic pressure, admission colonisation rate of 3–5%, and hand hygiene
compliance of 40–60%.

---

## Task Structure

### Part A — Model Development (25% + 25% of rubric)
1. Formulate a compartmental model for at least two wards. Define state variables,
   parameters, and transmission pathways. Justify every choice biologically.
2. Derive a basic reproduction number R₀ (or equivalent threshold). Discuss persistence
   vs. extinction of resistance.
3. Implement computationally (Python/MATLAB/R). Simulate with literature-based
   parameters. Perform sensitivity analysis on at least 3 key parameters.

### Part B — Intervention Analysis (feeds into Analytical Depth: 20%)
Evaluate four scenarios over a 12-month horizon:
- **A.** Hand hygiene compliance raised to 80%
- **B.** Universal admission screening (all wards) + contact precautions
- **C.** Antibiotic stewardship — 30% reduction in unnecessary use
- **D.** Combined strategy (at least two of the above)

Provide an evidence-based recommendation to the hospital board. Discuss limitations
and uncertainty.

### Part C — Critical Evaluation (20% of rubric — heavily AI-resistant)
1. Identify the **3 most significant limitations** of your model. For each: explain its
   effect on predictions and what additional data/approaches would address it.
2. Describe **2 alternative modelling approaches** you considered but rejected, and
   justify your choice.
3. Identify **one scenario** where your model gives misleading predictions, and explain why.

---

## Recommended Modelling Approach

### Core model: Multi-ward SIS compartmental model

Each ward i has two patient compartments:
- **S_i** — Susceptible (uncolonised) patients
- **C_i** — Colonised (carrying resistant organism) patients

Optionally extend to include:
- **H_i** — Healthcare workers as an indirect transmission vector
- **E_i** — Environmental contamination

Key biological justifications to document:
- SIS (not SIR) is appropriate because colonisation is not permanent — patients can
  be decolonised naturally or via treatment.
- Constant ward population assumption (N_i = S_i + C_i) is justified by assuming
  beds are always occupied (typical in NHS settings).
- Transfer flows between wards create coupling: ICU → GM (10%), GS → ICU (5%).
- Antibiotic pressure modulates the effective decolonisation rate γ_i per ward.

### R₀ derivation
Use the **Next Generation Matrix (NGM)** method. For a single ward:
  R₀ = β_eff / (γ + μ)
where μ = 1 / avg_stay and β_eff is modulated by hand hygiene compliance.
For the multi-ward system, R₀ is the spectral radius (dominant eigenvalue) of the
next generation matrix K.

---

## Suggested Timeline (18 April – 17 May = 29 days)

| Week | Focus |
|------|-------|
| Week 1 (Apr 18–24) | Literature reading; agree on model structure and state variables |
| Week 2 (Apr 25 – May 1) | Write ODE system; derive R₀; begin coding baseline simulation |
| Week 3 (May 2–8) | Run baseline; code interventions A–D; sensitivity analysis |
| Week 4 (May 9–15) | Write report; record video; complete AI Use Statement |
| Final 2 days (May 16–17) | Proofread; package submission; upload to Moodle by 23:59 |

---

## Evaluation Rubric

| Criterion | Weight | AI-Resistant? |
|-----------|--------|---------------|
| Mathematical Framework | 25% | Moderate |
| Biological Realism & Justification | 25% | **High** |
| Analytical Depth | 20% | Moderate |
| Critical Thinking & Model Evaluation | 20% | **High** |
| Communication & Transparency | 10% | Low |

> The two highest-weighted criteria are both AI-resistant. Your own biological reasoning,
> modelling judgement, and critical evaluation are what win this competition.

---

## Submission Checklist

- [ ] Written Report — PDF, ≤ 20 pages
- [ ] Video Presentation — MP4, ≤ 10 minutes
- [ ] Simulation Code — all files (Python / MATLAB / R)
- [ ] AI Use Statement — PDF, 1 page (template provided)

All submissions via Moodle.

---

## Key References (Starting Points)

1. D'Agata et al. (2007) — *J. Theoretical Biology* — hospital AMR compartmental models
2. Lipsitch et al. (2000) — *PNAS* — epidemiology of antibiotic resistance in hospitals
3. Webb et al. (2005) — *PNAS* — antibiotic-resistant bacterial epidemic models
4. Bootsma et al. (2006) — *Am. J. Epidemiology* — bacterial acquisition routes in hospitals
5. WHO (2024) — *Global Report on Antimicrobial Resistance*

> Search beyond these. Look for papers on MRSA/MSSA hospital network models,
> hand hygiene intervention RCTs, and antibiotic stewardship programme evaluations.
