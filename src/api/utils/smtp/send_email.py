from src.api.utils.smtp.task import send_email


def send_newletters_task():
    send_email.delay()
