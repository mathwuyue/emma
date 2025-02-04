import os
import traceback
from datetime import datetime
from typing import Any, Dict

import dotenv
import httpx
import orjson as json
from capybara.llm import llm
from fastapi import HTTPException

from ..logger import logger
from ..prompt import (
    emma_glu_summary,
    get_food_info_prompt,
    get_food_nutrients_prompt,
    user_preference_summary,
)
from ..utils import extract_json_from_text
from .model import (
    DietaryData,
    DietarySummary,
    EmmaComment,
    NutritionMacro,
    NutritionMicro,
    NutritionMineral,
    UserBasicInfo,
    UserPreferenceData,
)

dotenv.load_dotenv()
