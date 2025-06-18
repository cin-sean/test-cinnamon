from typing import Any, Dict, List

from pydantic import BaseModel, Field


class InferResponse(BaseModel):
    task_id: str = ""


class InferTaskResponse(BaseModel):
    job_id: str = ""
    error_code: str = ""
    error_message: str = ""
    result: List[Dict[str, Any]] = Field(
        default_factory=list, description="List of result items"
    )
    result_by_file: Dict[str, Any] = Field(
        default_factory=dict, description="File-level result mapping"
    )
