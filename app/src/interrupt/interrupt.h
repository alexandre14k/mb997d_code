#ifndef INTERRUPT_H
#define INTERRUPT_H

#include "stm32f4xx_hal.h"

uint32_t HAL_GetTick(void);
HAL_StatusTypeDef HAL_InitTick(uint32_t TickPriority);

void interrupt_init(void);

#endif