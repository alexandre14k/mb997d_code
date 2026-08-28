#include "queue.h"

#define QUEUE_SIZE 8

static enum queue_event queue[QUEUE_SIZE];

static volatile unsigned int write_index;
static volatile unsigned int read_index;

void queue_init(void)
{
    write_index = 0;
    read_index = 0;
}

int queue_push(enum queue_event event)
{
    unsigned int next;

    next = (write_index + 1U) % QUEUE_SIZE;

    if (next == read_index)
        return 0;

    queue[write_index] = event;
    write_index = next;

    return 1;
}

int queue_pop(enum queue_event *event)
{
    if (read_index == write_index)
        return 0;

    *event = queue[read_index];
    read_index = (read_index + 1U) % QUEUE_SIZE;

    return 1;
}