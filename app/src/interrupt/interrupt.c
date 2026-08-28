#include "stm32f4xx_hal.h"

#include "interrupt.h"
#include "../kernel/queue.h"

static volatile uint32_t st_tick;

static void interrupt_systick_process(void)
{
    st_tick++;

    if (st_tick >= 500U) {
        st_tick = 0U;
        queue_push(QUEUE_EVENT_TICK);
    }
}

uint32_t HAL_GetTick(void)
{
    return st_tick;
}

HAL_StatusTypeDef HAL_InitTick(uint32_t TickPriority)
{
    (void)TickPriority;

    if (SysTick_Config(HAL_RCC_GetSysClockFreq() / 1000U) != 0U)
        return HAL_ERROR;

    return HAL_OK;
}

void SysTick_Handler(void)
{
    interrupt_systick_process();
}

void interrupt_init(void)
{
    HAL_InitTick(0);
}