from pydantic import BaseModel


class CacheNamespace(BaseModel):
    users_list: str = "users-list"


class CacheConfig(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()
