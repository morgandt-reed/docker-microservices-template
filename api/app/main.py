from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime

from . import models
from .config import get_settings
from .database import engine, get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Microservices Template API",
    description="Production-ready FastAPI service with PostgreSQL",
    version="1.0.0"
)

settings = get_settings()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True


# Health check endpoint
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for container orchestration
    """
    try:
        # Check database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "disconnected"

    return {
        "status": "healthy",
        "database": db_status,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat()
    }


# Prometheus metrics endpoint
@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint
    """
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from starlette.responses import Response

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


# CRUD endpoints
@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item in the database
    """
    try:
        db_item = models.Item(
            name=item.name,
            description=item.description
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        logger.info(f"Created item with id: {db_item.id}")
        return db_item
    except Exception as e:
        logger.error(f"Failed to create item: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create item")


@app.get("/items", response_model=List[ItemResponse])
async def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all items with pagination
    """
    try:
        items = db.query(models.Item).offset(skip).limit(limit).all()
        return items
    except Exception as e:
        logger.error(f"Failed to fetch items: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch items")


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific item by ID
    """
    try:
        item = db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch item")


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific item
    """
    try:
        item = db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        db.delete(item)
        db.commit()

        logger.info(f"Deleted item with id: {item_id}")
        return {"message": "Item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete item {item_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete item")


# Root endpoint
@app.get("/")
async def root():
    """
    API root endpoint
    """
    return {
        "message": "Docker Microservices Template API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting API in {settings.ENVIRONMENT} environment")
    logger.info(f"Database URL: {settings.DATABASE_URL.split('@')[1]}")  # Log without credentials


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down API")
