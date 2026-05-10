# Mathematical Model Derivation — AMR Hospital Network

**Author:** Claude (Architect & Analyst)  
**Date:** 2026-05-08  
**Status:** Complete — approved for use in report and code implementation

---

## 1. State Variables

The hospital network comprises four wards indexed $i \in \{0, 1, 2, 3\}$ corresponding to General Medicine (GM), General Surgery (GS), Intensive Care Unit (ICU), and Geriatric Ward (GW).

For each ward $i$ at time $t$ (in days):

| Variable | Definition |
|----------|-----------|
| $S_i(t)$ | Number of **susceptible** (uncolonised) patients in ward $i$ |
| $C_i(t)$ | Number of **colonised** (AMR-carrying) patients in ward $i$ |
| $H_i(t)$ | **Proportion** of healthcare workers in ward $i$ with contaminated hands, $H_i \in [0,1]$ |

**Population constraint:** $S_i(t) + C_i(t) = N_i$ for all $t$, where $N_i$ is the fixed ward capacity (beds always occupied).

This is a **12-dimensional system**: $\mathbf{y} = (S_0, S_1, S_2, S_3, C_0, C_1, C_2, C_3, H_0, H_1, H_2, H_3)$.

---

## 2. ODE System

### 2.1 Colonised Patients $C_i$

$$\frac{dC_i}{dt} = \underbrace{\beta_i \frac{C_i}{N_i} S_i}_{\text{direct P-P transmission}} + \underbrace{\lambda_i H_i S_i}_{\text{HCW-mediated transmission}} + \underbrace{\alpha_i \mu_i N_i}_{\text{admission colonisation}} - \underbrace{(\gamma_i + \mu_i) C_i}_{\text{decolonisation + discharge}} - \underbrace{\left(\sum_{j \neq i} T_{ij}\right) C_i}_{\text{transfer out}}$$

### 2.2 Susceptible Patients $S_i$

Since $S_i = N_i - C_i$, we have:

$$\frac{dS_i}{dt} = \underbrace{\mu_i N_i}_{\text{clean admissions}} - \underbrace{\beta_i \frac{C_i}{N_i} S_i}_{\text{direct transmission}} - \underbrace{\lambda_i H_i S_i}_{\text{HCW-mediated}} + \underbrace{\gamma_i C_i}_{\text{decolonisation}} - \underbrace{\mu_i S_i}_{\text{discharge}} + \underbrace{\sum_{j \neq i} T_{ji} C_j}_{\text{transfer inflow (colonised)}}$$

**Note on transfers:** Patient transfers couple the wards. When a colonised patient transfers from ward $j$ to ward $i$, they leave the $C_j$ pool (reducing $dC_j/dt$) and enter $C_i$ (increasing $dC_i/dt$). Transfer rates $T_{ij}$ have units of (fraction of ward $i$ population transferred to ward $j$ per day).

### 2.3 HCW Contamination $H_i$

$$\frac{dH_i}{dt} = \underbrace{\eta_i \frac{C_i}{N_i}(1 - H_i)}_{\text{contamination from colonised patients}} - \underbrace{\delta_i H_i}_{\text{decontamination (hand hygiene)}}$$

At quasi-steady state (fast HCW dynamics relative to patient turnover):
$$H_i^* = \frac{\eta_i (C_i/N_i)}{\delta_i + \eta_i (C_i/N_i)}$$

This saturating form prevents $H_i > 1$ naturally, but we treat $H_i$ as a dynamic variable to capture non-equilibrium effects.

---

## 3. Term-by-Term Biological Justification

### 3.1 Direct patient-to-patient transmission: $\beta_i (C_i/N_i) S_i$
**Mechanism:** Resistant organisms spread through environmental contamination (shared surfaces, equipment, air droplets) at a rate proportional to the fraction of colonised patients. The mass-action term $(C_i/N_i) \cdot S_i$ is standard for homogeneous mixing within a closed ward.  
**Biological justification:** Validated by Lipsitch et al. (2000) for hospital AMR compartmental models. D'Agata et al. (2007) confirm that patient-to-patient spread is one of two primary transmission routes in their IBM.  
**Ward-specific $\beta_i$:** Higher antibiotic pressure selects for resistant organisms and increases the concentration of resistant bacteria in the environment, effectively amplifying direct transmission. We parameterise $\beta_i = \beta_{\text{base}} \times (1 + 0.5 \times a_i)$, where $a_i$ is the antibiotic use proportion. This gives ICU the highest $\beta$ (antibiotic use 80%), consistent with D'Agata 2007.

### 3.2 HCW-mediated transmission: $\lambda_i H_i S_i$
**Mechanism:** Healthcare workers with contaminated hands transmit organisms to susceptible patients at each contact. The rate is proportional to the fraction of HCWs contaminated ($H_i$) and the number of susceptible patients ($S_i$).  
**Biological justification:** D'Agata et al. (2007) model HCW contamination as the central transmission pathway in their IBM. Bootsma et al. estimate that exogenous (HCW-mediated) cross-transmission accounts for 21–29% of ICU acquisitions; the remaining endogenous acquisition is still partially HCW-driven through environmental contamination. Omitting $H_i$ would underestimate total transmission and overestimate the effect of patient-only interventions.

### 3.3 Admission colonisation: $\alpha_i \mu_i N_i$
**Mechanism:** A fraction $\alpha_i = 3{-}5\%$ of newly admitted patients are already colonised on arrival (community-acquired or from other facilities). The admission rate is $\mu_i N_i$ patients per day (since $1/\mu_i$ is average length of stay).  
**Biological justification:** The problem statement specifies 3–5% admission colonisation rate. Lipsitch et al. (2000) identify admission colonisation as a key parameter determining whether endemic persistence is possible even when in-hospital R₀ < 1. This term acts as a constant forcing function, preventing true disease-free equilibrium and making eradication difficult.

### 3.4 Decolonisation: $\gamma_i C_i$
**Mechanism:** Colonised patients clear the resistant organism at rate $\gamma_i$ per day through immune-mediated clearance or decolonisation treatment.  
**Biological justification:** Webb et al. (2005) demonstrate that resistant bacteria can revert to susceptible form through plasmid loss — this is the molecular basis for the $C \to S$ transition. Antibiotic use reduces the effective decolonisation rate by selecting for resistant organisms: $\gamma_i = \gamma_{\text{base}} \times (1 - 0.5 \times a_i)$. This means ICU (80% antibiotic use) has the lowest decolonisation rate, driving higher endemic prevalence.

### 3.5 Discharge/admission rate: $\mu_i$
**Mechanism:** Patients leave (discharge) and are replaced by new admissions at rate $\mu_i = 1/(\text{avg stay in days})$. The outgoing patients are replaced by clean admissions (fraction $1-\alpha_i$) or colonised admissions (fraction $\alpha_i$).

### 3.6 HCW contamination: $\eta_i (C_i/N_i)(1 - H_i)$
**Mechanism:** Uncontaminated HCWs become contaminated at a rate proportional to the prevalence of colonised patients and the fraction of HCWs currently uncontaminated ($1-H_i$). The saturating form prevents $H_i > 1$.  
**ICU-specific:** We set $\eta_{\text{ICU}} = 0.5 > \eta_{\text{other}} = 0.3$ to reflect higher procedural contact rates in ICU.

### 3.7 HCW decontamination: $\delta_i H_i$
**Mechanism:** Contaminated HCWs revert to uncontaminated state through hand hygiene. At 50% compliance with 10 contacts/day and 100% efficacy per contact: $\delta \approx 10 \times 0.5 \times 1.0 = 5$/day.  
**Intervention lever:** $\delta_i$ is the primary parameter modified in Scenario A (hand hygiene improvement). At 80% compliance: $\delta \to 10 \times 0.80 = 8$/day.

---

## 4. Model Choice Justification

### 4.1 Why SIS, not SIR
The standard SIR framework assumes that recovered individuals gain permanent immunity — appropriate for diseases like measles or influenza where recovered individuals are protected. AMR colonisation does **not** confer immunity. Decolonisation (loss of the resistant organism) returns the patient to a fully susceptible state because:
1. AMR colonisation is carriage of bacteria, not infection producing immunological memory
2. Webb et al. (2005) demonstrate explicit plasmid loss events — resistant organisms revert to non-resistant, and patients carrying only non-resistant organisms are fully susceptible to re-colonisation with resistant strains
3. Clinical observation confirms high rates of recurrent MRSA colonisation in the same patients (D'Agata 2007)

An SIR model would incorrectly predict that decolonised patients cannot be re-colonised, systematically underestimating long-run AMR prevalence.

### 4.2 Why constant ward population $N_i$
NHS bed occupancy routinely exceeds 95–98%. The assumption $S_i + C_i = N_i = \text{constant}$ is standard in hospital AMR models (Lipsitch et al. 2000; Cooper et al. 2004). The error introduced is bounded by the ~2–5% unoccupied bed fraction, which is smaller than the uncertainty in the transmission parameters $\beta_i$.

An alternative with variable occupancy would require modelling admission queues and bed management policies, adding parameters with high uncertainty and no significant improvement in the main outcomes of interest (endemic prevalence, R₀).

### 4.3 Why include HCW compartment $H_i$
D'Agata et al. (2007) show that HCW-mediated transmission is the primary mechanism in their IBM. Bootsma et al. attribute 21–29% of ICU colonisations to cross-transmission (predominantly HCW-mediated). Omitting $H_i$ would:
- Underestimate total transmission (and thus R₀)
- Overestimate the effectiveness of patient isolation alone
- Prevent modelling of hand hygiene interventions (Scenario A)

### 4.4 Why antibiotic pressure modulates $\beta_i$ and $\gamma_i$
Antibiotic pressure has two effects: (1) it selects for resistant organisms, increasing the effective transmission advantage of resistant strains (higher $\beta_i$); (2) it impairs natural decolonisation by suppressing competing susceptible flora that would otherwise outcompete the resistant strain (lower $\gamma_i$). Both effects are supported by D'Agata et al. (2007) and Webb et al. (2005). Our linear scaling is a simplification — the relationship is likely nonlinear — but captures the direction and qualitative magnitude of the effect.

---

## 5. Basic Reproduction Number R₀ — Next Generation Matrix Method

### 5.1 Overview
R₀ is the expected number of secondary colonisations produced by one colonised individual introduced into an otherwise susceptible, AMR-free population. For a multi-ward system, R₀ = ρ(K), the spectral radius of the Next Generation Matrix K = F·V⁻¹.

### 5.2 Disease-Free Equilibrium (DFE)
For R₀ calculation, we set admission colonisation $\alpha_i = 0$ (temporarily) to allow a true disease-free equilibrium. The DFE is:
$$S_i^* = N_i, \quad C_i^* = 0, \quad H_i^* = 0 \quad \forall i$$

### 5.3 Infected Compartments
We identify 8 infected compartments: $\{C_0, C_1, C_2, C_3, H_0, H_1, H_2, H_3\}$.

Order the state vector as: $\mathbf{x} = (C_0, C_1, C_2, C_3, H_0, H_1, H_2, H_3)$.

### 5.4 New Infection Matrix F (8×8)

F captures only *new* transmissions (not transitions between existing infected compartments). At the DFE ($S_i = N_i$):

**Direct patient-to-patient (C → C):** 
$$F_{i,i} = \beta_i \quad (i = 0,1,2,3)$$

**HCW-mediated (H → C, i.e., H_i creates new C_i):**
$$F_{i,\,4+i} = \lambda_i N_i \quad (i = 0,1,2,3)$$

**HCW contamination from colonised patients (C → H):**

Since $H_i$ is a *dimensionless fraction*, linearising $dH_i/dt = \eta_i (C_i/N_i)(1-H_i)$ at the DFE ($C_i=0$, $H_i=0$) with respect to $C_i$ gives:
$$F_{4+i,\,i} = \frac{\eta_i}{N_i} \quad (i = 0,1,2,3)$$

All other entries of F are zero.

$$\mathbf{F} = \begin{pmatrix} \mathrm{diag}(\beta_i) & \mathrm{diag}(\lambda_i N_i) \\ \mathrm{diag}(\eta_i/N_i) & \mathbf{0} \end{pmatrix}$$

### 5.5 Transition Matrix V (8×8)

V captures all outflows from infected compartments (excluding new transmissions):

**Patient colonisation outflows (diagonal, C_i):**
$$V_{i,i} = \gamma_i + \mu_i + \sum_{j \neq i} T_{ij} \quad (i = 0,1,2,3)$$

**HCW decontamination (diagonal, H_i):**
$$V_{4+i,4+i} = \delta_i \quad (i = 0,1,2,3)$$

Inter-ward transfers move already colonised patients between infected compartments, so the patient block of $V$ contains off-diagonal transition terms $-T_{ji}$ in addition to the diagonal loss terms.

$$\mathbf{V} = \begin{pmatrix} \mathrm{diag}(\gamma_i + \mu_i + \sigma_i) - \mathbf{T}^{\top} & \mathbf{0} \\ \mathbf{0} & \mathrm{diag}(\delta_i) \end{pmatrix}$$

where $\sigma_i = \sum_{j \neq i} T_{ij}$ is the total transfer-out rate from ward $i$. Under the one-way transfer structure used in this project, including the off-diagonal entries makes the NGM construction fully consistent with the ODE system while leaving the numerical value of $R_0$ unchanged.

### 5.6 Next Generation Matrix K = F·V⁻¹

Because the patient block of $V$ contains the transfer terms $-\mathbf{T}^{\top}$, the full inverse $V^{-1}$ is computed numerically rather than written as a simple diagonal expression. The next-generation matrix is therefore

$$\mathbf{K} = \mathbf{F} \cdot \mathbf{V}^{-1}$$

and **R₀ = ρ(K)** is the dominant eigenvalue of this 8×8 matrix.

### 5.7 Single-Ward Analytical Formula
For a single isolated ward with no transfers ($\sigma_i = 0$) and no HCW:
$$R_0^{\text{simple}} = \frac{\beta_i}{\gamma_i + \mu_i}$$

With HCW compartment (still no transfers), the 2×2 sub-block for ward $i$ is:
$$K_i = \begin{pmatrix} \frac{\beta_i}{\gamma_i+\mu_i} & \frac{\lambda_i N_i}{\delta_i} \\ \frac{\eta_i}{N_i(\gamma_i+\mu_i)} & 0 \end{pmatrix}$$

The spectral radius of this 2×2 block:
$$R_0^{\text{ward}} = \frac{\beta_i}{2(\gamma_i+\mu_i)} + \sqrt{\left(\frac{\beta_i}{2(\gamma_i+\mu_i)}\right)^2 + \frac{\lambda_i \eta_i}{\delta_i (\gamma_i+\mu_i)}}$$

For the full 4-ward system, R₀ = ρ(K) must be computed numerically (dominant eigenvalue of the 8×8 matrix).

### 5.8 Stability Theorem
By the Diekmann-Heesterbeek-Metz theorem:
- If R₀ < 1: the DFE is **locally asymptotically stable** — a small introduction of resistant organisms will die out
- If R₀ > 1: the DFE is **unstable** — resistant organisms will persist at an endemic equilibrium

**Note:** The admission colonisation term $\alpha_i \mu_i N_i$ creates a forced input even when R₀ < 1, so complete eradication requires both R₀ < 1 AND $\alpha_i \to 0$ (admission screening). This is the mechanism behind Scenario B's effectiveness.

---

## 6. Parameter Table

| Symbol | Definition | GM | GS | ICU | GW | Unit | Source |
|--------|-----------|----|----|-----|----|----|--------|
| $N_i$ | Ward capacity | 60 | 40 | 15 | 30 | beds | Problem |
| $\mu_i$ | Discharge rate | 0.200 | 0.143 | 0.083 | 0.071 | /day | Problem |
| $\beta_i$ | Direct transmission rate | 0.120 | 0.130 | 0.140 | 0.125 | /day | Bootsma; Lipsitch |
| $\gamma_i$ | Decolonisation rate | 0.080 | 0.070 | 0.060 | 0.075 | /day | Lipsitch 2000 |
| $\lambda_i$ | HCW transmission rate | 0.04 | 0.04 | 0.06 | 0.04 | /day | D'Agata 2007 |
| $\eta_i$ | HCW contamination rate | 0.3 | 0.3 | 0.5 | 0.3 | /day | D'Agata 2007 |
| $\delta_i$ | HCW decontamination rate | 5.0 | 5.0 | 5.0 | 5.0 | /day | Bootsma preprint |
| $\alpha_i$ | Admission colonisation fraction | 0.04 | 0.04 | 0.04 | 0.04 | — | Problem |
| $T_{GS \to ICU}$ | GS→ICU transfer rate | — | 0.007 | — | — | /day | Problem |
| $T_{ICU \to GM}$ | ICU→GM transfer rate | — | — | 0.008 | — | /day | Problem |

Transfer rates computed as: $T_{GS \to ICU} = 0.05 / \text{avg\_stay}_{GS} = 0.05/7 = 0.0071$/day (5% of GS patients transfer to ICU during their stay). $T_{ICU \to GM} = 0.10/12 = 0.0083$/day.

---

## 7. Validated Numerical Results

The implementation consistent with the corrected NGM and HCW linearisation reproduces the following baseline outputs:

| Quantity | Value |
|----------|-------|
| System $R_0$ | 0.9641 |
| GM prevalence (Day 365) | 5.08% |
| GS prevalence (Day 365) | 5.98% |
| ICU prevalence (Day 365) | 15.65% |
| GW prevalence (Day 365) | 9.26% |
| System prevalence (Day 365) | 7.29% |

These are the values that should be treated as the current validation targets for the code and report.
