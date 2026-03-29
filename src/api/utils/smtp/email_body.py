def email_body(confirm_code: str) -> str:
    body = f"""
    To change your password, we have generated a confirm_code for you: {confirm_code}
    """
    return body
