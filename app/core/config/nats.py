from pydantic import BaseModel


class NatsConfig(BaseModel):
    server: str = "nats://localhost:4222"