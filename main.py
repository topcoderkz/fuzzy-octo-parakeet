import sys
from src.exceptions import CustomError
from src import errors
from src.run import formatOutput, makeOutput


def main(cronExpr: str) -> None:
    exprs = cronExpr.split()
    if len(exprs) != 6:
        raise CustomError(errors.INVALID_LENGTH_CRON_EXPR)

    print(formatOutput(makeOutput(exprs)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise CustomError(errors.INVALID_NUMBER_OF_ARG)
    main(sys.argv[1])
