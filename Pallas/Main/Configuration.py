from argparse import ArgumentParser
import logging
import os

from Main.singleton import singleton


@singleton
class Configuration(object):

    def __init__(self, args=None):
        cli_parser = ArgumentParser()
        group = cli_parser.add_argument_group()
        group.add_argument("-v", "--log-level", help="Log level", type=str, default="INFO")
        group.add_argument("-t", "--target", help="Log level", type=str, default="http://localhost/")
        group.add_argument("-b", "--browser", help="Browser used to explore", type=str, default="PhantomJS")
        group.add_argument("--proxy-path", help="Path to browsermob proxy executable", type=str, default=None)
        group.add_argument("--auto", help="Launch automated analysis", default=False, action='store_true')
        group.add_argument("--env", help="Read environment variable", default=False, action='store_true')
        cli_args = cli_parser.parse_args(args)

        self._log_level = cli_args.log_level
        self._target = cli_args.target
        self._browser = 'PhantomJS'
        if cli_args.browser in ['PhantomJS', 'Firefox']:
            self._browser = cli_args.browser
        self._proxy_path = cli_args.proxy_path
        if cli_args.env:
            self._proxy_path = os.getenv('BROWSERMOB_PROXY_PATH', self._proxy_path)
        self._auto = cli_args.auto

    @property
    def auto(self):
        return self._auto

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
    @proxy_path.setter
    def proxy_path(self, value):
        self._proxy_path = value

    @property
    def target(self):
        return self._target

    @property
    def browser(self):
        return self._browser
    @browser.setter
    def browser(self, value):
        if value not in ['PhantomJS', 'Firefox', 'Dummy']:
            logging.warning('Browser not known : %s' % value)
        else:
            self._browser = value
