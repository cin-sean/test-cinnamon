from typing import List, Dict, Any, Tuple, IO

from pydantic import BaseModel, Field

class InferResponse(BaseModel):
    task_id: str = ""

class InferTaskResponse(BaseModel):
    job_id: str = ""
    error_code: str = ""
    error_message: str = ""
    result: List[Dict[str, Any]]
    result_by_file: Dict[str, Any] = Field(default_factory=dict, description="File level result")

