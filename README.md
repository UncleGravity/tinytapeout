![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# 7-Segment Counter ASIC

A simple decimal counter that increments once per second from 0 to 9 on a 7-segment display.

> ## What is Tiny Tapeout?
>
> Tiny Tapeout is an educational project that makes it easier and cheaper than ever to get your digital designs manufactured on a real chip. Learn more at [tinytapeout.com](https://tinytapeout.com).

## 3D Viewer
[Open 3D viewer](https://gds-viewer.tinytapeout.com/?model=https://unclegravity.github.io/tinytapeout/tinytapeout.oas&pdk=sky130A)

## 2D Preview
![png](https://unclegravity.github.io/tinytapeout/gds_render.png)

## How it Works

This design implements a 4-bit counter that increments on each clock edge. The counter value is decoded into 7-segment display patterns using combinational logic. When the counter reaches 9, it automatically wraps back to 0.

The design uses a 1 Hz clock (configured in `info.yaml`), which is provided by Tiny Tapeout's RP2040 chip, making the counting visible in real-time without additional clock division circuitry.

## Hardware Requirements

- **7-segment display** (common-cathode)

Connect the output pins (`uo[0]` through `uo[6]`) through resistors to segments A-G of the display. Connect the display's common cathode to ground.

## Running Tests

To run the tests, use the following command from the project root:

```bash
nix develop -c uv run make -B
```

This command:
- Enters the nix development environment
- Uses `uv` to manage the Python environment
- Runs `make -B` to execute the cocotb test suite

Results are displayed in the terminal output, and a waveform file (`tb.vcd`) is generated for inspection. To view the waveform file, use GTKWave:

```bash
gtkwave tb.vcd
```

This will open an interactive viewer where you can inspect the signal traces and debug your design.

## Resources

- [Project Documentation](docs/info.md)
- [Tiny Tapeout FAQ](https://tinytapeout.com/faq/)
- [Digital Design Lessons](https://tinytapeout.com/digital_design/)
- [Join the Community](https://tinytapeout.com/discord)
