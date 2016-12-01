### paraload

I was bored at home. A friend asked me a question on chat, he said "I need to train a network, but my data is too big to fit the memory, and also I need to do some argumentation on the fly. Do you have a tool for it ?", "Is there any ready to use tool out there for this purpose ?", I replied. "No, I tried to find it online, tried a couple, but none of them fit my needs exactly, espacially that I have a limited memory.", "ok, it's simple, should be a 1 or 2 hours work.", I replied and followed a long silence...., "Maybe I could write one for you.", he replied immediately with a giant "thank you" emoji...


After ~2 hours work, here is it. following is an example of using it, check paraload_example.py for full example: 

```python
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
        # use the data 
        training(buffer[i])
        # return the batch for refilling
        paraloader.return_back_for_refill(i)
```

This codes is done in short time, only tested on linux for simple cases. on your own when you use it. If you're on windows, you may need to do small modifications in idpool.py when using ctypes loading the shared lib, maybe just several characters change.


