import abc
from abc import abstractmethod


class Logger(abc.ABC):

    @abstractmethod
    def trace(self, msg):
        pass

    @abstractmethod
    def debug(self, msg):
        pass

    @abstractmethod
    def info(self, msg):
        pass

    @abstractmethod
    def warning(self, msg):
        pass

    @abstractmethod
    def error(self, msg):
        pass

    @abstractmethod
    def exception(self, msg):
        pass

    @abstractmethod
    def critical(self, msg):
        pass
