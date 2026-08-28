#include "stm32f4xx_hal.h"

#include "queue.h"
#include "statemachine.h"

enum state {
    STATE_GREEN,
    STATE_ORANGE,
    STATE_RED,
    STATE_BLUE
};

static enum state state;

static void leds_off(void)
{
    HAL_GPIO_WritePin(
        GPIOD,
        GPIO_PIN_12 |
        GPIO_PIN_13 |
        GPIO_PIN_14 |
        GPIO_PIN_15,
        GPIO_PIN_RESET);
}

void statemachine_init(void)
{
    state = STATE_GREEN;
    leds_off();
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12, GPIO_PIN_SET);
}

void statemachine_process(void)
{
    enum queue_event event;

    while (queue_pop(&event)) {
        if (event != QUEUE_EVENT_TICK)
            continue;

        leds_off();

        switch (state) {
        case STATE_GREEN:
            state = STATE_ORANGE;
            HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13, GPIO_PIN_SET);
            break;

        case STATE_ORANGE:
            state = STATE_RED;
            HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, GPIO_PIN_SET);
            break;

        case STATE_RED:
            state = STATE_BLUE;
            HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, GPIO_PIN_SET);
            break;

        case STATE_BLUE:
            state = STATE_GREEN;
            HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12, GPIO_PIN_SET);
            break;
        }
    }
}