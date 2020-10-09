import logging
logger = logging.getLogger(__name__)

# Decorator for functions that doesn't return anything
def prevent_exception(f):
    def no_exception_f(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Encoutered error while processing {f.__name__}, {e}")

    return no_exception_f