from app.tasks.celery import celery

from PIL import Image
from pathlib import Path

from app.tasks.email_tenplates import create_register_email

@celery.task
def process_picture(
        path: str
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f"app/static/images/im_resized_1000_500_{im_path.name}")
    im_resized_200_100.save(f"app/static/images/im_resized_200_100_{im_path.name}")


@celery.task
def send_register_email(
        data: dict,
        email_to: str,
):
    msg_content = create_register_email(data, email_to)