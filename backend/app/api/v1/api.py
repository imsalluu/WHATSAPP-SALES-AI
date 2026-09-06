from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.organizations import router as org_router
from app.api.v1.products import router as products_router
from app.api.v1.orders import router as orders_router
from app.api.v1.conversations import router as conv_router
from app.api.v1.leads import router as leads_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.agent_config import router as agent_router
from app.api.v1.whatsapp import router as wa_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.ws import router as ws_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(org_router)
api_router.include_router(products_router)
api_router.include_router(orders_router)
api_router.include_router(conv_router)
api_router.include_router(leads_router)
api_router.include_router(knowledge_router)
api_router.include_router(agent_router)
api_router.include_router(wa_router)
api_router.include_router(analytics_router)
api_router.include_router(ws_router)
