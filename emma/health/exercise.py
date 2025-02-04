import os
import traceback
from datetime import datetime, timedelta
from typing import Any, Dict, Tuple

import dotenv
import httpx
import orjson as json
from capybara.llm import llm

from ..db import ExerciseDatabase, db
from ..logger import logger
from ..prompt import emma_exercise_summary, get_exercise_info
from ..utils import extract_json_from_text
from .model import EmmaComment, UserBasicInfo

dotenv.load_dotenv()


def cal_calories_met(weight: float, duration: float, met: float) -> float:
    met * duration / 60 * 1.05 * weight


def cal_max_bpm(age: int) -> float:
    if not age:
        age = 30
    return 208 - 0.7 * age


def cal_exercise_bpm_range(age: int) -> Tuple[int, int]:
    """TODO: Maybe we can use HRR to calculate the range"""
    return (int(0.6 * (220 - age)), int(0.89 * (220 - age)))


async def extract_exercise_info(image_url):
    """
    Analyze exercise image to get the exercise data
    """
    query = [
        {"type": "text", "text": get_exercise_info()},
        {"type": "image_url", "image_url": {"url": image_url}},
    ]
    # Analyze food image
    exercise_info = await llm(query, model="qwen-vl-max", temperature=0.1, is_text=True)
    return exercise_info


async def get_exercise_summary(
    user_data: str,
    exercise: str,
    intensity: str,
    duration: float,
    bpm: float,
    start_time,
    remark: str,
    previous_records: list[Dict[str, Any]],
) -> Tuple[EmmaComment, float]:
    """
    TODO: How to get the meal time?
    """
    # get from db
    with db.atomic():
        exercise_data = ExerciseDatabase.get_or_none(
            (ExerciseDatabase.exercise == exercise)
            & (ExerciseDatabase.type == intensity)
        )
    # calcualte caories. Check ExerciseDatabase for the formula
    if not exercise_data:
        met = 0.0  # Default value
    else:
        met = exercise_data.calories
    # user_data = UserBasicInfo(**user_data_response.json())
    # print(user_data)
    # Calculate calories based on duration and base calories from database
    calories = cal_calories_met(
        float(user_data.cur_weight), float(duration), float(met)
    )
    conditions = f"{user_data.condition} (Level {user_data.cond_level})"
    new_record = {
        "exercise": exercise,
        "intensity": intensity,
        "duration": duration,
        "calories": calories,
        "bpm": bpm,
        "start_time": start_time,
        "remark": remark,
    }
    # format records
    exercise_records = format_exercise_records(previous_records)
    # calculate exercise bpm range
    min_bpm, max_bpm = cal_exercise_bpm_range(user_data.age)
    # prompt
    prompt = emma_exercise_summary(
        new_record,
        exercise_records,
        user_data.cur_weight,
        user_data.ga,
        conditions,
        user_data.complications,
        {"min": min_bpm, "max": max_bpm},
    )
    llm_json = extract_json_from_text(await llm(prompt, is_text=True))
    if not calories:
        calories = llm_json["calories"]
    return EmmaComment(**llm_json), calories


def format_exercise_records(previous_records) -> dict:
    """Format ExerciseData records into standardized JSON structure"""
    formatted_data = []

    for record in previous_records:
        formatted_data.append(
            {
                "datetime": record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "exercise": record.exercise,
                "intensity": record.intensity,
                "duration": record.duration,
                "calories": float(record.calories),
            }
        )

    return {"total": len(formatted_data), "data": formatted_data}
