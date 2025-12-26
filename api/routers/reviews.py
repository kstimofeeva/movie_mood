from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from services.review_service import ReviewService
from schemas.review_schemas import ReviewCreate, Review
from api.dependencies import get_review_service

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=Review, status_code=201)
def create_review(review: ReviewCreate, review_service: ReviewService = Depends(get_review_service)):
    try:
        return review_service.create_review(review)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/movie/{movie_id}", response_model=List[Review])
def get_movie_reviews(movie_id: int, review_service: ReviewService = Depends(get_review_service)):
    return review_service.get_reviews_by_movie(movie_id)

@router.get("/{review_id}", response_model=Review)
def get_review(review_id: int, review_service: ReviewService = Depends(get_review_service)):
    review = review_service.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Не найден отзыв")
    return review

@router.delete("/{review_id}", status_code=204)
def delete_review(review_id: int, review_service: ReviewService = Depends(get_review_service)):
    success = review_service.delete_review(review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    return None

