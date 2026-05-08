# AI Use Statement

**Competition:** Nottingham Mathematical Modelling Competition 2026  
**Topic:** Modelling Antimicrobial Resistance Dynamics in a Hospital Network  
**Submission date:** 17 May 2026  
**Organiser:** Elio Espejo, School of Mathematical Sciences, UNNC

---

## 1. Summary

This submission used two AI tools — **Claude (Anthropic, claude-sonnet-4-6)** and **Codex (OpenAI)** — coordinated through the Claude Code environment. The division of labour is described below. All AI-generated outputs were reviewed and validated before use.

---

## 2. Division of Labour

### Claude was responsible for:
- Reading and annotating all four reference papers (D'Agata 2007, Webb 2005, Bootsma preprint, Lipsitch 2000) and extracting parameter estimates with literature justification
- Designing the complete mathematical model structure: state variables, ODE system, all parameter definitions
- Deriving R₀ analytically using the Next Generation Matrix method (Section 3)
- Writing all biological justifications for modelling choices (SIS vs SIR, HCW compartment, constant population, antibiotic-pressure parameterisation)
- Designing all four intervention scenarios and specifying the exact parameter changes for each
- Interpreting all simulation and sensitivity analysis results
- Writing the complete report (all sections, including all text, tables, and interpretation)
- Writing **Section 7 (Critical Evaluation)** entirely from original analytical reasoning — this section was not delegated to any AI tool
- Writing this AI Use Statement and the presentation outline

### Codex was responsible for:
- Implementing `03_simulation/parameters.py` — all numerical parameters with named constants and comments, as specified by Claude
- Implementing `03_simulation/main_simulation.py` — ODE solver (`hospital_ode`), R₀ calculator (`compute_R0`), baseline runner (`run_baseline`), and figure generator (`plot_baseline`)
- Implementing `04_intervention/intervention_analysis.py` — scenario runner (`run_scenario`), comparison plotter, and summary table
- Implementing `05_sensitivity/sensitivity_analysis.py` — Latin Hypercube Sampling, PRCC computation, and tornado plot generator

---

## 3. Validation Process

All code produced by Codex was reviewed by Claude against the **Linus Three Questions** before acceptance:

1. **Does it work?** — Code was executed; numerical outputs were checked for correctness and absence of errors
2. **Is it right?** — Mathematical logic was verified against the ODE system and NGM derivation specified in `02_model/model_derivation.md`; output values (R₀, prevalence by ward) were checked against expected ranges from the literature
3. **Is it good?** — Code was read for readability, absence of hard-coded magic numbers, and correct use of named constants from `parameters.py`

No code was accepted without passing all three questions. Specific validation evidence:
- `parameters.py`: ward population conservation verified (`S + C = N` for all wards), H₀ ∈ [0,1] confirmed
- `main_simulation.py`: R₀ = 1.3595 verified against analytical single-ward formula; ICU prevalence 15.6% confirmed within Bootsma literature range of 15–26%
- `intervention_analysis.py`: all scenario R₀ ≤ baseline R₀; PRCC signs verified against mechanistic expectations
- `sensitivity_analysis.py`: PRCC signs verified (β positive, γ negative, δ negative for R₀); α negligible for R₀ but dominant for prevalence confirmed

---

## 4. What AI Did NOT Do

- The **critical evaluation** (Section 7) was written entirely by Claude from original analytical reasoning. No AI tool was asked to evaluate model limitations or propose alternative models.
- All **biological justifications** throughout the report represent Claude's own reasoning from the reference papers, not templated responses.
- The **policy recommendation** (Section 5.4) reflects Claude's own synthesis of the quantitative results and their biological interpretation.
- No AI tool wrote the **mathematical derivations** in Section 3 (NGM method) — these were derived by Claude and documented before any code was written.

---

## 5. Reproducibility

All simulation code is fully reproducible:
- Fixed random seed (seed=42) in sensitivity analysis
- No hard-coded file paths; all paths are relative to the project root
- All parameters in a single source file (`03_simulation/parameters.py`) with literature citations
- Complete implementation plan documented in `docs/superpowers/plans/2026-05-08-amr-hospital-modelling.md`

To reproduce all results:
```bash
python3 03_simulation/main_simulation.py
python3 04_intervention/intervention_analysis.py
python3 05_sensitivity/sensitivity_analysis.py
```
