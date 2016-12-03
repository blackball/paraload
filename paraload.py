# -*- coding: utf-8 -*-
# bugway@gmail.com

from idpool import IdPool
import threading 
from time import sleep

class ParaLoad(object):
    def __init__(self, buffer, callback):
        self._buffer = buffer
        self._ip = IdPool(len(buffer))
        self._callback = callback
        self._is_finished = False
        self._loaders = []

    
    def __del__(self):
        #if len(self._loaders):
        #    print ("waiting threads to finish!")
        for t in self._loaders:
            t.join()


    def start_loaders(self, num_loaders = 2):
        self._loaders = []
        if not self._is_finished:
            for i in range(num_loaders):
                t = threading.Thread(target = self._private_callback)
                self._loaders.append(t)
                t.start()

                
    def get_available_data_index(self):
        i = 0
        while True:
            i = self._ip.get_available_data_index()
            if i >= 0:
                break
            if self._is_finished:
                return -1
            sleep(0.001)
        return i


    def _private_callback(self):
        while True:
            batch_id = self._query_empty_slot_index()
            ret = self._callback(self._buffer[batch_id])
            if ret == False:
                self._is_finished = True
                break
            else:
                self._return_back_for_use(batch_id)

                
    def _query_empty_slot_index(self):
        i = 0
        while True:
            i = self._ip.query_empty_slot_index()
            if i >= 0:
                break
            sleep(0.001)            
        return i

    
    def return_back_for_refill(self, i):
        self._ip.return_back_for_refill(i);

        
    def _return_back_for_use(self, i):
        self._ip.return_back_for_use(i)
