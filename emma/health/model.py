from typing import Annotated, Any, Dict, List, Optional

from pydantic import BaseModel, BeforeValidator, Field

UserId = Annotated[int, BeforeValidator(lambda v: str(v))]


class NutritionMacro(BaseModel):
    calories: float
    protein: float
    fat: float
    carb: float


class NutritionMicro(BaseModel):
    fa: float
    vc: float
    vd: float


class NutritionMineral(BaseModel):
    calcium: float
    iron: float
    zinc: float
    iodine: float


class DietarySummary(BaseModel):
    comment: Optional[str] = Field(default="", description="Comment for dietary")
    advice: Optional[str] = Field(default="", description="Advice for dietary")
    tables: Optional[List[Dict[str, Any]]] = Field(
        default=[], description="Tables for dietary"
    )
    charts: Optional[List[Dict[str, Any]]] = Field(
        default=[], description="Charts for dietary"
    )


class DietaryData(BaseModel):
    day: int
    meals: List[str]


class EmmaComment(BaseModel):
    summary: str
    advice: str = ""


class UserBasicInfo(BaseModel):
    user_id: UserId
    age: int
    pre_weight: float
    cur_weight: float
    height: float
    is_twins: bool = False
    glu: float
    hba1c: float
    bph: float
    bpl: float
    ga: int
    condition: str
    cond_level: int
    complications: str
    execise: int
    scripts: Optional[str] = Field(default=None, description="Prescribed scripts")
    advice: Optional[str] = Field(
        default=None, description="Doctor's advice for dietary"
    )


class UserPreferenceData(BaseModel):
    appetite: int = 0
    pork: int = 0
    beef: int = 0
    chicken: int = 0
    seafood: int = 0
    vegetable: int = 0
    fruit: int = 0
    milk: int = 0
    soymilk: int = 0
    dairy: int = 0
    grain: int = 0
    oil: int = 0
    salt: int = 0
    sugar: int = 0
    offal: int = 0
    rice: int = 0
    noodles: int = 0
    bread: int = 0
    nuts: int = 0
    prefer: str = ""
    dislike: str = ""
