# Nottingham Mathematical Modelling Competition 2026

## Project Overview

Model antimicrobial resistance (AMR) transmission dynamics in a 4-ward hospital network.
Full problem statement: `docs/problem/Math_Competition_Three_Campuses.pdf`
Deadline: **17 May 2026, 23:59 GMT+8** — submit via Moodle.

---

## Role Division

### Claude (Architect & Analyst)
- Designs the mathematical model structure (compartments, state variables, ODE system)
- Derives R₀ analytically using the Next Generation Matrix method
- Writes biological justifications for every modelling choice
- Designs intervention scenarios and interprets simulation results
- Authors Part C (critical evaluation) — this section is AI-resistant and must be Claude's own reasoning
- Reviews and validates all code Codex produces before it is used
- Writes the final report (`06_report/`) and presentation outline (`07_presentation/`)
- **Does not write simulation or analysis code — all coding is delegated to Codex**

### Codex (Scientific Computing)
- Implements all Python simulation code as specified by Claude
- Receives tasks via `/ask codex` with exact file paths and function specifications
- Returns completed code for Claude to review against the Linus Three Questions
- Runs code and reports numerical outputs / errors back to Claude

---

## Collaboration Workflow

### Standard task delegation
```
/ask codex "<task description> — target file: <path>"
/pend codex      # wait for result
/ping codex      # keep connection alive if needed
```

### Full work loop
```
1. Claude designs model / specifies function interface
2. Claude → /ask codex "implement X — file: src/Y.py — spec: ..."
3. Codex writes and runs the code
4. /pend codex to receive result
5. Claude applies Linus Three Questions to the output
6. Pass → move to next task | Fail → send specific feedback to Codex
```

---

## Fallback Protocol

| Situation | Action |
|-----------|--------|
| Codex unresponsive | Wait 30 s, then retry `/ask codex` |
| Codex fails twice | Claude provides a more detailed spec / pseudocode, then re-delegates |
| Codex fails three times | Pause; report blocker to user; request manual intervention |
| Task too complex | Claude breaks it into smaller subtasks before delegating |

---

## Linus Three Questions (required before every code acceptance)

Before Claude accepts any code from Codex, answer all three:

1. **Does it work?** — Does it produce correct numerical output? Are edge cases handled?
2. **Is it right?** — Is the mathematical logic faithful to the ODE system Claude designed?
3. **Is it good?** — Is it readable, reproducible, and free of hard-coded magic numbers?

All three must pass. Otherwise, return to Codex with specific line-level feedback.

---

## Task List

### Phase 1 — Literature & Model Design (Claude leads)
- [ ] Read and annotate all 4 reference papers in `docs/reference/`
- [ ] Finalise ODE system for all 4 wards — document in `02_model/model_derivation.md`
- [ ] Derive R₀ analytically (NGM method) — document in `02_model/model_derivation.md`
- [ ] Define all parameters with biological sources — update `03_simulation/parameters.py`

### Phase 2 — Baseline Simulation (Codex codes, Claude reviews)
- [ ] `/ask codex` — implement `hospital_ode()` in `03_simulation/main_simulation.py`
- [ ] `/ask codex` — implement `run_simulation()` and baseline plots in `03_simulation/main_simulation.py`
- [ ] Claude validates: do steady-state prevalence values match literature estimates?

### Phase 3 — Intervention Analysis (Codex codes, Claude designs scenarios)
- [ ] Claude specifies parameter changes for interventions A, B, C, D
- [ ] `/ask codex` — implement `04_intervention/intervention_analysis.py`
- [ ] Claude interprets results and writes recommendation section

### Phase 4 — Sensitivity Analysis (Codex codes, Claude selects parameters)
- [ ] Claude selects ≥3 parameters for sensitivity analysis (β, γ, hand hygiene compliance)
- [ ] `/ask codex` — implement `05_sensitivity/sensitivity_analysis.py` (tornado plot or PRCC)
- [ ] Claude interprets which parameters most affect R₀ and prevalence

### Phase 5 — Report & Presentation (Claude writes)
- [ ] Draft full report in `06_report/report_draft.md` → export to PDF (≤ 20 pages)
- [ ] Write AI Use Statement in `08_submission/AI_Use_Statement.md`
- [ ] Write presentation script / slide outline in `07_presentation/slides_outline.md`
- [ ] Record video (≤ 10 minutes, MP4)

### Phase 6 — Submission
- [ ] Package all files into `08_submission/`
- [ ] Upload to Moodle before 17 May 2026, 23:59 GMT+8

---

## Key Constraints

- Part C (critical evaluation) must be written entirely by Claude — it is the most AI-resistant section and is worth 20% of the rubric. Do not delegate to Codex.
- Every biological justification in the report must come from Claude's own reasoning, backed by the reference papers.
- The AI Use Statement must honestly document which tasks were delegated to Codex and how outputs were validated.
- All simulation code must be reproducible: fixed random seeds, no hard-coded paths, clear inline comments.

---

## File Map

```
docs/problem/Math_Competition_Three_Campuses.pdf   ← problem statement (read-only)
docs/rules/Competition_Rules_And_Guidelines.pdf    ← rules (read-only)
docs/reference/                                    ← 4 reference papers (read-only)

02_model/model_derivation.md                       ← ODE system + R₀ derivation (Claude writes)
03_simulation/parameters.py                        ← all model parameters
03_simulation/main_simulation.py                   ← baseline ODE solver + plots
03_simulation/figures/                             ← all output figures
04_intervention/intervention_analysis.py           ← Part B scenarios
05_sensitivity/sensitivity_analysis.py             ← sensitivity + tornado plot
06_report/report_draft.md                          ← full report draft
07_presentation/slides_outline.md                  ← video presentation outline
08_submission/AI_Use_Statement.md                  ← mandatory 1-page disclosure
```
