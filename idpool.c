#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define IDPOOL_IMPL
typedef struct
{
    int32_t lock;
    int32_t size;
    uint8_t lut[0];
} IdPool;

#define IDPOOL_EMPTY  0
#define IDPOOL_FULL   1
#define IDPOOL_IN_USE 2

#include "idpool.h"

#ifdef _MSC_VER

#include <windows.h>

#define atom_spinlock(ptr) while (InterlockedExchange((LONG volatile *)ptr , 1)) {}
#define atom_spinunlock(ptr) InterlockedExchange((LONG volatile *)ptr, 0)

#else

#define atom_spinlock(ptr) while (__sync_lock_test_and_set(ptr,1)) {}
#define atom_spinunlock(ptr) __sync_lock_release(ptr)

#endif

#define LOCK(Q) atom_spinlock(&(Q)->lock)
#define UNLOCK(Q) atom_spinunlock(&(Q)->lock)


IdPool* idpool_create(int32_t size)
{
    IdPool *p = malloc(sizeof(*p) + sizeof(uint8_t) * size);
    p->lock = 0;
    p->size = size;
    {
        int32_t i = 0;
        for (; i < size; ++i) p->lut[i] = IDPOOL_EMPTY;
    }
    return p;
}

void idpool_destroy(IdPool *ip)
{
    free(ip);
}

int32_t idpool_query_empty_slot_index(IdPool *ip)
{
    int32_t i = 0;
    LOCK(ip);
    {
        for (; i < ip->size; ++i) {
            if (ip->lut[i] == 0) break;
        }
                
        if (i == ip->size)
            i = -1;
        else
            ip->lut[i] = IDPOOL_IN_USE;
    }
    UNLOCK(ip);
    return i;
}

void idpool_return_back_for_use(IdPool *ip, int32_t i)
{
    LOCK(ip);
    ip->lut[i] = IDPOOL_FULL;
    UNLOCK(ip);
}

int32_t idpool_get_available_data_index(IdPool *ip)
{
    int32_t i = 0;
    LOCK(ip);
    {
        for (; i < ip->size; ++i) {
            if (ip->lut[i] == IDPOOL_FULL) break;
        }
        if (i == ip->size)
            i = -1;
        else
            ip->lut[i] = IDPOOL_IN_USE;
    }
    UNLOCK(ip);
    return i;
}

void idpool_return_back_for_refill(IdPool *ip, int32_t i)
{
    LOCK(ip);
    ip->lut[i] = IDPOOL_EMPTY;
    UNLOCK(ip);
}
