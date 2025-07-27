from pycalc.app import Expression

if __name__ == "__main__":
    e = Expression("(1-+2)*2")
    print(e.infix)
    print(e.evaluate())