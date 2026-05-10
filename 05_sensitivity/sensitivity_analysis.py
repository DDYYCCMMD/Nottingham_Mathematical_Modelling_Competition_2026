"""PRCC sensitivity analysis for the 4-ward AMR model."""

import os
import sys
from copy import deepcopy
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import rankdata

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "03_simulation"))
import parameters
from main_simulation import (
    C_SLICE,
    H_SLICE,
    HCW_MAX_FRACTION,
    HCW_MIN_FRACTION,
    S_SLICE,
    build_params_dict,
    compute_R0,
    hospital_ode,
    run_baseline,
)

# Sensitivity parameters and bounds specified in the task.
PARAM_NAMES = ["beta_scale", "gamma_scale", "delta_scale", "alpha_scale"]
PARAM_BOUNDS = [
    (0.5, 1.5),
    (0.5, 1.5),
    (0.2, 1.0),
    (0.25, 2.0),
]

# Faster solver tolerances for the Monte Carlo loop.
SENSITIVITY_SOLVER_METHOD = "RK45"
SENSITIVITY_SOLVER_RTOL = 1.0e-4
SENSITIVITY_SOLVER_ATOL = 1.0e-6

# Plot settings for the tornado chart.
DEFAULT_SAVE_PATH = "03_simulation/figures/sensitivity.png"
TORNADO_FIGURE_SIZE = (12, 5)
TORNADO_DPI = 150
PRCC_AXIS_MIN = -1.0
PRCC_AXIS_MAX = 1.0
POSITIVE_COLOR = "green"
NEGATIVE_COLOR = "red"
VALUE_TEXT_OFFSET = 0.03
BAR_EDGE_COLOR = "black"


def latin_hypercube_sample(n_samples: int, bounds: list, seed: int = 42) -> np.ndarray:
    """Generate a Latin Hypercube sample over the provided parameter bounds."""
    rng = np.random.default_rng(seed)
    n_params = len(bounds)
    result = np.zeros((n_samples, n_params))

    for j, (low, high) in enumerate(bounds):
        cuts = np.linspace(0.0, 1.0, n_samples + 1)
        u = rng.uniform(cuts[:-1], cuts[1:])
        rng.shuffle(u)
        result[:, j] = low + u * (high - low)

    return result


def compute_prcc(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Compute parameter-wise PRCC values from regressions on ranked variables."""
    n_samples, n_params = X.shape
    if Y.shape[0] != n_samples:
        raise ValueError("X and Y must contain the same number of samples.")

    ranked_X = np.apply_along_axis(rankdata, 0, X)
    ranked_Y = rankdata(Y)
    prcc_values = np.zeros(n_params)
    intercept = np.ones((n_samples, 1))

    for j in range(n_params):
        other_indices = [k for k in range(n_params) if k != j]
        regressors = ranked_X[:, other_indices]
        design_matrix = np.hstack([intercept, regressors])

        y_coefficients, _, _, _ = np.linalg.lstsq(design_matrix, ranked_Y, rcond=None)
        y_residual = ranked_Y - design_matrix @ y_coefficients

        xj_coefficients, _, _, _ = np.linalg.lstsq(design_matrix, ranked_X[:, j], rcond=None)
        xj_residual = ranked_X[:, j] - design_matrix @ xj_coefficients

        prcc_values[j] = np.corrcoef(xj_residual, y_residual)[0, 1]

    return prcc_values


def run_sensitivity_analysis(n_samples: int = 1000, seed: int = 42) -> dict:
    """Evaluate R0 and 12-month prevalence across a Latin Hypercube design."""
    samples = latin_hypercube_sample(n_samples, PARAM_BOUNDS, seed=seed)
    r0_values = np.zeros(n_samples)
    prevalence_values = np.zeros(n_samples)
    total_capacity = np.sum(parameters.N)
    ward_count = parameters.N.size

    for sample_index, scales in enumerate(samples):
        params = deepcopy(build_params_dict())
        params["beta"] = parameters.beta * scales[0]
        params["gamma"] = parameters.gamma * scales[1]
        params["delta"] = parameters.delta_base * scales[2] * np.ones(ward_count)
        params["alpha"] = parameters.alpha * scales[3]

        r0_values[sample_index] = compute_R0(params)

        solution = solve_ivp(
            fun=lambda time, state: hospital_ode(time, state, params),
            t_span=parameters.T_SPAN,
            y0=parameters.y0,
            t_eval=np.array([parameters.T_EVAL[-1]]),
            method=SENSITIVITY_SOLVER_METHOD,
            rtol=SENSITIVITY_SOLVER_RTOL,
            atol=SENSITIVITY_SOLVER_ATOL,
        )

        if not solution.success:
            raise RuntimeError(
                f"Sensitivity simulation failed at sample {sample_index}: {solution.message}"
            )

        final_colonised = solution.y[C_SLICE, -1]
        prevalence_values[sample_index] = np.sum(final_colonised) / total_capacity

        # Keep the solver state bounded for HCW fractions when debugging outputs.
        _ = np.clip(solution.y[H_SLICE, -1], HCW_MIN_FRACTION, HCW_MAX_FRACTION)

    return {
        "samples": samples,
        "R0": r0_values,
        "prevalence": prevalence_values,
        "param_names": PARAM_NAMES,
        "param_bounds": PARAM_BOUNDS,
    }


def plot_tornado(prcc_r0, prcc_prev, param_names, save_path=DEFAULT_SAVE_PATH):
    """Plot side-by-side PRCC tornado charts for R0 and 12-month prevalence."""
    figure_path = Path(save_path)
    figure_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=TORNADO_FIGURE_SIZE, dpi=TORNADO_DPI)
    y_positions = np.arange(len(param_names))

    for axis, values, title in (
        (ax1, prcc_r0, "Sensitivity: R₀"),
        (ax2, prcc_prev, "Sensitivity: 12-month Prevalence"),
    ):
        colors = [POSITIVE_COLOR if value >= 0.0 else NEGATIVE_COLOR for value in values]
        axis.barh(y_positions, values, color=colors, edgecolor=BAR_EDGE_COLOR)
        axis.set_yticks(y_positions, labels=param_names)
        axis.set_xlim(PRCC_AXIS_MIN, PRCC_AXIS_MAX)
        axis.set_xlabel("PRCC")
        axis.set_title(title)
        axis.axvline(0.0, color="black", linewidth=1.0)

        for position, value in zip(y_positions, values):
            text_x = value + VALUE_TEXT_OFFSET if value >= 0.0 else value - VALUE_TEXT_OFFSET
            horizontal_alignment = "left" if value >= 0.0 else "right"
            axis.text(
                text_x,
                position,
                f"{value:.2f}",
                va="center",
                ha=horizontal_alignment,
            )

    fig.tight_layout()
    fig.savefig(figure_path)
    plt.close(fig)


if __name__ == "__main__":
    del run_baseline  # Imported per task requirements but not needed in this script.

    print("Running sensitivity analysis (n=1000 samples)...")
    sens_results = run_sensitivity_analysis(n_samples=1000, seed=42)
    prcc_r0 = compute_prcc(sens_results["samples"], sens_results["R0"])
    prcc_prev = compute_prcc(sens_results["samples"], sens_results["prevalence"])

    print("\nPRCC vs R0:")
    for name, val in zip(sens_results["param_names"], prcc_r0):
        print(f"  {name}: {val:.3f}")

    print("\nPRCC vs 12-month Prevalence:")
    for name, val in zip(sens_results["param_names"], prcc_prev):
        print(f"  {name}: {val:.3f}")

    human_names = [
        "β (transmission)",
        "γ (decolonisation)",
        "δ (hand hygiene)",
        "α (admission rate)",
    ]
    plot_tornado(prcc_r0, prcc_prev, human_names)
    print(f"\nFigure saved to {DEFAULT_SAVE_PATH}")
