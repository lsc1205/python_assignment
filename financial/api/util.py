from functools import wraps
import traceback

def response_decorator(func):
    """
    Error handling decorator to handle any api exception.
    If an error occurs, an error message will be automatically added.
    """
    @wraps(func)
    def real_decorator(*args, **kwargs):
        result = {}
        try:
            result = func(*args, **kwargs)
            if "info" not in result:
                result["info"] = {"error": ""}
        except Exception as e:
            result["info"] = {
                "error": f"Exception: {e}"
            }
            traceback.print_exc()

        return result
    
    return real_decorator