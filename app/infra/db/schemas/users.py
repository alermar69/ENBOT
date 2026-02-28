from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    telegram_id: int
    lang: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)

