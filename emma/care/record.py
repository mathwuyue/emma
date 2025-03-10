import datetime

from ..meta import HumanMeta


def cal_exp_weight(humanmeta: HumanMeta) -> HumanMeta:
    """
    Calculate the expected weight range based on the user's BMI and gestational week.

    Args:
        humanmeta: User's human meta information
    """
    if (
        not humanmeta.cur_weight
        or not humanmeta.gestational_week
        or not humanmeta.gestational_week.gestational_week
        or not humanmeta.bmi
        or not humanmeta.pre_weight
    ):
        return humanmeta

    now = datetime.datetime.now()

    # If the current date and the stored expected weight date fall in the same ISO week, return the stored expected weight
    if now.isocalendar()[:2] == humanmeta.cur_weight.exp_timestamp.isocalendar()[:2]:
        return humanmeta
    # Fallback: if not in the same week, return the current weight (or apply alternate logic as needed)
    if now.isocalendar()[:2] != humanmeta.gestational_week.timestamp.isocalendar()[:2]:
        week_difference: int = (now - humanmeta.gestational_week.timestamp).days // 7
        if week_difference > 0:
            humanmeta.gestational_week.gestational_week += week_difference
            humanmeta.gestational_week.timestamp = now
            humanmeta.gestational_week.type = "2"
    else:
        return humanmeta

    # Get current gestational week
    current_week = humanmeta.gestational_week.gestational_week
    pre_pregnancy_weight = humanmeta.pre_weight
    bmi = humanmeta.bmi

    # Calculate expected min and max weight based on BMI category and gestational week
    if bmi < 18.5:  # Underweight
        if current_week <= 13:  # Early pregnancy
            min_weight = pre_pregnancy_weight + 1
            max_weight = pre_pregnancy_weight + 2
        else:  # Mid to late pregnancy
            mid_late_gain_min = (current_week - 13) * 0.44
            mid_late_gain_max = (current_week - 13) * 0.58
            min_weight = pre_pregnancy_weight + 1 + mid_late_gain_min
            max_weight = pre_pregnancy_weight + 2 + mid_late_gain_max

    elif bmi < 25:  # Normal weight
        if current_week <= 13:  # Early pregnancy
            min_weight = pre_pregnancy_weight + 1
            max_weight = pre_pregnancy_weight + 2
        else:  # Mid to late pregnancy
            mid_late_gain_min = (current_week - 13) * 0.35
            mid_late_gain_max = (current_week - 13) * 0.5
            min_weight = pre_pregnancy_weight + 1 + mid_late_gain_min
            max_weight = pre_pregnancy_weight + 2 + mid_late_gain_max

    elif bmi < 30:  # Overweight
        if current_week <= 13:  # Early pregnancy
            min_weight = pre_pregnancy_weight + 0.5
            max_weight = pre_pregnancy_weight + 2
        else:  # Mid to late pregnancy
            mid_late_gain_min = (current_week - 13) * 0.23
            mid_late_gain_max = (current_week - 13) * 0.33
            min_weight = pre_pregnancy_weight + 0.5 + mid_late_gain_min
            max_weight = pre_pregnancy_weight + 2 + mid_late_gain_max

    else:  # Obese
        if current_week <= 13:  # Early pregnancy
            min_weight = pre_pregnancy_weight + 0.5
            max_weight = pre_pregnancy_weight + 2
        else:  # Mid to late pregnancy
            mid_late_gain_min = (current_week - 13) * 0.17
            mid_late_gain_max = (current_week - 13) * 0.27
            min_weight = pre_pregnancy_weight + 0.5 + mid_late_gain_min
            max_weight = pre_pregnancy_weight + 2 + mid_late_gain_max

    # Round to one decimal place for better readability
    min_weight = round(min_weight, 1)
    max_weight = round(max_weight, 1)

    # Update humanmeta with the calculated expected weight range
    humanmeta.cur_weight.exp_min_weight = min_weight
    humanmeta.cur_weight.exp_max_weight = max_weight
    humanmeta.cur_weight.exp_timestamp = now

    return humanmeta
