from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, APIRouter
from fastapi.responses import FileResponse, JSONResponse

from app.config import settings


router = APIRouter()

# API-метод для получения конкретной фотографии по имени
@router.get("/files/{filename}", response_class=FileResponse, summary="Получить конкретную фотографию")
async def get_image(filename: str):
    """
    Возвращает конкретную фотографию по имени файла.
    """
    file_path = settings.MEDIA_ROOT / "files" / filename
    if not file_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Файл не найден")
    return FileResponse(file_path)  # Возвращаем файл как FileResponse