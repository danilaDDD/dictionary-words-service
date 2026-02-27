from typing import List

from fastapi import APIRouter, Depends, Response, HTTPException
from starlette.status import HTTP_201_CREATED

from app.schemas.requests import CreateWordRequest, UpdateWordRequest
from app.schemas.responses import WordResponseEntity
from app.services.rest_word_service import RestWordService, get_rest_word_service

word_router = APIRouter(
    prefix="/words",
    tags=["words"],
)

@word_router.post("/",
                  responses={
                      HTTP_201_CREATED:{
                          "model": WordResponseEntity,
                          "description": "Word created successfully."
                      }
                  })
async def create_word(
        request: CreateWordRequest,
        response: Response,
        rest_word_service: RestWordService = Depends(get_rest_word_service),
) -> WordResponseEntity:

    response.status_code = HTTP_201_CREATED
    return await rest_word_service.create_chat(request)

@word_router.put("/{id}/",
                 responses={
                     200: {
                         "model": WordResponseEntity,
                         "description": "Word updated successfully."
                     },
                 })
async def update_word(
        id: str,
        request: UpdateWordRequest,
        rest_word_service: RestWordService = Depends(get_rest_word_service),
) -> WordResponseEntity:
    return await rest_word_service.update_word(request)

@word_router.get("/",
                 responses={
                     200: {
                         "model": List[WordResponseEntity],
                         "description": "List of words retrieved successfully."
                     },
                 })
async def get_words(rest_word_service: RestWordService = Depends(get_rest_word_service)) -> List[WordResponseEntity]:
    return await rest_word_service.get_words()

@word_router.get("/{id}/",
                    responses={
                        200: {
                            "model": WordResponseEntity,
                            "description": "Word retrieved successfully."
                        },
                    })
async def get_word_by_id(id: str, rest_word_service: RestWordService = Depends(get_rest_word_service)) -> WordResponseEntity:
    return await rest_word_service.get_word_by_id(id)


@word_router.delete("/{id}/",
                    responses={
                        200: {
                            "model": WordResponseEntity,
                            "description": "Word deleted successfully"
                        },
                    })
async def delete_word(id: str, rest_word_service: RestWordService = Depends(get_rest_word_service)) -> WordResponseEntity:
    return await rest_word_service.delete_word(id)

