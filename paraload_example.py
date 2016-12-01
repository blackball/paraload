# -*- coding: utf-8 -*-
# bugway@gmail.com
# -*- coding: utf-8 -*-
# bugway@gmail.com

import itertools
from time import sleep 
from paraload import ParaLoad
import numpy as np

# write your data item 
class Batch:
    def __init__(self):
        self.X = 0 # allocate memory, like: np.array((30,32,32), dtype = np.float32)
        self.Y = 0

# implement your callback for preparing a batch of data
counter = itertools.count()
def callback(batch):
    global counter
    # load data into batch
    batch.X = counter.next()
    sleep(0.01)
    return batch.X < 1000 # False indicates the job is finished

# dummy function to demostrate how to use the batch 
def training(batch):
    #s = 0
    print "training:", batch.X
    sleep(0.05)
    
if __name__ == '__main__':
    # create a working buffer in memory with 100 batches inside 
    buffer = [Batch() for i in xrange(100)]  
    # setup the paraload
    paraloader = ParaLoad(buffer, callback)
    # will use 4 threads for loading data into buffer 
    # you could adjust the number for your needs 
    paraloader.start_loaders(4)
    
    while True:
        # try to get a loaded data indice, if i < 0 means, job finished
        i = paraloader.get_available_data_index()
        if i < 0:
            break
        # use data 
        training(buffer[i])
        # return the batch for refilling 
        paraloader.return_back_for_refill(i)
