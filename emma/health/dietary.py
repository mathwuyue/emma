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

# from ..prompt import (
#     emma_glu_summary,
#     get_food_info_prompt,
#     get_food_nutrients_prompt,
#     user_preference_summary,
# )
from ..utils import extract_json_from_text
from jinja2 import Template

# from .model import (
#     DietaryData,
#     DietarySummary,
#     EmmaComment,
#     NutritionMacro,
#     NutritionMicro,
#     NutritionMineral,
#     UserBasicInfo,
#     UserPreferenceData,
# )

# dotenv.load_dotenv()

prompt = Template(
    """我的体重是59.3公斤，身高1.77，孕周是7周，血糖正常，口味是 {{ cuisine }}。请给我推荐一个一天的食谱。要求：1. 符合孕妇营养健康要求，每天分为5餐：早餐、早加餐（一般是水果、坚果、乳制品等）、中餐、下午茶（一般是水果、坚果等，注意不要和早加餐冲突）、晚餐。2. 要求推荐具体食物和食物量（按照克计算） 3. 对于早、中、晚三餐，根据推荐的食物，组合成一个或多个菜谱，给出菜的名称（title）、菜的做法（description）、包含的食物和用量（[{"name": "鱼", "amount": "200"}]。返回如下JSON格式：{"dailyfood": [
    {"name": "早餐", "recipes": [
        {"title": "西红柿炒蛋", "description": "西红柿洗净了炒鸡蛋", "foods": [{"name": "西红柿", "amount": 200]},{"name":"鸡蛋", "amount": 100}]},
        {"title": "牛奶", "description": "牛奶是动物乳制品", "foods": [{"name": "牛奶", "amount": 200}]}
    ]},
    {"name": "午餐", "recipes": [
        {"title": "鱼香肉丝", "description": "猪肉丝炒青椒", "foods": [{"name": "猪肉", "amount": 200},{"name":"青椒", "amount": 100}]},
        {"title": "米饭", "description": "大米煮熟了", "foods": [{"name": "大米", "amount": 200}]}
    ]},
    {"name": "晚餐", "recipes": [
        {"title": "红烧肉", "description": "猪肉炖土豆", "foods": [{"name": "猪肉", "amount": 200},{"name":"土豆", "amount": 100}]},
        {"title": "面条", "description": "面条是面制品", "foods": [{"name": "面条", "amount": 200}]}
    ]}
    ]}"""
)


async def emma_daily_dietary(cuisine="闽菜"):
    query = prompt.render(cuisine=cuisine)
    dietary_data = await llm(query, is_test=True)
    return extract_json_from_text(dietary_data)
