from typing import Union
from pydantic import BaseModel, Field
from typing_extensions import Annotated

class Main_User(BaseModel):
    name: Union[str, None] = None
    id: Annotated[Union[int, None], Field(default = 100, ge = 1, it = 200)] = None

class Main_UserDB(Main_User):
    password: Annotated[Union[str, None], Field(max_length = 200, min_length = 8)] = None

class New_Response(BaseModel):
    message: str