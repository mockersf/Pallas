from argparse import ArgumentParser
import logging

from singleton import singleton


@singleton
class Configuration(object):

    def __init__(self):
        cli_parser = ArgumentParser()
        group = cli_parser.add_argument_group()
        group.add_argument("-v", "--log-level", help="Log level", type=str, default="INFO")
        group.add_argument("-t", "--target", help="Log level", type=str, default="http://github.com/")
        group.add_argument("--proxy-path", help="Path to browsermob proxy executable", type=str, default=None)
        cli_args = cli_parser.parse_args()

        self._log_level = cli_args.log_level
        self._target = cli_args.target
        self._proxy_path = cli_args.proxy_path

    @property
    def log_level(self):
        return self._log_level

    def get_log_level(self):
        if self._log_level == "INFO":
            return logging.INFO
        if self._log_level == "DEBUG":
            return logging.DEBUG
        if self._log_level == "WARNING":
            return logging.WARNING
        if self._log_level == "ERROR":
            return logging.ERROR
        if self._log_level == "CRITICAL":
            return logging.CRITICAL
        return logging.FATAL

    @property
    def proxy_path(self):
        return self._proxy_path

    @property
    def target(self):
        return self._target
