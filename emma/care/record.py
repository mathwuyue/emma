from ..meta import HumanMeta
import datetime


def cal_exp_weight(humanmeta: HumanMeta) -> float:
    """
    Calculate the expected weight based on the user's current weight and gestational week.

    Args:
        humanmeta: User's human meta information
    """
    now = datetime.now()
    # If the current date and the stored expected weight date fall in the same ISO week (year and week number), return the stored expected weight
    if now.isocalendar()[:2] == humanmeta.cur_weight.exp_timestamp.isocalendar()[:2]:
        return humanmeta.cur_weight.exp_weight
    # Fallback: if not in the same week, return the current weight (or apply alternate logic as needed)
    if (
        not humanmeta.gestational_week
        or not humanmeta.gestational_week.gestational_week
    ):
        return humanmeta
    if now.isocalendar()[:2] != humanmeta.gestational_week.timestamp.isocalendar()[:2]:
        week_difference: int = (now - humanmeta.gestational_week.timestamp).days // 7
        if week_difference > 0:
            humanmeta.gestational_week.gestational_week += week_difference
            humanmeta.gestational_week.timestamp = now
            humanmeta.gestational_week.type = "2"
    return humanmeta.cur_weight.weight
