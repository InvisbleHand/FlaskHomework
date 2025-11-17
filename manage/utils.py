def alert_error(message):
    """通用错误提示函数"""
    return f"<script>alert('{message}'); window.history.back();</script>"