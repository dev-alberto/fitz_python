import numpy as np
import tulipy as ti
import timeit
from numpy_ringbuffer import RingBuffer

def print_info(indicator):
    print("Type:", indicator.type)
    print("Full Name:", indicator.full_name)
    print("Inputs:", indicator.inputs)
    print("Options:", indicator.options)
    print("Outputs:", indicator.outputs)


def mock_data():
    np.random.seed(1)
    return np.random.normal(loc = 0, scale = 1, size = (10000000000,))

def compute_one():
    data = mock_data()[-256:]
    r = []
    return ti.sma(data, 256)

def compute():
    data = mock_data()
    return ti.sma(data, 256)


if __name__ == '__main__':

    queue = RingBuffer(capacity=6, dtype=np.float64)

    queue.append(6)
    queue.append(5)
    queue.append(4)
    queue.append(3)
    queue.append(2)
    queue.append(1)

    #print(queue)
    DATA = np.array(queue)
    print(DATA.dtype)
    print(ti.sma(DATA, period=3))



    # code snippet to be executed only once 
#    mysetup = "import numpy as np \nimport tulipy as ti"

    # code snippet whose execution time is to be measured 
#    mycode = '''def compute():
#        data = mock_data()
#        return ti.sma(data, 256)'''
    
#    mycode2 = '''def compute_one():
#        data = mock_data()[-256:]
#        return ti.sma(data, 256)'''
  
    # timeit statement 
#    print(timeit.timeit(setup = mysetup, 
#                        stmt = mycode, 
#                        number = 1000000))

#    print(timeit.timeit(setup = mysetup, 
#                        stmt = mycode2, 
#                        number = 1000000))
    
    #print(len(compute()))

    #print(len(compute_one()))