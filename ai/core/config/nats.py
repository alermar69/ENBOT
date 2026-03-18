from pydantic import BaseModel


class NatsConfig(BaseModel):
    url: str = "nats://localhost:4222"
