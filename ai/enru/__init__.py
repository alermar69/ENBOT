from faststream.nats import NatsRouter

from .sentences import router as router_sentences
from .words import router as router_words

router = NatsRouter()

router.include_router(router_sentences)
router.include_router(router_words)
