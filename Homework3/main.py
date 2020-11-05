# use slide implementation of square and multiply
def sam(base, exp):
    f = 1
    while exp > 0:
        lsb = 0x1 & exp
        exp >>=1
        if lsb:
            f *= base
        base *= base
    return f


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    base = 5
    exp = 26
    print(sam(base, exp))
    print(base)
    print(exp)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
