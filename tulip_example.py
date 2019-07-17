import numpy as np
import tulipy as ti


def print_info(indicator):
    print("Type:", indicator.type)
    print("Full Name:", indicator.full_name)
    print("Inputs:", indicator.inputs)
    print("Options:", indicator.options)
    print("Outputs:", indicator.outputs)





if __name__ == '__main__':

    DATA = np.array([3, 5, 10, 15, 20, 25], dtype=np.float64)

    print(ti.sma(DATA, period=3))