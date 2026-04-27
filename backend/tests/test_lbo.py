from app.services.lbo_engine import run_lbo_model


def test_lbo_basic():
    result = run_lbo_model(
        ebitda=100,
        entry_multiple=10,
        exit_multiple=10,
        leverage=0.6,
        growth_rate=0.05,
        holding_period=5,
    )
    assert result["entry_ev"] == 1000
    assert result["irr"] > 0
