from fastapi import FastAPI
from api.v1.endpoints import items
from core.config import settings
from db.session import engine
from models import item as item_model

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Create database tables
item_model.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(items.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
