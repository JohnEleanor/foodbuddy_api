from pydantic import BaseModel

class LineMessage(BaseModel):
    message: str