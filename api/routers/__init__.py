from .movies import router as movies_router
from .reviews import router as reviews_router
from recommendations import router as recommendations_router

__all__ = ['movies_router', 'reviews_router', 'recommendations_router']