import re

from faststream import Logger
from faststream.nats import NatsRouter
from pydantic import BaseModel

from main import broker
from mistral_ai.gen.text import gpt_text

# router = NatsRouter()
