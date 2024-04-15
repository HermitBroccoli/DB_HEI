from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import shutil
import os
import io

uploads = APIRouter()


# Папка для сохранения загруженных файлов
UPLOAD_DIRECTORY = "resources/img"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@uploads.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Получаем байты изображения
    contents = await file.read()

    # Сохраняем изображение в папку uploads
    filename = os.path.join(UPLOAD_DIRECTORY, 'building', file.filename)
    with open(filename, "wb") as f:
        f.write(contents)

    # Возвращаем название изображения в виде байтов
    return {"filename_bytes": str(file.filename).encode("utf-8")}
