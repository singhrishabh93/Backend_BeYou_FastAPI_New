from fastapi import APIRouter, HTTPException, status, Request
from typing import List
from app.models.affirmation import Affirmation, AffirmationCreate, AffirmationInDB
from app.database import db
from bson import ObjectId
from datetime import datetime
import logging
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/affirmations",
    tags=["affirmations"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Affirmation])
async def get_affirmations():
    try:
        affirmations = await db.affirmations.find().to_list(1000)
        return affirmations
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Database connection error. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )

@router.get("/{affirmation_id}", response_model=Affirmation)
async def get_affirmation(affirmation_id: str):
    try:
        affirmation = await db.affirmations.find_one({"id": affirmation_id})
        if affirmation is None:
            raise HTTPException(status_code=404, detail="Affirmation not found")
        return affirmation
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Database connection error. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )

@router.post("/", response_model=Affirmation, status_code=status.HTTP_201_CREATED)
async def create_affirmation(affirmation: AffirmationCreate):
    try:
        new_affirmation = AffirmationInDB(
            text=affirmation.text,
            category=affirmation.category
        )
        
        affirmation_dict = new_affirmation.model_dump()
        result = await db.affirmations.insert_one(affirmation_dict)
        
        created_affirmation = await db.affirmations.find_one({"_id": result.inserted_id})
        return created_affirmation
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Database connection error. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )

@router.delete("/{affirmation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_affirmation(affirmation_id: str):
    """Delete an affirmation by ID"""
    try:
        # Check if affirmation exists
        existing_affirmation = await db.affirmations.find_one({"id": affirmation_id})
        if existing_affirmation is None:
            raise HTTPException(status_code=404, detail="Affirmation not found")
        
        # Delete the affirmation
        result = await db.affirmations.delete_one({"id": affirmation_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Affirmation not found")
            
        return {"message": "Affirmation deleted successfully"}
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Database connection error. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )