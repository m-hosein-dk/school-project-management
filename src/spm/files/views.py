import mimetypes
from fastapi import APIRouter, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from spm.core import DbSession
from . import service as files_service

router = APIRouter()

@router.post("/")
def post_file(
    file: UploadFile,
    project_id: int,
    session: DbSession
):
    files_service.store_file(
        file_name=file.filename or "",
        file=file.file.read(),
        project_id=project_id,
        session=session
    )


@router.get("/{file_id}")
async def view_file(
    file_id: int,
    session: DbSession
):
    file_info = files_service.get_file_by_id(file_id, session)

    if not file_info:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "file with this id not found"
        )

    return FileResponse(
        path=file_info.path,
        media_type=file_info.mime_type,
        headers={"Content-Disposition": "inline"}
    )

@router.get("/{file_id}/info")
def get_file_info(
    file_id: int,
    session: DbSession
):
    return files_service.get_file_by_id(file_id, session)