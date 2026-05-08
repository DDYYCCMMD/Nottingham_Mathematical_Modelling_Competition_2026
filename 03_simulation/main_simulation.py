"""Baseline ODE simulation and R0 calculation for the 4-ward AMR model."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import parameters

# Structural constants derived from the shared parameter module so this file
# does not duplicate model dimensions.
WARD_COUNT = parameters.N.size
STATE_BLOCK_SIZE = WARD_COUNT
PATIENT_STATE_SIZE = STATE_BLOCK_SIZE + STATE_BLOCK_SIZE
TOTAL_STATE_SIZE = PATIENT_STATE_SIZE + STATE_BLOCK_SIZE
INFECTED_COMPARTMENT_SIZE = PATIENT_STATE_SIZE

# Named slices for the 12-element state vector y = [S, C, H].
S_SLICE = slice(0, STATE_BLOCK_SIZE)
C_SLICE = slice(STATE_BLOCK_SIZE, PATIENT_STATE_SIZE)
H_SLICE = slice(PATIENT_STATE_SIZE, TOTAL_STATE_SIZE)

# Plotting and solver configuration requested by the task description.
DEFAULT_SAVE_PATH = "03_simulation/figures/baseline.png"
SOLVER_METHOD = "RK45"
SOLVER_RTOL = 1.0e-6
SOLVER_ATOL = 1.0e-8
FIGURE_WIDTH_INCHES = 10
FIGURE_HEIGHT_INCHES = 8
FIGURE_DPI = 150
PREVALENCE_AXIS_MIN = 0.0
PREVALENCE_AXIS_MAX = 0.5
REFERENCE_PREVALENCE = 0.05
HCW_MIN_FRACTION = 0.0
HCW_MAX_FRACTION = 1.0

# Build a 2x2 layout from the number of wards instead of hardcoding panel order.
FIGURE_ROWS = int(np.sqrt(WARD_COUNT))
FIGURE_COLS = int(np.ceil(WARD_COUNT / FIGURE_ROWS))


def hospital_ode(t, y, params):
    """Return the 12-dimensional ODE right-hand side for the AMR model."""
    del t  # Autonomous system: the right-hand side does not depend explicitly on time.

    S = y[S_SLICE]
    C = y[C_SLICE]
    H = y[H_SLICE]
    H_clipped = np.clip(H, HCW_MIN_FRACTION, HCW_MAX_FRACTION)

    N = params["N"]
    mu = params["mu"]
    beta = params["beta"]
    gamma = params["gamma"]
    lambda_hcw = params["lambda_hcw"]
    eta = params["eta"]
    delta = params["delta"]
    alpha = params["alpha"]
    transfer_matrix = params["T"]

    colonised_fraction = C / N
    outgoing_transfer_rate = np.sum(transfer_matrix, axis=1)
    incoming_colonised_flow = transfer_matrix.T @ C

    dC = (
        beta * colonised_fraction * S  # Direct patient-to-patient transmission.
        + lambda_hcw * H_clipped * S  # HCW-mediated transmission into patients.
        + alpha * mu * N  # Colonised admissions replacing discharges.
        - (gamma + mu) * C  # Decolonisation plus discharge of colonised patients.
        - outgoing_transfer_rate * C  # Transfer outflow of colonised patients.
        + incoming_colonised_flow  # Transfer inflow of colonised patients from other wards.
    )
    dS = -dC
    dH = (
        eta * colonised_fraction * (HCW_MAX_FRACTION - H_clipped)  # HCW contamination acquisition.
        - delta * H_clipped  # HCW decontamination from hand hygiene.
    )

    return np.concatenate([dS, dC, dH])


def build_params_dict():
    """Construct the baseline parameter dictionary from the shared parameter module."""
    return {
        "N": parameters.N,
        "mu": parameters.mu,
        "beta": parameters.beta,
        "gamma": parameters.gamma,
        "lambda_hcw": parameters.lambda_hcw,
        "eta": parameters.eta,
        "delta": parameters.delta,
        "alpha": parameters.alpha,
        "T": parameters.T,
    }


def compute_R0(params):
    """Compute the basic reproduction number using the Next Generation Matrix."""
    F = np.zeros((INFECTED_COMPARTMENT_SIZE, INFECTED_COMPARTMENT_SIZE))
    V = np.zeros((INFECTED_COMPARTMENT_SIZE, INFECTED_COMPARTMENT_SIZE))

    patient_indices = np.arange(STATE_BLOCK_SIZE)
    hcw_indices = STATE_BLOCK_SIZE + patient_indices

    F[patient_indices, patient_indices] = params["beta"]
    F[patient_indices, hcw_indices] = params["lambda_hcw"] * params["N"]
    F[hcw_indices, patient_indices] = params["eta"]

    V[patient_indices, patient_indices] = (
        params["gamma"] + params["mu"] + np.sum(params["T"], axis=1)
    )
    V[hcw_indices, hcw_indices] = params["delta"]

    next_generation_matrix = F @ np.linalg.inv(V)
    spectral_radius = np.max(np.abs(np.linalg.eigvals(next_generation_matrix)))
    return float(np.real_if_close(spectral_radius))


def run_baseline():
    """Solve the baseline ODE system over the configured simulation horizon."""
    params = build_params_dict()
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
        raise RuntimeError(f"Baseline simulation failed: {solution.message}")

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


def plot_baseline(result, save_path=DEFAULT_SAVE_PATH):
    """Plot ward-level colonisation prevalence trajectories and save the figure."""
    figure_path = Path(save_path)
    figure_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(
        FIGURE_ROWS,
        FIGURE_COLS,
        figsize=(FIGURE_WIDTH_INCHES, FIGURE_HEIGHT_INCHES),
        dpi=FIGURE_DPI,
        sharex=True,
        sharey=True,
    )
    axes_flat = np.atleast_1d(axes).ravel()

    for ward_index, ward_name in enumerate(parameters.WARD_NAMES):
        axis = axes_flat[ward_index]
        axis.plot(result["t"], result["prevalence"][ward_index, :], linewidth=1.5)
        axis.axhline(
            REFERENCE_PREVALENCE,
            linestyle="--",
            color="gray",
            linewidth=1.0,
        )
        axis.set_ylim(PREVALENCE_AXIS_MIN, PREVALENCE_AXIS_MAX)
        axis.set_title(ward_name)
        axis.set_xlabel("Days")
        axis.set_ylabel("Colonisation Prevalence")

    for axis in axes_flat[WARD_COUNT:]:
        axis.set_visible(False)

    fig.tight_layout()
    fig.savefig(figure_path)
    plt.close(fig)


if __name__ == "__main__":
    params = build_params_dict()
    r0 = compute_R0(params)
    print(f"System R0 = {r0:.4f}")
    result = run_baseline()
    for i, name in enumerate(parameters.WARD_NAMES):
        final_prev = result["prevalence"][i, -1]
        print(f"{name}: final prevalence = {final_prev:.3f} ({final_prev * 100:.1f}%)")
    plot_baseline(result)
    print(f"Figure saved to {DEFAULT_SAVE_PATH}")
