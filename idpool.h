// bugway@gmail.com

#ifndef IDPOOL_H
#define IDPOOL_H

#include <stdint.h>

#if defined(__cplusplus)
extern "C" {
#endif 

#ifndef IDPOOL_IMPL
typedef void IdPool;
#endif 

IdPool* idpool_create(int32_t size);
void idpool_destroy(IdPool *ip);
int32_t idpool_query_empty_slot_index(IdPool *ip);
void idpool_return_back_for_use(IdPool *ip, int32_t i);
int32_t idpool_get_available_data_index(IdPool *ip);
void idpool_return_back_for_refill(IdPool *ip, int32_t i);


#if defined(__cplusplus)
}
#endif 

#endif /* IDPOOL_H */
