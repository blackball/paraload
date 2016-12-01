# -*- coding: utf-8 -*-
# bugway@gmail.com

import os
import ctypes

class IdPool(object):
    try:
        _idpool_dll = ctypes.cdll.LoadLibrary(os.path.abspath("c_idpool.so"))
        _c_idpool_create = _idpool_dll.idpool_create
        _c_idpool_create.restype = ctypes.c_void_p
        _c_idpool_create.argstype = [ctypes.c_int32]
        
        _c_idpool_destroy = _idpool_dll.idpool_destroy
        _c_idpool_destroy.restype = None 
        _c_idpool_destroy.argstype = [ctypes.c_void_p]

        _c_idpool_query_empty_slot_index = _idpool_dll.idpool_query_empty_slot_index
        _c_idpool_query_empty_slot_index.restye  = ctypes.c_int32
        _c_idpool_query_empty_slot_index.argstype  = [ctypes.c_void_p]

        _c_idpool_get_available_data_index = _idpool_dll.idpool_get_available_data_index
        _c_idpool_get_available_data_index.restye  = ctypes.c_int32
        _c_idpool_get_available_data_index.argstype  = [ctypes.c_void_p]

        _c_idpool_return_back_for_use = _idpool_dll.idpool_return_back_for_use
        _c_idpool_return_back_for_use.restype = None 
        _c_idpool_return_back_for_use.argstype = [ctypes.c_void_p, ctypes.c_int32]

        _c_idpool_return_back_for_refill = _idpool_dll.idpool_return_back_for_refill
        _c_idpool_return_back_for_refill.restype = None 
        _c_idpool_return_back_for_refill.argstype = [ctypes.c_void_p, ctypes.c_int32]
        
        _idpool_dll = None
    except Exception, e:
        raise e
    
    # TODO: setup input and output types    
    def __init__(self, size = 8):
        self._c_ip = IdPool._c_idpool_create(size)
        
    def __del__(self):
        self._c_idpool_destroy(self._c_ip)
        
    def query_empty_slot_index(self):
        return IdPool._c_idpool_query_empty_slot_index(self._c_ip)

    def get_available_data_index(self):
        return IdPool._c_idpool_get_available_data_index(self._c_ip)

    def return_back_for_use(self, i):
        #print "fill:", i
        IdPool._c_idpool_return_back_for_use(self._c_ip, i)

    def return_back_for_refill(self, i):
        #print "usedup", i
        IdPool._c_idpool_return_back_for_refill(self._c_ip, i)
