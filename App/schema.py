from pydantic import BaseModel, EmailStr, Field
from typing import Deque, List, Optional, Tuple


class UserInput(BaseModel):
    customerCode : int
    customerPartNumber : int
    userText : str
    fallbackQuantity : int
    toUpdateArticles : int
    parallelConnections : Optional[int] = 1
    # tblCacheArticles : int
