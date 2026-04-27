"""LBO model with Monte Carlo sensitivity analysis."""
import numpy as np


def run_lbo_model(
    ebitda: float,
    entry_multiple: float,
    exit_multiple: float,
    leverage: float,
    growth_rate: float,
    holding_period: int = 5,
) -> dict:
    """Compute base-case LBO returns."""
    enterprise_value = ebitda * entry_multiple
    debt = enterprise_value * leverage
    equity = enterprise_value - debt

    final_ebitda = ebitda * (1 + growth_rate) ** holding_period
    exit_ev = final_ebitda * exit_multiple
    exit_equity = exit_ev - debt  # assume bullet, simplified

    moic = exit_equity / equity if equity > 0 else 0
    irr = (moic ** (1 / holding_period) - 1) if moic > 0 else -1

    return {
        "entry_ev": enterprise_value,
        "equity_check": equity,
        "exit_equity": exit_equity,
        "moic": moic,
        "irr": irr,
    }


def monte_carlo_lbo(base_params: dict, n_sims: int = 1000) -> dict:
    """Run Monte Carlo over key LBO inputs."""
    irrs = []
    for _ in range(n_sims):
        params = {
            "ebitda": base_params["ebitda"] * np.random.normal(1.0, 0.05),
            "entry_multiple": base_params["entry_multiple"],
            "exit_multiple": base_params["exit_multiple"] * np.random.normal(1.0, 0.10),
            "leverage": base_params["leverage"],
            "growth_rate": np.random.normal(base_params["growth_rate"], 0.02),
            "holding_period": base_params["holding_period"],
        }
        irrs.append(run_lbo_model(**params)["irr"])
    return {
        "p10": float(np.percentile(irrs, 10)),
        "p50": float(np.percentile(irrs, 50)),
        "p90": float(np.percentile(irrs, 90)),
        "mean": float(np.mean(irrs)),
    }
