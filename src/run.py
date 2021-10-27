from src.parsers import TimeParser
from src.constants import timeRanges, timeKeys, tableFieldNameLength


def makeOutput(exprs: list) -> dict:
    result = {}
    for key, expr in zip(timeKeys, exprs):
        result[key] = TimeParser.parse(
            expr, timeRanges[key][0], timeRanges[key][1]
        )[1:]

    result["command"] = exprs[5]
    return result


def formatOutput(output: dict) -> str:
    result = ""
    for key in output:
        line = f"{key.ljust(tableFieldNameLength)} {output[key]}"
        result += f"{line}\n"
    return result
