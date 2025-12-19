"""Pagination module for consistent pagination across endpoints"""

from math import ceil
from typing import Generic, TypeVar, List, Optional, Any

from pydantic import BaseModel, Field, validator
from fastapi import Query
from tortoise.queryset import QuerySet

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters for requests"""

    page: int = Field(default=1, ge=1, description="Page number (1-based)")
    page_size: int = Field(
        default=20, ge=1, le=100, description="Number of items per page"
    )

    @validator("page_size")
    def validate_page_size(cls, v):
        if v > 100:
            raise ValueError("Page size cannot exceed 100")
        return v

    @property
    def offset(self) -> int:
        """Calculate offset for database queries"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit for database queries"""
        return self.page_size


class PaginationMeta(BaseModel):
    """Pagination metadata for responses"""

    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of items per page")
    total_items: int = Field(description="Total number of items")
    total_pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_previous: bool = Field(description="Whether there is a previous page")
    next_page: Optional[int] = Field(
        description="Next page number if available")
    previous_page: Optional[int] = Field(
        description="Previous page number if available"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""

    items: List[T] = Field(description="List of items for current page")
    meta: PaginationMeta = Field(description="Pagination metadata")


class PaginationHelper:
    """Helper class for pagination operations"""

    @staticmethod
    def create_meta(page: int, page_size: int, total_items: int) -> PaginationMeta:
        """Create pagination metadata"""
        total_pages = ceil(total_items / page_size) if total_items > 0 else 0
        has_next = page < total_pages
        has_previous = page > 1

        return PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous,
            next_page=page + 1 if has_next else None,
            previous_page=page - 1 if has_previous else None,
        )

    @staticmethod
    async def paginate_queryset(
        queryset: QuerySet, pagination_params: PaginationParams
    ) -> tuple[List[Any], PaginationMeta]:
        """
        Paginate a Tortoise ORM queryset

        Args:
            queryset: The queryset to paginate
            pagination_params: Pagination parameters

        Returns:
            Tuple of (items, pagination_meta)
        """
        # Get total count
        total_items = await queryset.count()

        # Apply pagination to queryset
        items = await queryset.offset(pagination_params.offset).limit(
            pagination_params.limit
        )

        # Create pagination metadata
        meta = PaginationHelper.create_meta(
            page=pagination_params.page,
            page_size=pagination_params.page_size,
            total_items=total_items,
        )

        return items, meta

    @staticmethod
    def create_paginated_response(
        items: List[T], meta: PaginationMeta
    ) -> PaginatedResponse[T]:
        """Create a paginated response"""
        return PaginatedResponse(items=items, meta=meta)


# Convenience function for common pagination workflow
async def paginate(
    queryset: QuerySet, pagination_params: PaginationParams
) -> PaginatedResponse:
    """
    Convenience function to paginate a queryset and return a paginated response

    Args:
        queryset: The queryset to paginate
        pagination_params: Pagination parameters

    Returns:
        PaginatedResponse with items and metadata
    """
    items, meta = await PaginationHelper.paginate_queryset(queryset, pagination_params)
    return PaginationHelper.create_paginated_response(items, meta)


# Common pagination parameters dependency
def get_pagination_params(
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(
        default=20, ge=1, le=100, description="Number of items per page"
    ),
) -> PaginationParams:
    """FastAPI dependency for pagination parameters"""
    return PaginationParams(page=page, page_size=page_size)
