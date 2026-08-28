# mb997d_code
STM32 C Embedded Project Template

![Visitors](https://api.visitorbadge.io/api/VisitorHit?user=alexandre14k&repo=https://github.com/alexandre14k/mb997d_code&label=Views&labelColor=%23555555&countColor=%23007EC6)

# About
STM32 C Embedded Project Template<br>
targets the STM32F4-DISCOVERY (MB997) board.<br>
Everyday tasks (build, flash, debug, manage external dependencies)<br>
run through a single interactive entry point,<br>
cross-compiled with the Arm GNU toolchain and built with xmake.

## Features
- Bare-metal C project layout for the STM32F4-DISCOVERY (MB997) board
- `xmake` -- based build system with cross-compilation configuration
- OpenOCD + GDB-ready for on-target flashing and debugging over SWD
- A single `run.py` entry point that wraps build, board,<br>
and external-dependency management behind one interactive menu
- No vendor IDE required — just a toolchain, a build tool, and a terminal

## Prerequisites

| Tool | Purpose |
|---|---|
| [arm-none-eabi-gcc](https://gitlab.arm.com/tooling/gnu-toolchains-for-arm/-/tree/releases/15.3.rel1?ref_type=heads#windows) | Cross-compiler toolchain for ARM Cortex-M cores |
| `gdb-multiarch` | Debugger for stepping through firmware on-target |
| [git](https://git-scm.com/install/) | Version control |
| [python3](https://www.python.org/downloads/release/python-3120/) | Run scripts |
| [openocd](https://openocd.org/pages/getting-openocd.html) | Erase, Flash and Debug binaries |
| [xmake](https://github.com/xmake-io/xmake/releases) | Configures and builds the project |
| [STM32 Discovery mb997d](https://www.st.com/en/evaluation-tools/stm32f4discovery.html) | Target hardware STM32F407VG MCU |

> **Minimum tested environment: Linux Mint 22.2.**<br>
Other Linux distributions, Windows, and macOS should work too<br>
the toolchain, xmake, Python, and OpenOCD are all cross-platform.<br>
See the [wiki](https://github.com/alexandre14k/mb997d_code/wiki) for platform-specific notes.

### Installing on Linux Mint 22.2
```bash
sudo apt update
sudo apt install -y gcc-arm-none-eabi\
     gdb-multiarch git python3 openocd
curl -fsSL https://xmake.io/shget.text | bash
source ~/.xmake/profile
```

### Verify installation
```bash
arm-none-eabi-gcc --version
gdb-multiarch --version
git --version
xmake --version
python3 --version
openocd --version
```

### Hardware setup
Tested on the **STM32F4-DISCOVERY (MB997)** board.<br>
On Linux, add udev rules so it's accessible without **sudo**:
```bash
sudo tee /etc/udev/rules.d/49-stlink.rules > /dev/null <<'RULES'
SUBSYSTEM=="usb", ATTR{idVendor}=="0483", MODE="0666"
RULES
sudo udevadm control --reload-rules
```

## Project Structure
```
.
├── app/        # Application source code
├── doc/        # Releases tests and some documentation
├── ext/        # External/vendor sources (managed via git sparse checkout)
├── script/     # build.py and board.py — drive xmake, OpenOCD, and GDB
├── LICENSE
├── README.md
├── run.bat     # Windows entry point
├── run.py      # Cross-platform entry point (interactive menu)
└── run.sh      # Linux/macOS entry point
```

## Contributing
Issues and pull requests are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the BSD 3-Clause License - see the LICENSE
file for details.

Copyright (c) 2026 alexander14k28@gmail.com

See [LICENSE](LICENSE) for the license governing this project.
