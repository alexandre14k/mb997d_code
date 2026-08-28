#ifndef QUEUE_H
#define QUEUE_H

enum queue_event {
    QUEUE_EVENT_NONE,
    QUEUE_EVENT_TICK
};

void queue_init(void);
int queue_push(enum queue_event event);
int queue_pop(enum queue_event *event);

#endif