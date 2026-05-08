"""
Model parameters for 4-ward hospital AMR transmission model.
All values from literature unless noted. Units in days.

Sources:
- D'Agata et al. (2007) J. Theor. Biol. 249:487-499
- Lipsitch et al. (2000) PNAS 97:1938-1943
- Bootsma et al. (preprint -> Am. J. Epidemiol.) ICU acquisition routes
- Webb et al. (2005) PNAS 102:13343-13348
"""

import numpy as np

# Ward indices used consistently across all state vectors and matrices.
GM, GS, ICU, GW = 0, 1, 2, 3
WARD_NAMES = ["General Medicine", "General Surgery", "ICU", "Geriatric Ward"]

# Fixed bed capacities per ward under the always-occupied assumption.
N = np.array([60.0, 40.0, 15.0, 30.0])

# Average length of stay in days by ward, used to derive discharge/admission
# rate mu_i = 1 / average length of stay.
AVG_STAY_DAYS = np.array([5.0, 7.0, 12.0, 14.0])
mu = 1.0 / AVG_STAY_DAYS

# Antibiotic exposure proportions by ward (dimensionless fraction in [0, 1]).
ANTIBIOTIC_USE_FRACTIONS = np.array([0.40, 0.60, 0.80, 0.50])
antibiotic_use = ANTIBIOTIC_USE_FRACTIONS

# Direct patient-to-patient transmission baseline (per day) and multiplicative
# antibiotic amplification from the model specification.
BETA_BASE_PER_DAY = 0.10
ANTIBIOTIC_BETA_MULTIPLIER = 0.5
beta_base = BETA_BASE_PER_DAY
beta = beta_base * (1.0 + ANTIBIOTIC_BETA_MULTIPLIER * antibiotic_use)

# Baseline decolonisation rate (per day) and antibiotic-associated reduction.
GAMMA_BASE_PER_DAY = 0.10
ANTIBIOTIC_GAMMA_REDUCTION = 0.5
gamma_base = GAMMA_BASE_PER_DAY
gamma = gamma_base * (1.0 - ANTIBIOTIC_GAMMA_REDUCTION * antibiotic_use)

# HCW-mediated transmission rates (per day), elevated in ICU per literature.
lambda_hcw = np.array([0.04, 0.04, 0.06, 0.04])

# HCW contamination rates (per day), again with higher ICU acquisition pressure.
eta = np.array([0.3, 0.3, 0.5, 0.3])

# Hand-hygiene baseline assumptions: 10 effective contacts/day with 50%
# compliance, so decontamination rate is contacts * compliance.
HAND_HYGIENE_COMPLIANCE_BASELINE = 0.50
HCW_CONTACTS_PER_DAY = 10.0
NUMBER_OF_WARDS = 4
hand_hygiene_compliance_baseline = HAND_HYGIENE_COMPLIANCE_BASELINE
contacts_per_day = HCW_CONTACTS_PER_DAY
delta_base = contacts_per_day
delta = delta_base * hand_hygiene_compliance_baseline * np.ones(NUMBER_OF_WARDS)

# Admission colonisation fraction from the problem statement range 3%-5%;
# 4% is used as the common midpoint across wards.
ADMISSION_COLONISATION_FRACTION = 0.04
alpha = ADMISSION_COLONISATION_FRACTION * np.ones(NUMBER_OF_WARDS)

# Inter-ward transfer matrix T[i, j] gives movement FROM ward i TO ward j.
# Rates are implemented as per-stay fractions divided by mean stay in origin ward.
T = np.zeros((NUMBER_OF_WARDS, NUMBER_OF_WARDS))
GS_TO_ICU_TRANSFER_FRACTION_PER_STAY = 0.05
ICU_TO_GM_TRANSFER_FRACTION_PER_STAY = 0.10
T[GS, ICU] = GS_TO_ICU_TRANSFER_FRACTION_PER_STAY / AVG_STAY_DAYS[GS]
T[ICU, GM] = ICU_TO_GM_TRANSFER_FRACTION_PER_STAY / AVG_STAY_DAYS[ICU]

# Initial colonised patient fractions by ward and resulting state vector blocks.
INITIAL_COLONISED_FRACTIONS = np.array([0.05, 0.05, 0.10, 0.05])
C0_frac = INITIAL_COLONISED_FRACTIONS
C0 = C0_frac * N
S0 = N - C0

# Initial contaminated HCW fractions, constrained to [0, 1].
INITIAL_HCW_CONTAMINATION_FRACTIONS = np.array([0.05, 0.05, 0.10, 0.05])
H0 = INITIAL_HCW_CONTAMINATION_FRACTIONS
y0 = np.concatenate([S0, C0, H0])

# One-year simulation horizon with daily evaluation points.
SIMULATION_START_DAY = 0
SIMULATION_END_DAY = 365
SIMULATION_NUM_EVAL_POINTS = 366
T_SPAN = (SIMULATION_START_DAY, SIMULATION_END_DAY)
T_EVAL = np.linspace(SIMULATION_START_DAY, SIMULATION_END_DAY, SIMULATION_NUM_EVAL_POINTS)

# Intervention scenario constants.
IMPROVED_HAND_HYGIENE_COMPLIANCE = 0.80
REDUCED_ANTIBIOTIC_USE_FACTOR = 0.70
ADMISSION_SCREENING_ALPHA_REDUCTION_FACTOR = 0.20
BETA_REDUCTION_FACTOR_WITH_BUNDLE = 0.70

# Scenario A: improved hand hygiene only.
SCENARIO_A = {"delta": delta_base * IMPROVED_HAND_HYGIENE_COMPLIANCE * np.ones(NUMBER_OF_WARDS)}

# Scenario B: stronger admission control and reduced transmission pressure.
antibiotic_use_C = antibiotic_use * REDUCED_ANTIBIOTIC_USE_FACTOR
SCENARIO_B = {
    "alpha": alpha * ADMISSION_SCREENING_ALPHA_REDUCTION_FACTOR,
    "beta": beta * BETA_REDUCTION_FACTOR_WITH_BUNDLE,
}

# Scenario C: reduced antibiotic pressure increases decolonisation.
SCENARIO_C = {
    "gamma": gamma_base * (1.0 - ANTIBIOTIC_GAMMA_REDUCTION * antibiotic_use_C)
}

# Scenario D: combined hand hygiene and antibiotic stewardship.
SCENARIO_D = {
    "delta": delta_base * IMPROVED_HAND_HYGIENE_COMPLIANCE * np.ones(NUMBER_OF_WARDS),
    "gamma": gamma_base * (1.0 - ANTIBIOTIC_GAMMA_REDUCTION * antibiotic_use_C),
}
