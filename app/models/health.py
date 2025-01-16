from pydantic import BaseModel, ConfigDict

# Pydantic model for the item (Create and Update)
class HealthcheckBase(BaseModel):
    status: str
    project_info: dict[str, str]

# Pydantic model for item response (including id)
class Healthcheck(HealthcheckBase):

    model_config = ConfigDict(
        from_attributes=True
    )
