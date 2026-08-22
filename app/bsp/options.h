#ifndef OPTIONS_H
#define OPTIONS_H

// -- see RM0090, section 3.7 "Option bytes"
// -- (Flash memory and protection, STM32F4 series)

// -- no read protection, flash stays writable
#define OPTIONS_RDP_LEVEL     OB_RDP_LEVEL_0

// -- no page write protection
#define OPTIONS_WRP_STATE     OB_WRPSTATE_DISABLE

// -- no pages selected, since WRP is disabled
#define OPTIONS_WRP_PAGES     0x00000000U

// -- watchdog started by software, not hardware
#define OPTIONS_IWDG          OB_IWDG_SW

// -- no reset on entering stop mode
#define OPTIONS_STOP          OB_STOP_NORST

// -- no reset on entering standby mode
#define OPTIONS_STDBY         OB_STDBY_NORST

#endif