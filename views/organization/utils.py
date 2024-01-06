import os
import uuid

from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from config import ORG_FILES_PATH


def del_exists_file(content_type, full_image_path, path_image_dir, inn=None, worker_id=None):
    if inn:
        if content_type == "image/png":
            if os.path.isfile(f'{path_image_dir}{inn}.jpeg'):
                os.remove(f'{full_image_path}.jpeg')
        else:
            if os.path.isfile(f'{path_image_dir}{inn}.png'):
                os.remove(f'{full_image_path}.png')
    else:
        if content_type == "image/png":
            if os.path.isfile(f'{path_image_dir}{worker_id}.jpeg'):
                os.remove(f'{full_image_path}.jpeg')
        else:
            if os.path.isfile(f'{path_image_dir}{worker_id}.png'):
                os.remove(f'{full_image_path}.png')


def upload_photos(file: UploadFile, image_path: str, inn: str = None, worker_id: uuid.UUID = None):
    file_size = file.size
    content_type = file.content_type

    if file_size > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    if content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    cwd = os.getcwd()
    path_image_dir = image_path

    if not os.path.exists(path_image_dir):
        os.mkdir(path_image_dir)

    if not worker_id:
        full_image_path = os.path.join(cwd, path_image_dir, inn)
        file_name = f'{path_image_dir}{inn}.{content_type[6:]}'
        del_exists_file(content_type=content_type, inn=inn, path_image_dir=image_path, full_image_path=full_image_path)

    else:
        full_image_path = f"{os.path.join(cwd, path_image_dir)}/{worker_id}"
        file_name = f'{path_image_dir}{worker_id}.{content_type[6:]}'
        del_exists_file(content_type=content_type, worker_id=worker_id, path_image_dir=image_path,
                        full_image_path=full_image_path)

    with open(file_name, 'wb+') as f:
        f.write(file.file.read())
        f.flush()
        f.close()

    return file_name


def validate_organization_inn(inn: str):
    if not inn.isdigit() or len(inn) != 10:
        raise HTTPException(status_code=400, detail="invalid inn")

    coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8]
    control_sum = sum([int(inn[i]) * coefficients[i] for i in range(9)]) % 11 % 10

    if str(control_sum) != inn[9]:
        raise HTTPException(status_code=400, detail="invalid inn")

    return inn


def upload_files(file: UploadFile, inn: str):
    cwd = os.getcwd()
    path_image_dir = ORG_FILES_PATH
    full_image_path = os.path.join(cwd, path_image_dir, inn)
    file_name = f"{path_image_dir}/{inn}/{file.filename}"
    content_type = file.content_type
    file_size = file.size

    if file_size > 3 * 1024 * 1024:  # 3mb
        raise HTTPException(status_code=400, detail="File too large")

    if content_type not in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            "image/jpeg",
                            "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    if not os.path.exists(full_image_path):
        os.mkdir(full_image_path)

    with open(file_name, 'wb+') as f:
        f.write(file.file.read())
        f.flush()
        f.close()

    return file_name
