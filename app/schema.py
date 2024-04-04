from pydantic import BaseModel, EmailStr, Field
from typing import Deque, List, Optional, Tuple


class UserInput(BaseModel):
    customerCode: str
    userPassword: str
    customerPartNumber: Optional[str] = "No text"
    userText: Optional[str] = "No text"
    fallbackQuantity: Optional[int] = 1
    toUpdateArticles: Optional[int] = 10000
    parallelConnections: Optional[int] = 1
