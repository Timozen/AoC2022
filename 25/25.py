__all__ = ["Snafu"]

import pathlib

class Snafu:
    # SNAFU is number system with base of 5
    # and the digits are 2, 1, 0, -, =
    # and - means -1, and = means -2

    MAP = {
        "0": 0,
        "1": 1,
        "2": 2,
        "-": -1,
        "=": -2,
    }
    @staticmethod
    def to_decimal(value: str) -> int:
        out_value = 0
        for idx, char in enumerate(reversed(value)):
            out_value += Snafu.MAP[char] * 5 ** idx
        return out_value
    
    @staticmethod
    def to_snafu(value: int) -> str:
        if value == 0:
            return "0"
        out_value = []
        while value:
            remainder = value % 5
            if remainder == 4:
                out_value.append("-")
                value += 1
            elif remainder == 3:
                out_value.append("=")
                value += 2
            else:
                out_value.append(str(remainder))
            value //= 5
        return "".join(reversed(out_value))
    
lines = pathlib.Path("input.txt").read_text().splitlines()
sum_snafu = sum(Snafu.to_decimal(line) for line in lines)
print("Task 1:", Snafu.to_snafu(sum_snafu))