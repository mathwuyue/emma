from typing import Dict, Any, Optional, List
from datetime import datetime

from model.userinfo import BasicInfo, UserPreferenceData
from pydantic import BaseModel, Field


class CurrentWeight(BaseModel):
    weight: float = Field(..., description="Current weight")
    bmi: float = Field(..., description="BMI")
    remark: Optional[str] = Field(None, description="Remark")
    timestamp: datetime = Field(..., description="Timestamp")


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


class RecordFrequency(BaseModel):
    record_type: str = Field(..., description="record, food, exercise")
    remark: Optional[str] = Field(None, description="Remark")


class HumanMeta(BaseModel):
    pre_weight: float = Field(None, description="Previous weight")
    cur_weight: CurrentWeight = Field(..., description="Current weight")
    gestational_week: GestationalWeek = Field(..., description="Gestational week")
    complications: Complications = Field(..., description="Complications")
    record_frequency: RecordFrequency = Field(..., description="Record frequency")
    food_frequency: RecordFrequency = Field(..., description="Food frequency")
    exercise_frequency: RecordFrequency = Field(..., description="Exercise frequency")


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
