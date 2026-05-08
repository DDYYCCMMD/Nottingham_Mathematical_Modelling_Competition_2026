"""Scenario analysis for ward-level AMR interventions."""

import copy
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "03_simulation"))
import parameters
from main_simulation import (
    C_SLICE,
    H_SLICE,
    HCW_MAX_FRACTION,
    HCW_MIN_FRACTION,
    S_SLICE,
    SOLVER_ATOL,
    SOLVER_METHOD,
    SOLVER_RTOL,
    build_params_dict,
    compute_R0,
    hospital_ode,
)

# Intervention comparison figure settings requested by the task description.
INTERVENTION_FIGURE_SIZE = (12, 9)
INTERVENTION_FIGURE_DPI = 150
INTERVENTION_PREVALENCE_MIN = 0.0
INTERVENTION_PREVALENCE_MAX = 0.4
REFERENCE_PREVALENCE = 0.05
DEFAULT_SAVE_PATH = "03_simulation/figures/interventions.png"

# The four wards are displayed in a 2x2 panel layout.
FIGURE_ROWS = 2
FIGURE_COLS = 2

# Line styles for each scenario to keep the comparison plot deterministic.
BASELINE_LINEWIDTH = 2.0
STANDARD_LINEWIDTH = 1.5
SCENARIO_STYLES = {
    "Baseline": {"color": "black", "linestyle": "-", "linewidth": BASELINE_LINEWIDTH},
    "A: Hand Hygiene": {"color": "blue", "linestyle": "-", "linewidth": STANDARD_LINEWIDTH},
    "B: Admission Screening": {"color": "orange", "linestyle": "--", "linewidth": STANDARD_LINEWIDTH},
    "C: Antibiotic Stewardship": {"color": "green", "linestyle": "-.", "linewidth": STANDARD_LINEWIDTH},
    "D: Combined A+C": {"color": "red", "linestyle": "-", "linewidth": BASELINE_LINEWIDTH},
}

def run_scenario(scenario_params: dict) -> dict:
    """Run the ODE model with a baseline parameter set overridden by one scenario."""
    params = copy.deepcopy(build_params_dict())
    for key, value in scenario_params.items():
        params[key] = copy.deepcopy(value)

    solution = solve_ivp(
        fun=lambda time, state: hospital_ode(time, state, params),
        t_span=parameters.T_SPAN,
        y0=parameters.y0,
        t_eval=parameters.T_EVAL,
        method=SOLVER_METHOD,
        rtol=SOLVER_RTOL,
        atol=SOLVER_ATOL,
    )

    if not solution.success:
        raise RuntimeError(f"Scenario simulation failed: {solution.message}")

    S = solution.y[S_SLICE, :]
    C = solution.y[C_SLICE, :]
    H = np.clip(solution.y[H_SLICE, :], HCW_MIN_FRACTION, HCW_MAX_FRACTION)
    prevalence = C / params["N"][:, np.newaxis]

    return {
        "t": solution.t,
        "S": S,
        "C": C,
        "H": H,
        "prevalence": prevalence,
    }


def compute_scenario_R0(scenario_params: dict) -> float:
    """Return the reproduction number for a scenario-overridden parameter set."""
    params = copy.deepcopy(build_params_dict())
    params.update(copy.deepcopy(scenario_params))
    return compute_R0(params)


def plot_interventions(results: dict, save_path=DEFAULT_SAVE_PATH):
    """Plot prevalence trajectories for all intervention scenarios by ward."""
    figure_path = Path(save_path)
    figure_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(
        FIGURE_ROWS,
        FIGURE_COLS,
        figsize=INTERVENTION_FIGURE_SIZE,
        dpi=INTERVENTION_FIGURE_DPI,
        sharex=True,
        sharey=True,
    )
    axes_flat = np.atleast_1d(axes).ravel()

    for ward_index, ward_name in enumerate(parameters.WARD_NAMES):
        axis = axes_flat[ward_index]
        for scenario_name, result in results.items():
            axis.plot(
                result["t"],
                result["prevalence"][ward_index, :],
                label=scenario_name,
                **SCENARIO_STYLES[scenario_name],
            )
        axis.axhline(
            REFERENCE_PREVALENCE,
            linestyle="--",
            color="gray",
            linewidth=1.0,
        )
        axis.set_title(ward_name)
        axis.set_xlabel("Days")
        axis.set_ylabel("Colonisation Prevalence")
        axis.set_ylim(INTERVENTION_PREVALENCE_MIN, INTERVENTION_PREVALENCE_MAX)

    axes_flat[0].legend()
    fig.tight_layout()
    fig.savefig(figure_path)
    plt.close(fig)


def summary_table(results: dict, r0s: dict):
    """Print a compact scenario summary table with ward and system prevalence."""
    total_capacity = np.sum(parameters.N)
    scenario_column_width = max(len("Scenario"), max(len(name) for name in results))
    r0_column_width = len("R0")
    ward_column_width = max(len("ICU"), len("15.6%"))
    system_column_width = max(len("System"), len("100.0%"))

    header = (
        f"{'Scenario':<{scenario_column_width}} | "
        f"{'R0':<{r0_column_width}} | "
        f"{'GM':<{ward_column_width}} | "
        f"{'GS':<{ward_column_width}} | "
        f"{'ICU':<{ward_column_width}} | "
        f"{'GW':<{ward_column_width}} | "
        f"{'System':<{system_column_width}}"
    )
    divider = (
        f"{'-' * scenario_column_width}|"
        f"{'-' * (r0_column_width + 2)}|"
        f"{'-' * (ward_column_width + 2)}|"
        f"{'-' * (ward_column_width + 2)}|"
        f"{'-' * (ward_column_width + 2)}|"
        f"{'-' * (ward_column_width + 2)}|"
        f"{'-' * (system_column_width + 1)}"
    )

    print(header)
    print(divider)
    for scenario_name, result in results.items():
        final_prevalence = result["prevalence"][:, -1]
        final_colonised_counts = result["C"][:, -1]
        system_prevalence = np.sum(final_colonised_counts) / total_capacity
        gm_display = f"{final_prevalence[parameters.GM] * 100:.1f}%"
        gs_display = f"{final_prevalence[parameters.GS] * 100:.1f}%"
        icu_display = f"{final_prevalence[parameters.ICU] * 100:.1f}%"
        gw_display = f"{final_prevalence[parameters.GW] * 100:.1f}%"
        system_display = f"{system_prevalence * 100:.1f}%"
        print(
            f"{scenario_name:<{scenario_column_width}} | "
            f"{r0s[scenario_name]:<{r0_column_width}.2f} | "
            f"{gm_display:<{ward_column_width}} | "
            f"{gs_display:<{ward_column_width}} | "
            f"{icu_display:<{ward_column_width}} | "
            f"{gw_display:<{ward_column_width}} | "
            f"{system_display:<{system_column_width}}"
        )


if __name__ == "__main__":
    scenarios = {
        "Baseline": {},
        "A: Hand Hygiene": parameters.SCENARIO_A,
        "B: Admission Screening": parameters.SCENARIO_B,
        "C: Antibiotic Stewardship": parameters.SCENARIO_C,
        "D: Combined A+C": parameters.SCENARIO_D,
    }

    results = {}
    r0s = {}
    for name, scenario_params in scenarios.items():
        results[name] = run_scenario(scenario_params)
        r0s[name] = compute_scenario_R0(scenario_params)

    summary_table(results, r0s)
    plot_interventions(results)
    print(f"Figure saved to {DEFAULT_SAVE_PATH}")
