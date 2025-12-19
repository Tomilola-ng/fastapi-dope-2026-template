"""Base Routes"""

from typing import Optional, List

from fastapi import (
    APIRouter,
    status,
    UploadFile,
    File,
    Form,
    Depends,
    Query,
)

from app.base.models import FileAsset
from app.base.schemas import FileOut
from app.config.storage import r2_storage
from app.config.settings import settings
from app.config.pagination import (
    PaginationParams,
    PaginatedResponse,
    get_pagination_params,
    PaginationHelper,
)

router = APIRouter(prefix="/base", tags=["Base"])


@router.post("/files", response_model=FileOut, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    alt_text: Optional[str] = Form(None),
    folder: str = Form("files"),
):
    """
    Upload an file to R2 storage and create an FileAsset record.

    - Accepts multipart form-data with `file` (UploadFile), optional `alt_text`, and optional `folder`.
    - Stores the file under `<folder>/<uuid>.<ext>` in R2.
    - Returns FileOut with a presigned preview URL (`url`).
    """
    # Upload to storage (returns the R2 key/path)
    key = await r2_storage.upload_file(file=file, folder=folder)

    # Compute file size (optional)
    try:
        content = await file.read()
        file_size = len(content) if content is not None else None
    finally:
        await file.seek(0)

    # Persist the file metadata
    file = await FileAsset.create(
        key=key,
        alt_text=alt_text,
        content_type=file.content_type,
        file_size=file_size,
    )

    # Return pydantic schema with presigned URL
    return FileOut.model_validate(file)


if settings.ENVIRONMENT == "local":
    @router.get(
        "/files",
        response_model=PaginatedResponse[FileOut],
        status_code=status.HTTP_200_OK,
    )
    async def list_files(
        pagination_params: PaginationParams = Depends(get_pagination_params),
        folder: Optional[str] = Query(
            None, description="Filter by folder prefix, e.g., 'files'"
        ),
    ):
        """
        List files with pagination. Each item includes a presigned `url` for preview.
        Optionally filter by `folder` (prefix).
        """
        queryset = FileAsset.all().order_by("-id")
        if folder:
            prefix = folder if folder.endswith("/") else f"{folder}/"
            queryset = queryset.filter(key__startswith=prefix)

        items, meta = await PaginationHelper.paginate_queryset(queryset, pagination_params)

        # Convert ORM objects to pydantic models (autogenerates url)
        out_items: List[FileOut] = [
            FileOut.model_validate(item) for item in items]

        return PaginationHelper.create_paginated_response(out_items, meta)
