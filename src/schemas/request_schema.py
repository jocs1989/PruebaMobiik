from pydantic import BaseModel
from typing import List, Optional




class CreateModelRequest(BaseModel):
    # Siempre obligatorios
    model_name: Optional[str] = None
    description: Optional[str] = None
    model_class: List[str] = ["Lineal"]

