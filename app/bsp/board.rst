.. _board  -- mb997d
    label  -- STM32F4DISCOVERY
    device -- STM32F407VG

    Cortex-M4F -- 168 MHz
    clock -- HSI -- internal -- 16 MHz
    clock -- HSE -- external crystal -- 8 MHz
    clock -- LSE -- external crystal -- 32.768 kHz
    clock -- LSI -- internal -- ~32 kHz

    PLL -- HSE -- 8 MHz
    PLL_M -- 8
    PLL_N -- 336
    PLL_P -- 2
    PLL_Q -- 7
    SYSCLK -- 168 MHz
    AHB -- 168 MHz
    APB1 -- 42 MHz
    APB2 -- 84 MHz

    flash -- 1 MB
    ram -- SRAM -- 128 KB

    PA0 -- GPIO -- ADC123_IN0
    PA1 -- GPIO -- ADC123_IN1
    PA2 -- GPIO -- USART2_TX -- ADC123_IN2
    PA3 -- GPIO -- USART2_RX -- ADC123_IN3
    PA4 -- GPIO -- SPI1_NSS -- ADC12_IN4
    PA5 -- GPIO -- SPI1_SCK -- ADC12_IN5
    PA6 -- GPIO -- SPI1_MISO -- ADC12_IN6
    PA7 -- GPIO -- SPI1_MOSI -- ADC12_IN7

    PA8 -- GPIO -- TIM1_CH1
    PA9 -- GPIO -- USART1_TX
    PA10 -- GPIO -- USART1_RX
    PA11 -- GPIO -- USB_OTG_FS_DM
    PA12 -- GPIO -- USB_OTG_FS_DP
    PA13 -- SWDIO
    PA14 -- SWCLK
    PA15 -- GPIO -- SPI1_NSS

    PB0 -- GPIO -- ADC12_IN8
    PB1 -- GPIO -- ADC12_IN9
    PB3 -- GPIO -- SPI1_SCK
    PB4 -- GPIO -- SPI1_MISO
    PB5 -- GPIO -- SPI1_MOSI
    PB6 -- GPIO -- I2C1_SCL
    PB7 -- GPIO -- I2C1_SDA
    PB8 -- GPIO -- I2C1_SCL
    PB9 -- GPIO -- I2C1_SDA
    PB10 -- GPIO -- I2C2_SCL -- USART3_TX
    PB11 -- GPIO -- I2C2_SDA -- USART3_RX
    PB12 -- GPIO -- SPI2_NSS
    PB13 -- GPIO -- SPI2_SCK
    PB14 -- GPIO -- SPI2_MISO
    PB15 -- GPIO -- SPI2_MOSI

    PC13 -- GPIO
    PC14 -- LSE_IN -- 32.768 kHz
    PC15 -- LSE_OUT -- 32.768 kHz

    PD12 -- GPIO -- onboard LED GREEN
    PD13 -- GPIO -- onboard LED ORANGE
    PD14 -- GPIO -- onboard LED RED
    PD15 -- GPIO -- onboard LED BLUE

    PH0 -- HSE_IN -- 8 MHz
    PH1 -- HSE_OUT -- 8 MHz

    VDD -- 3.3V
    VSS -- ground
    VBAT -- RTC / backup supply
    NRST -- active-LOW reset

    linker script
    FLASH -- ORIGIN 0x08000000 -- LENGTH 1024K
    RAM -- ORIGIN 0x20000000 -- LENGTH 128K