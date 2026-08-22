.. board> d -- starts openocd in the background, tracks its pid
   board> t -- starts gdb, loads target/debug/app.elf
   board> q -- stops every tracked openocd instance

   inside gdb --
   target extended-remote localhost:3333 -- attach to openocd
   monitor reset halt -- reset the target and halt at entry
   break <function-name> -- set a breakpoint by symbol name,
       e.g. break gpio_led_toggle
   continue -- run until the next breakpoint
   monitor reset halt -- use again to restart, gdb has no
       "reset" command
   quit -- leave gdb, openocd keeps running until board> q