import logging


class Consts:
    LOGGER_NAME = "project_logger"
    LOGGER_FILE_NAME = LOGGER_NAME + ".log"
    LOG_FILE_DEBUG_LEVEL = logging.DEBUG
    CONSOLE_DEBUG_LEVEL = logging.INFO
    LOG_STACK = True
    MAX_LOG_STACK_SIZE = 12

    LOG_SIGNER_DEBUG = True
    LOG_DB_DEBUG = True
    LOG_DATA_PROCESSING_DEBUG = True
    LOG_JSON_RESULTS = True
    LOG_EXCLUDE_MODULES = []




