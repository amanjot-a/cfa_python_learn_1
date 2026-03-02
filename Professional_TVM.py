#  Hi   
#  This is a simple program to calculate the time value of money (TVM) for a given set of inputs.
#  The program prompts the user to enter any of the following inputs: present value (PV), future value (FV), interest rate (r), number of periods (n), and payment (PMT).
#  The user can enter any three of the inputs, and the program will calculate the remaining two inputs using the TVM formulas.
#  The program uses the math module to perform calculations and includes error handling to ensure that the user enters valid inputs.
#  The program also includes a simple user interface to guide the user through the input process and display the results in a clear and concise manner.
#  The program can be used to help investors understand the concept of time value of money and how to calculate the various components of TVM based on different inputs. It can also be used as a learning tool for understanding the principles of finance and investment.

import math  


def get_float(prompt):
    """Prompt the user and return a float or None if the input is blank."""
    s = input(prompt).strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        print("Invalid number entered, treating as unknown.")
        return None


def fv(PV, r, n, PMT):
    """Future value given PV, rate, periods and payment."""
    # handle the case r == 0 separately to avoid division by zero
    if r == 0:
        return PV + PMT * n
    return PV * (1 + r) ** n + PMT * (((1 + r) ** n - 1) / r)


def pv(FV, r, n, PMT):
    """Present value given FV, rate, periods and payment."""
    if r == 0:
        return FV - PMT * n
    return (FV - PMT * (((1 + r) ** n - 1) / r)) / ((1 + r) ** n)


def solve_for_n(PV, r, PMT, FV):
    """Solve for number of periods using bisection when needed."""
    # if PMT is zero we can use closed form
    if PMT == 0:
        if PV <= 0 or FV <= 0 or r <= -1:
            return None
        try:
            return math.log(FV / PV) / math.log(1 + r)
        except (ValueError, ZeroDivisionError):
            return None

    # otherwise use numeric search
    low, high = 0.0, 1000.0
    for _ in range(200):
        mid = (low + high) / 2
        val = fv(PV, r, mid, PMT) - FV
        if abs(val) < 1e-8:
            return mid
        if val < 0:
            low = mid
        else:
            high = mid
    return mid


def solve_for_r(PV, FV, n, PMT):
    """Solve for rate using bisection; returns rate as decimal."""
    # we search for r between -0.999999 and very large
    low, high = -0.999999, 1.0
    # expand high until the sign changes or we hit a limit
    while fv(PV, high, n, PMT) < FV and high < 1e6:
        high *= 2
    for _ in range(200):
        mid = (low + high) / 2
        val = fv(PV, mid, n, PMT) - FV
        if abs(val) < 1e-8:
            return mid
        if val < 0:
            low = mid
        else:
            high = mid
    return mid


def solve_for_pmt(PV, FV, r, n):
    """Compute payment given the other four variables."""
    if r == 0:
        return (FV - PV) / n
    denom = ((1 + r) ** n - 1) / r
    return (FV - PV * (1 + r) ** n) / denom


def main():
    print("Professional TVM Calculator")
    print("Enter the known values and leave the others blank.")
    while True:
        PV = get_float("Present value (PV): ")
        FV = get_float("Future value (FV): ")
        r = get_float("Interest rate per period (%) (r): ")
        n = get_float("Number of periods (n): ")
        PMT = get_float("Payment each period (PMT): ")

        # convert percentage to decimal
        if r is not None:
            r /= 100.0

        # treat an unspecified payment as zero for calculations
        if PMT is None:
            PMT = 0.0

        known = [PV, FV, r, n, PMT].count(None)
        if known > 2:
            print("Insufficient data; please provide at least three inputs.")
            continue

        # compute missing values where possible
        if PV is None and FV is not None and r is not None and n is not None:
            PV = pv(FV, r, n, PMT)
        if FV is None and PV is not None and r is not None and n is not None:
            FV = fv(PV, r, n, PMT)
        if n is None and PV is not None and FV is not None and r is not None:
            n = solve_for_n(PV, r, PMT, FV)
        if r is None and PV is not None and FV is not None and n is not None:
            r = solve_for_r(PV, FV, n, PMT)
        if PMT == 0.0 and PV is not None and FV is not None and r is not None and n is not None:
            PMT = solve_for_pmt(PV, FV, r, n)

        print("\nResults:")
        if PV is not None:
            print(f"  PV = {PV:.2f}")
        if FV is not None:
            print(f"  FV = {FV:.2f}")
        if r is not None:
            print(f"  r = {r * 100:.6f}% per period")
        if n is not None:
            print(f"  n = {n:.6f} periods")
        if PMT is not None:
            print(f"  PMT = {PMT:.2f} per period")

        again = input("\nCalculate again? (y/n): ").strip().lower()
        if again != 'y':
            break


if __name__ == '__main__':
    main()
