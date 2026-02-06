import os
from typing import Literal
import random
import mimetypes
from spm.config import FILES_PATH
from sqlalchemy.orm import Session
from .models import (
    File,
    FileOut
)

def store_file(
    file_name: str,
    file: bytes,
    project_id: int,
    session: Session
):
    random_id = random.randint(1*10**6, (1*10**7)-1) # six digit number
    path = os.path.join(
        FILES_PATH, 
        f"{project_id}"
        "_"
        f"{random_id}"
        "_"
        f"{file_name}"
    )
    file_object = File(
        id=random_id, # 🙏
        project_id=project_id,
        path=path,
        file_name=file_name
    )
    session.add(file_object)

    open(
        path,
        "wb"
    ).write(file)

    return random_id

def get_file_by_id(
    file_id:int,
    session: Session
) -> FileOut | None:
    file_object = session.query(File).filter(
        File.id == file_id
    ).one_or_none()
    if not file_object: return

    try:
        file = open(file_object.path, "rb")
    except FileNotFoundError:
        return

    mime_type, _ = mimetypes.guess_type(file_object.path)

    return FileOut(
        file_name=file_object.file_name,
        file_size=os.path.getsize(file_object.path),
        project_id=file_object.project_id,
        mime_type=mime_type or "application/octet-stream",
        path= file_object.path
    )

def is_uploadable(
    file_size: int,
    file_name: str,
    allowed_extentions: Literal["*"] | list[str] = "*"
) -> bool:
    if allowed_extentions == "*":
        return True
    
    extention = file_name.rsplit(".", 2)[1]

    if extention.lower() in map(lambda x: x.lower() ,allowed_extentions):
        return True
    
    return False