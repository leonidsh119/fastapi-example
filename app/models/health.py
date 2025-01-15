from pydantic import BaseModel

# Pydantic model for the item (Create and Update)
class HealthcheckBase(BaseModel):
    status: str
    project_info: dict[str, str]

# Pydantic model for item response (including id)
class Healthcheck(HealthcheckBase):

    class Config:
        from_attributes = True
