from pydantic import BaseModel

class IntegrateCms(BaseModel):
    id: int
    name: str