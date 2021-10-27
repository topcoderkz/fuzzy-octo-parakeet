def createRange(start, end, step):
    rangeOutput = ""
    for num in range(start, end + 1, step):
        rangeOutput += f" {num}"
    return rangeOutput
