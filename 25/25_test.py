m = __import__("25")
try:
    attrlist = m.__all__
except AttributeError:
    attrlist = dir (m)
for attr in attrlist:
    globals()[attr] = getattr (m, attr)

assert         1  == Snafu.to_decimal("1")
assert         2  == Snafu.to_decimal("2")
assert         3  == Snafu.to_decimal("1=")
assert         4  == Snafu.to_decimal("1-")
assert         5  == Snafu.to_decimal("10")
assert         6  == Snafu.to_decimal("11")
assert         7  == Snafu.to_decimal("12")
assert         8  == Snafu.to_decimal("2=")
assert         9  == Snafu.to_decimal("2-")
assert        10  == Snafu.to_decimal("20")
assert        15  == Snafu.to_decimal("1=0")
assert        20  == Snafu.to_decimal("1-0")
assert      2022  == Snafu.to_decimal("1=11-2")
assert     12345  == Snafu.to_decimal("1-0---0")
assert 314159265  == Snafu.to_decimal("1121-1110-1=0")

assert Snafu.to_snafu(        1)  == "1"
assert Snafu.to_snafu(        2)  == "2"
assert Snafu.to_snafu(        3)  == "1="
assert Snafu.to_snafu(        4)  == "1-"
assert Snafu.to_snafu(        5)  == "10"
assert Snafu.to_snafu(        6)  == "11"
assert Snafu.to_snafu(        7)  == "12"
assert Snafu.to_snafu(        8)  == "2="
assert Snafu.to_snafu(        9)  == "2-"
assert Snafu.to_snafu(       10)  == "20"
assert Snafu.to_snafu(       15)  == "1=0"
assert Snafu.to_snafu(       20)  == "1-0"
assert Snafu.to_snafu(     2022)  == "1=11-2"
assert Snafu.to_snafu(    12345)  == "1-0---0"
assert Snafu.to_snafu(314159265)  == "1121-1110-1=0"



