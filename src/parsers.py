from abc import ABC, abstractmethod
from .exceptions import CustomError
from . import errors
from .utils import createRange


class Parser(ABC):
    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def isValid(self):
        pass


class ExprParser(ABC):
    @abstractmethod
    def isValid(expr, sign):
        if sign in ["/", "-"]:
            if len(expr.split(sign)) != 2:
                return False
            firstPart, secondPart = expr.split(sign)
            if sign == "/":
                if firstPart != "*" and not firstPart.isnumeric():
                    return False
                if not secondPart.isnumeric():
                    return False
            else:
                if not firstPart.isnumeric() or not secondPart.isnumeric():
                    return False
        elif sign == ",":
            for num in expr.split(","):
                if not num.isnumeric():
                    return False
        elif sign == "*":
            if expr != "*":
                return False

        return True

    @abstractmethod
    def parse(expr, sign, low, up) -> str:
        if sign in ["/", "-"]:
            firstPart, secondPart = expr.split(sign)
            if sign == "/":
                start = low if firstPart == "*" else int(firstPart)
                step = int(secondPart)
                if start < low or start > up:
                    raise CustomError(errors.INVALID_EXPR_RANGE)
                result = ""
                for num in range(start, up + 1, 1):
                    if num % step != 0:
                        continue
                    result += f" {num}"
                return result
            else:
                start, end = int(firstPart), int(secondPart)
                if start > end:
                    raise CustomError(errors.INVALID_EXPR_RANGE)
                if start < low or end > up:
                    raise CustomError(errors.INVALID_TIME_FORMAT)
                return createRange(start, end, 1)
        elif sign == ",":
            result = ""
            for num in expr.split(","):
                if int(num) < low or int(num) > up:
                    raise CustomError(errors.INVALID_TIME_FORMAT)
                result += f" {num}"
            return result
        elif sign == "*":
            return createRange(low, up, 1)
        else:
            num = int(expr)
            if num < low or num > up:
                raise CustomError(errors.INVALID_TIME_FORMAT)
            return f" {expr}"


class TimeParser(ABC):
    def parse(expr, low, up) -> str:
        if expr.isnumeric():
            return ExprParser.parse(expr, "", low, up)

        for sign in ["/", "-", ",", "*"]:
            if sign not in expr:
                continue
            if not ExprParser.isValid(expr, sign):
                raise CustomError(errors.INVALID_EXPR_FORMAT)
            return ExprParser.parse(expr, sign, low, up)
