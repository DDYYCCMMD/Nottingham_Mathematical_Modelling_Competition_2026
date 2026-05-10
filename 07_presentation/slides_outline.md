# Video Presentation Outline — AMR Hospital Network Modelling
## Nottingham Mathematical Modelling Competition 2026
## Target length: ≤ 10 minutes

---

### Slide 1 — Title (30 seconds)

**Title:** Modelling Antimicrobial Resistance Dynamics in a Hospital Network

**Subtitle:** A Coupled SIS+HCW Compartmental Model

**Visual:** Simple diagram of 4 connected wards (GM–GS–ICU–GW) with arrows showing patient transfers

**Script:**
> "In this presentation, we model the transmission dynamics of antimicrobial-resistant bacteria across a four-ward hospital network, derive analytically the basic reproduction number governing resistance persistence, and evaluate four evidence-based intervention strategies over a 12-month horizon."

---

### Slide 2 — Problem & Motivation (60 seconds)

**Title:** Why Hospital AMR Matters

**Visuals:**
- Table: 4 wards with beds, length of stay, antibiotic use
- Brief bullet: "AMR kills >700,000 people/year globally; hospitals are primary transmission hotspots"

**Script:**
> "Our hospital has four wards — General Medicine, General Surgery, ICU, and Geriatric — each with different bed capacities, patient turnover rates, and antibiotic use levels. The ICU uses antibiotics in 80% of patients for an average of 12 days, creating the highest selective pressure for resistance. Patient transfers between wards couple these environments: 5% of surgical patients are transferred to ICU, and 10% of ICU patients step down to General Medicine. Our research question: which combination of interventions most cost-effectively reduces endemic AMR colonisation across this network?"

---

### Slide 3 — Model Structure (90 seconds)

**Title:** The SIS + HCW Compartmental Model

**Visuals:**
- Flow diagram: S_i ↔ C_i with arrows labelled β·(C/N)·S, λ·H·S, α·μ·N, (γ+μ)·C
- Small box for H_i with arrows: η·(C/N)·(1−H) in, δ·H out
- Transfer arrows between ward boxes

**ODE display (show, don't derive):**
```
dC_i/dt = β_i(C_i/N_i)S_i + λ_i H_i S_i + α_i μ_i N_i − (γ_i+μ_i)C_i ± transfers
dH_i/dt = η_i(C_i/N_i)(1−H_i) − δ_i H_i
```

**Script:**
> "Each ward has two patient compartments — susceptible S and colonised C — and a healthcare worker compartment H tracking the proportion of HCWs with contaminated hands. We chose SIS rather than SIR because AMR colonisation confers no immunity: patients can be decolonised and immediately recolonised. We include the HCW compartment because D'Agata et al. show it is the central transmission pathway — omitting it would underestimate R₀ by 30–50%. Antibiotic pressure modulates both the transmission rate β and the decolonisation rate γ per ward."

---

### Slide 4 — R₀ Analysis (60 seconds)

**Title:** Basic Reproduction Number R₀ = 0.96

**Visuals:**
- Box: "R₀ = ρ(F·V⁻¹) = 0.96"
- Small 2×2 block structure of K matrix (illustrative, not full 8×8)
- Two bullet interpretations

**Script:**
> "We derive R₀ using the Next Generation Matrix method. The infected compartments — four colonised patient pools and four HCW contamination pools — form an 8×8 system. The spectral radius of the next generation matrix gives R₀ = 0.96 — below 1. This means in-hospital transmission alone cannot sustain endemic AMR. The disease-free equilibrium is stable in the absence of external forcing. However, AMR persists endemically because of the constant admission colonisation forcing term: every day, approximately 4% of admissions carry resistant organisms, continuously seeding each ward regardless of R₀. Complete eradication therefore requires both R₀ < 1 — already satisfied — and near-elimination of admission colonisation. Scenario B moves strongly in this direction by reducing admission colonisation by 80%, but does not set it exactly to zero."

---

### Slide 5 — Baseline Simulation Results (60 seconds)

**Title:** Baseline: 12-Month Colonisation Dynamics

**Visuals:**
- Figure 1: 4-panel baseline prevalence plot
- Table: Day-365 prevalence by ward vs literature ranges

**Script:**
> "Simulating over 365 days from realistic initial conditions, all four wards reach approximate steady state within 120 days. The ICU reaches 15.6% colonisation, consistent with Bootsma et al.'s reported ICU prevalence of 15–26%. General Medicine reaches only 5.1% — reflecting its lower antibiotic pressure and shorter stays. The Geriatric Ward exceeds General Surgery despite lower antibiotic use because its longer stays accumulate greater cumulative exposure — illustrating that length of stay is an independent AMR risk factor."

---

### Slide 6 — Intervention Results (90 seconds)

**Title:** Which Intervention Works Best?

**Visuals:**
- Figure 2: 4-panel intervention comparison plot
- Table 2: R₀ and ward prevalence for all 5 scenarios
- Highlight row: Scenario B (most dramatic prevalence reduction)

**Script:**
> "We tested four interventions. Scenario A — raising hand hygiene compliance to 80% — reduces R₀ from 0.96 to 0.95 but has negligible impact on endemic prevalence. Why? Because endemic prevalence is maintained by a constant stream of colonised admissions, which hand hygiene alone cannot address. Scenario B — universal admission screening plus contact precautions — produces the most dramatic result: system prevalence drops from 7.3% to just 1.0%, with R₀ falling to 0.70. Its strength is that it simultaneously targets the two strongest prevalence drivers: admission colonisation, reduced by 80%, and direct transmission, reduced by 30%. Scenario C, antibiotic stewardship, reduces system prevalence by 12%, most effectively in the ICU. The combined Scenario D achieves the lowest R₀ at 0.88, but its system prevalence of 6.3% is far higher than Scenario B because it does not address admission colonisation."

---

### Slide 7 — Sensitivity Analysis (45 seconds)

**Title:** What Drives R₀ vs. What Drives Prevalence

**Visuals:**
- Figure 3: Two-panel tornado plot (PRCC for R₀ and prevalence side by side)
- Callout box: "δ: moderate for R₀ (−0.52), weak for prevalence (−0.14). α: negligible for R₀ (−0.02), strong for prevalence (+0.92). β dominates both."

**Script:**
> "PRCC analysis reveals a critical asymmetry. For R₀, β (+0.99) and γ (−0.96) dominate, while δ has moderate influence (−0.52) and α is negligible. For 12-month prevalence, β (+0.95) and α (+0.92) jointly dominate — admission colonisation rate α leaps from irrelevant to the second strongest driver. This means a hospital using R₀ to prioritise interventions would invest in hand hygiene and antibiotic stewardship while under-investing in admission screening — exactly backwards for reducing endemic prevalence. Scenario B is optimal precisely because it simultaneously targets both top prevalence drivers: β through contact precautions and α through admission screening."

---

### Slide 8 — Critical Evaluation (60 seconds)

**Title:** Model Limitations and Honest Assessment

**Visuals:**
- Three bullet limitations with one-line descriptions
- One callout: "Appropriate use: endemic planning. Not appropriate: outbreak prediction."

**Script:**
> "Our model has three significant limitations. First, homogeneous mixing within wards: real transmission is spatially structured by bed proximity and nursing assignments, which we cannot capture. Second, deterministic ODE for the 15-bed ICU: stochastic extinction is possible when R₀ is only modestly above 1, which our model cannot represent. Third, static parameters: real compliance improvements decay over time. We also considered but rejected an individual-based model — because it cannot support sensitivity analysis — and a two-strain model — because resistance emergence is a multi-year process beyond our 12-month horizon. Finally, this model should be used as a steady-state planning tool, not as an outbreak prediction engine: during an active outbreak, emergency management responses zero the transfer rates and raise compliance in ways our static parameters cannot capture."

---

### Slide 9 — Conclusion & Recommendation (45 seconds)

**Title:** Recommendation to the Hospital Board

**Visuals:**
- Three action items with icons
- Bottom line: "R₀ is necessary but insufficient — target admission colonisation to reduce endemic burden"

**Script:**
> "Our recommendation to the hospital board: implement universal admission screening and contact precautions as the primary intervention — this most strongly suppresses endemic prevalence by targeting both imported colonisation and direct transmission. Antibiotic stewardship should be presented as a separate follow-on policy for sustained management of antibiotic selection pressure in high-intensity wards, rather than as a model-tested B+C optimum. Maintain hand hygiene improvement as a baseline standard, particularly for its structural effect on R₀ and outbreak risk. The key scientific lesson from this analysis: R₀ and endemic prevalence have different sensitivity profiles, and optimising interventions for prevalence reduction — the metric that matters clinically — requires targeting admission colonisation and transmission together."

---

## Timing Summary

| Slide | Content | Time |
|-------|---------|------|
| 1 | Title | 0:30 |
| 2 | Problem & motivation | 1:30 |
| 3 | Model structure | 3:00 |
| 4 | R₀ analysis | 4:00 |
| 5 | Baseline results | 5:00 |
| 6 | Intervention results | 6:30 |
| 7 | Sensitivity analysis | 7:15 |
| 8 | Critical evaluation | 8:15 |
| 9 | Conclusion | 9:00 |
| **Total** | | **9:00** |

*Allow 1 minute buffer for transitions and pauses.*
