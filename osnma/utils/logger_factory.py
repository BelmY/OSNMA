#
# Copyright © European Union 2022
#
# Licensed under the EUPL, Version 1.2 or – as soon they will be approved by
# the European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations under the Licence.
#

import logging
import os
from datetime import datetime

from osnma.utils.config import Config

str_to_log_level = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors. Thanks to Sergey Pleshakov"""

    grey = "\x1b[1m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[30;41m"
    reset = "\x1b[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "%(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def configure_loggers():
    """
    From each file we are getting the logger using __name__. Therefore, all of them share the parent logger 'osnma' and
    propagate to this parent logger. We can set the appropriate handlers here and let the library do the rest.
    """
    logger = logging.getLogger('osnma')

    # Clear all handlers (multiple executions would just add infinite loggers)
    # DO NOT use logger.hasHandlers() because it also checks parents and pytest adds a logger to root
    while len(logger.handlers) > 0:
        logger.removeHandler(logger.handlers[0])

    # Disable the call to logging.lastresort when no handler is found
    logger.addHandler(logging.NullHandler())

    # File Handler
    if Config.LOG_FILE:
        now = datetime.now()
        file_path = Config.LOGS_PATH / f'logs_{now.strftime("%Y%m%d_%H%M%S%f")}'
        os.makedirs(file_path)
        file_name = file_path / 'general_logs.log'

        f_handler = logging.FileHandler(file_name, mode='w')
        f_handler.setLevel(Config.FILE_LOG_LEVEL)
        # f_format = logging.Formatter('%(asctime)s | %(name)-35s | %(levelname)-8s | %(message)s')
        f_format = logging.Formatter('%(name)-35s | %(levelname)-8s | %(message)s')

        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    # Console Handler
    if Config.LOG_CONSOLE:
        c_handler = logging.StreamHandler()
        c_handler.setLevel(Config.CONSOLE_LOG_LEVEL)
        c_handler.setFormatter(CustomFormatter())

        logger.addHandler(c_handler)


def get_logger(name):
    # By default, the log level is Warning. We could use this function to change specifics to file
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger
