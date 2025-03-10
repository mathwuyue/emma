from datetime import datetime
from typing import Any, Dict, List, Optional

from model.userinfo import BasicInfo, UserPreferenceData
from pydantic import BaseModel, Field


class CurrentWeight(BaseModel):
    weight: float = Field(..., description="Current weight")
    bmi: float = Field(..., description="BMI before pregancy")
    remark: Optional[str] = Field(None, description="Remark")
    timestamp: datetime = Field(..., description="Timestamp")
    exp_weight_min: float = Field(0, description="Expected weight min")
    exp_weight_max: float = Field(0, description="Expected weight max")
    exp_timestamp: datetime = Field(
        datetime(1970, 1, 1), description="exp weight timestamp"
    )


class GestationalWeek(BaseModel):
    gestational_week: int = Field(..., description="Gestational week")
    timestamp: datetime = Field(..., description="Timestamp")
    type: str = Field(..., description="0: LMP, 1: Ultrasound, 2: calculated")


class Complications(BaseModel):
    is_gestational_hypertension: bool = Field(
        ..., description="Gestational hypertension"
    )
    is_diabetes: bool = Field(..., description="Diabetes")
    is_multiple_pregnancy: bool = Field(..., description="Multiple pregnancy")
    is_retinopathy: bool = Field(..., description="Retinopathy")
    timestamp: datetime = Field(..., description="Timestamp")


class RecordFrequency(BaseModel):
    record_type: str = Field(..., description="record, food, exercise")
    remark: Optional[str] = Field(None, description="Remark")


class Period(BaseModel):
    lmp: str = Field(
        default="2021-01-01", description="Last menstrual period，末次月经第一天"
    )
    cycle: int = Field(default=28, description="月经周期")
    is_regular: bool = Field(default=True, description="月经是否规律")


class Preference(BaseModel):
    cuisine: List[str] = Field(default=["闽菜"], description="Cuisine")
    like: List[str] = Field(default=["海鲜"], description="Like")
    dislike: List[str] = Field(default=["水果"], description="Dislike")
    timestamp: datetime = Field(default=datetime.now(), description="Timestamp")


class HumanMeta(BaseModel):
    age: int = Field(default=25, description="Age")
    address: str = Field(default="上海市", description="Address")
    height: float = Field(default=1.77, description="Height in m")
    pre_weight: float = Field(default=59.3, description="Previous weight")
    bmi: float = Field(default=18.9, description="BMI before pregnancy")
    cur_weight: CurrentWeight = Field(default=59.3, description="Current weight")
    period: Period = Field(default=Period(), description="Period")
    gestational_week: GestationalWeek = Field(default=0, description="Gestational week")
    due_date: str = Field(default="2021-10-08", description="预产期")
    is_twins: bool = Field(default=False, description="是否为双胞胎")
    # exercise: int = Field(default=2, description="运动强度, 1-4")
    complications: Complications = Field(..., description="Complications")
    record_frequency: RecordFrequency = Field(..., description="Record frequency")
    food_frequency: RecordFrequency = Field(..., description="Food frequency")
    exercise_frequency: RecordFrequency = Field(..., description="Exercise frequency")
    preference: Preference = Field(..., description="Preference")


def set_humanmeta(
    human_meta: HumanMeta, datafield_or_dict: Any, value: Any = None
) -> HumanMeta:
    """Set fields in human meta

    Args:
        human_meta: HumanMeta object
        datafield_or_dict: Either a string field name or a dictionary of field-value pairs
        value: Value to set if datafield_or_dict is a string field name

    Returns:
        Updated HumanMeta object
    """
    if value is not None:
        # Case 1: Three arguments (field name and value)
        setattr(human_meta, datafield_or_dict, value)
    else:
        # Case 2: Two arguments (dict of field-value pairs)
        for field, val in datafield_or_dict.items():
            setattr(human_meta, field, val)
    return human_meta


# class HumanMeta:
#     def __init__(self, human_meta: str):
#         """Initialize with user_id"""
#         self.user_id = user_id

#     def get_all_meta(self) -> Dict[str, Any]:
#         """Aggregate all meta information into a dictionary"""
#         return {
#             "userinfo": self.get_userinfo(),
#             "meal_summary": self.get_meal_summary(),
#             "exercise_summary": self.get_exercise_summary(),
#             "food_preference": self.get_food_preference(),
#             "medical_records": self.get_medical_records(),
#         }

#     def get_userinfo(self) -> Optional[Dict[str, Any]]:
#         """Retrieve user information"""
#         pass

#     def get_meal_summary(self):
#         """Retrieve meal summary"""
#         # Implementation depends on how meal data is stored
#         # Placeholder implementation
#         return {"status": "not implemented"}

#     def get_exercise_summary(self) -> Optional[Dict[str, Any]]:
#         """Retrieve exercise summary"""
#         # Implementation depends on how exercise data is stored
#         # Placeholder implementation
#         return {"status": "not implemented"}

#     def get_food_preference(self) -> Optional[Dict[str, Any]]:
#         """Retrieve food preferences"""
#         pass

#     def get_medical_records(self):
#         """Retrieve medical records"""
#         # Implementation depends on how medical records are stored
#         # Placeholder implementation
#         return {"status": "not implemented"}
