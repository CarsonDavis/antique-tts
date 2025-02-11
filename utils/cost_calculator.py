# utils/cost_calculator.py


def calculate_cost(char_count: int, cost_per_char: float) -> float:
    """Calculate total cost for synthesis"""
    return char_count * cost_per_char


def get_user_confirmation(total_cost: float) -> bool:
    """Get user confirmation if cost is greater than 0"""
    if total_cost <= 0:
        return True

    response = input(
        f"\nEstimated cost: ${total_cost:.2f}\n" f"Do you want to proceed? (y/N): "
    ).lower()
    return response == "y"
