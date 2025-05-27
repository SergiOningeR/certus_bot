from .user_handlers import user_router
from .admin_handlers import admin_router
from .common_handlers import common_router

__all__ = ["user_router", "admin_router", "common_router"]