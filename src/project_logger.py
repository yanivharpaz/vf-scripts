import logging
import time
import os
import sys
import json
import socket
import inspect
import platform

from consts import Consts
from singleton_base import Singleton


class ProjectLogger(Singleton):
    logger = None

    def __init__(self, log_level=Consts.LOG_FILE_DEBUG_LEVEL, name=None, stack_list=None) -> None:
        if self.logger is None:
            # self.iStartTime = None
            self.start_time = None
            self.create(log_level, name)
            if stack_list is not None:
                self.logger.debug(self.format_stack_list(stack_list))

    def create(self, log_level, name):
        # self.iStartTime = time.time()
        self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.DEBUG)
        # self.logger.addHandler(logging.StreamHandler())
        # self.logger.info(f'Started ProjectLogger')
        self.start_time = time.time()
        self.logger = logging.getLogger(name or Consts.LOGGER_NAME)

        if log_level is not None:
            self.logger.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s |%(message)s', "%Y-%m-%d %H:%M:%S")

            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(formatter)
            stdout_handler.setLevel(Consts.CONSOLE_DEBUG_LEVEL)

            log_file_handler = logging.FileHandler(self.get_script_directory() + '/../' + Consts.LOGGER_FILE_NAME)
            log_file_handler.setFormatter(formatter)
            log_file_handler.setLevel(log_level)

            # self.logger.addHandler(stdout_handler)
            self.logger.addHandler(log_file_handler)
        self.logger.info("Platform : " + str(platform.uname()))
        self.logger.info("Version  : " + str(sys.version_info))
        self.logger.info(f"{Consts.LOG_EXCLUDE_MODULES}")

    @staticmethod
    def print_stack(stack_list, max_stack_size=Consts.MAX_LOG_STACK_SIZE):
        if Consts.LOG_STACK and stack_list is not None and len(stack_list) > 0:
            list_to_show = stack_list[:min(max_stack_size, len(stack_list))]

            ProjectLogger.debug(ProjectLogger.format_stack_list())

    @staticmethod
    def get_script_directory():
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def get_ip():
        return socket.gethostbyname(socket.gethostname())

    # @staticmethod
    # def time_from_start(self):
    #     return time.time() - self.iStartTime

    @staticmethod
    def get_stack_list():
        return inspect.stack()

    @staticmethod
    def get_stack_modules():
        return [stack_item[3] for stack_item in inspect.stack()]

    @staticmethod
    def format_stack_list():
        modules = ProjectLogger.get_stack_modules()
        return f'Stack[{len(modules)}]: {str(" <|".join(modules))}'

    @staticmethod
    def build_logging_message(message, project_logger, print_module, print_stack, stack_list):
        if print_stack:
            project_logger.print_stack(stack_list)
        if print_module:
            module = inspect.getmodule(inspect.stack()[1][0])
            message = f'{module}|{message}'
        return message

    @staticmethod
    def info(message, print_stack=False, stack_list=None, print_module=False):
        stack_modules = ProjectLogger.get_stack_modules()
        if ProjectLogger.if_any(stack_modules, Consts.LOG_EXCLUDE_MODULES):
            return None

        project_logger = ProjectLogger(name="project_logger")
        message = ProjectLogger.build_logging_message(message, project_logger, print_module, print_stack, stack_list)
        project_logger.logger.info(message)

    @staticmethod
    def if_any(first_list, second_list):
        for item in first_list:
            if item in second_list:
                return True
        return False

    @staticmethod
    def debug(message, print_stack=False, stack_list=None, print_module=False):
        stack_modules = ProjectLogger.get_stack_modules()
        if ProjectLogger.if_any(stack_modules, Consts.LOG_EXCLUDE_MODULES):
            return None

        project_logger = ProjectLogger(name="project_logger")
        message = ProjectLogger.build_logging_message(message, project_logger, print_module, print_stack, stack_list)
        if print_stack:
            project_logger.logger.debug(ProjectLogger.format_stack_list())
        project_logger.logger.debug(message)

    @staticmethod
    def dict_to_str_list(input_dict):
        return json.dumps(input_dict, indent=4).split('\n')

    @staticmethod
    def dictionary_debug(input_dict, message='', print_stack=False, stack_list=None, print_module=False):
        stack_modules = ProjectLogger.get_stack_modules()
        if ProjectLogger.if_any(stack_modules, Consts.LOG_EXCLUDE_MODULES):
            return None

        if not Consts.LOG_JSON_RESULTS:
            return None

        str_lines = ProjectLogger.dict_to_str_list(input_dict)

        project_logger = ProjectLogger(name="project_logger")
        if print_stack:
            project_logger.logger.debug(ProjectLogger.format_stack_list())
        project_logger.logger.debug(f"{message} | {len(input_dict)} | number of : -> {str(str_lines).count(':')} json:")
        for line in str_lines:
            project_logger.logger.debug(line)

    @staticmethod
    def error(message, print_stack=False, stack_list=None, print_module=False):
        project_logger = ProjectLogger(name="project_logger")
        message = ProjectLogger.build_logging_message(message, project_logger, print_module, print_stack, stack_list)
        project_logger.logger.error(message)

    @staticmethod
    def critical(message, print_stack=False, stack_list=None, print_module=False):
        project_logger = ProjectLogger(name="project_logger")
        message = ProjectLogger.build_logging_message(message, project_logger, print_module, print_stack, stack_list)
        project_logger.logger.critical(message)



