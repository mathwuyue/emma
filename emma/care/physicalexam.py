from datetime import datetime, timedelta

from capybara.llm import llm

from ..prompt import emma_report_comment, exam_report_ocr_prompt
from ..utils import extract_json_from_text

physicalexam_ga = [6, 12, 13, 17, 21, 25, 29, 33, 36, 37, 38, 39, 40]
physicalexam_notice = [
    "初次孕检，空腹，确认孕周",
    "NT检查，建档",
    "唐氏筛查，此后超声如无医嘱，无需憋尿",
    "四维检查，大排畸，主要检查胎儿外观发育上是否有较大问题",
    "OGTT糖耐，空腹，妊娠糖尿病筛查",
    "乙肝筛查",
    "水肿，子痫前症筛查，系统性彩超排除胎儿发育异常",
    "详细的超声检查，评估胎儿发育状况",
    "胎心监护，续监视胎儿的状态",
    "做B超、专家做产前评估，预估分娩方式",
    "胎位固定",
    "胎儿各项数据采集",
    "复查超声",
]
physicalexam_title = [
    "6-7周早期孕检",
    "12周第一次孕检",
    "13-16周第二次孕检",
    "17-20周第三次孕检",
    "21-24周第四次孕检",
    "25-28周第五次孕检",
    "29-32周第六次孕检",
    "33-35周第七次孕检",
    "36周第八次孕检",
    "37周第九次孕检",
    "38周第十次孕检",
    "39周第十一次孕检",
    "40周第十二次孕检",
]


def _calculate_mon_of_gestational_age(lmp: str, exp_gestational_week: int) -> str:
    """
    Calculate the Monday date of the specified expected gestational week.

    Args:
        cur_gestational_week: Current gestational week (integer)
        exp_gestational_week: Target gestational week to calculate Monday for

    Returns:
        ISO format date string of the Monday in the target gestational week
    """

    try:
        lmp_date = datetime.strptime(lmp, "%Y-%m-%d").date()
    except ValueError:
        return None
    if exp_gestational_week <= 0:
        return None
    # Calculate the target date for the expected gestational week.
    # We assume gestational week 1 starts at lmp, so subtract 1 before multiplying by 7 days.
    target_date = lmp_date + timedelta(weeks=exp_gestational_week - 1)
    # Determine the Monday of that week by subtracting the weekday number (Monday=0).
    monday_date = target_date - timedelta(days=target_date.weekday())
    return monday_date.isoformat()


def generate_physicalexam_list(lmp: str) -> list:
    """
    Generate a list of physical exam tasks based on the current gestational week.

    Args:
        cur_gestational_week: Current gestational week (integer)

    Returns:
        List of physical exam tasks (strings)
    """

    # Calculate Monday dates for each expected gestational week
    monday_dates = [
        _calculate_mon_of_gestational_age(lmp, exp_week) for exp_week in physicalexam_ga
    ]

    # Generate physical exam list
    physical_exam_list = [
        (date, notice, title)
        for date, notice, title in zip(
            monday_dates, physicalexam_notice, physicalexam_title
        )
    ]

    return physical_exam_list


async def exam_report_ocr(pic_urls: list) -> str:
    prompt = exam_report_ocr_prompt()
    query = [{"type": "text", "text": prompt}] + [
        {
            "type": "image_url",
            "image_url": {"url": url},
        }
        for url in pic_urls
    ]
    response = await llm(query, model="qwen-vl-max", temperature=0.1, is_text=True)
    return extract_json_from_text(response)


async def exam_report_analysis(report):
    prompt = emma_report_comment(report=report)
    result = await llm(prompt, temperature=0.1, is_text=True)
    return result
