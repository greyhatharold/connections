import os
import logging
from logging.handlers import RotatingFileHandler
import structlog
from colorama import init, Fore
import functools
import traceback
import sys
import weakref

# Initialize colorama for cross-platform color support
init()

class Logger:
    _instances = weakref.WeakValueDictionary()

    @classmethod
    def get_instance(cls, name, log_folder='logs', max_size=10*1024*1024, backup_count=5):
        if name not in cls._instances:
            instance = cls(name, log_folder, max_size, backup_count)
            cls._instances[name] = instance
        return cls._instances[name]

    def __init__(self, name, log_folder='logs', max_size=10*1024*1024, backup_count=5):
        self.logger = self._setup_logger(name, log_folder, max_size, backup_count)
        self.structured_logger = self._setup_structlog()

    def _setup_logger(self, name, log_folder, max_size, backup_count):
        os.makedirs(log_folder, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            os.path.join(log_folder, f'{name}.log'),
            maxBytes=max_size,
            backupCount=backup_count
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter())

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger

    def _setup_structlog(self):
        return structlog.wrap_logger(
            self.logger,
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.stdlib.render_to_log_kwargs,
            ],
        )

    def info(self, message, **kwargs):
        self.structured_logger.info(message, **kwargs)

    def error(self, message, **kwargs):
        self.structured_logger.error(message, **kwargs)

    def warning(self, message, **kwargs):
        self.structured_logger.warning(message, **kwargs)

    def debug(self, message, **kwargs):
        self.structured_logger.debug(message, **kwargs)

    def critical(self, message, **kwargs):
        self.structured_logger.critical(message, **kwargs)
        self._handle_critical_error(message, **kwargs)

    def _handle_critical_error(self, message, **kwargs):
        error_msg = f"CRITICAL ERROR: {message}"
        if 'exc_info' in kwargs:
            error_msg += f"\n{''.join(traceback.format_exception(*kwargs['exc_info']))}"
        print(f"{Fore.RED}{Fore.BRIGHT}{error_msg}{Fore.RESET}", file=sys.stderr)

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Fore.BRIGHT
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, Fore.RESET)}{log_message}{Fore.RESET}"

def get_logger(name, log_folder='logs'):
    return Logger.get_instance(name, log_folder)

def set_log_level(logger, level):
    logger.logger.setLevel(level)

def log_function_call(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Calling {func.__name__}", args=args, kwargs=kwargs)
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} completed successfully", result=result)
                return result
            except Exception as e:
                logger.critical(f"Critical error in {func.__name__}", exc_info=sys.exc_info())
                raise
        return wrapper
    return decorator

def get_logger_for_file(file_name, log_folder='logs'):
    return Logger.get_instance(os.path.splitext(os.path.basename(file_name))[0], log_folder)

# Example usage
if __name__ == "__main__":
    main_logger = get_logger("main")
    db_logger = get_logger("database")
    current_file_logger = get_logger_for_file(__file__)

    main_logger.info("Application started")
    db_logger.info("Database connection established")
    current_file_logger.info("This log entry is specific to the current file")