# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

# 7-segment display patterns for digits 0-9
# Bit order: [G, F, E, D, C, B, A]
SEVEN_SEG_PATTERNS = {
    0: 0b0111111,  # 0
    1: 0b0000110,  # 1
    2: 0b1011011,  # 2
    3: 0b1001111,  # 3
    4: 0b1100110,  # 4
    5: 0b1101101,  # 5
    6: 0b1111101,  # 6
    7: 0b0000111,  # 7
    8: 0b1111111,  # 8
    9: 0b1101111,  # 9
}


@cocotb.test()
async def test_counter_reset(dut):
    """Test that the counter starts at 0 after reset"""
    dut._log.info("Start counter reset test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # After reset, counter should be at 0
    await ClockCycles(dut.clk, 1)
    segments = int(dut.uo_out.value) & 0x7F  # Mask out the decimal point (bit 7)
    dut._log.info(
        f"After reset: segments = 0b{segments:07b} (expected 0b{SEVEN_SEG_PATTERNS[0]:07b})"
    )
    assert segments == SEVEN_SEG_PATTERNS[0], (
        f"Expected digit 0 pattern, got 0b{segments:07b}"
    )

    dut._log.info("Test passed: Counter starts at 0")


@cocotb.test()
async def test_counter_increment(dut):
    """Test that the counter increments on each clock cycle"""
    dut._log.info("Start counter increment test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # Test that counter increments from 0 to 1
    initial_segments = int(dut.uo_out.value) & 0x7F
    dut._log.info(f"Initial segments: 0b{initial_segments:07b} (digit 0)")
    assert initial_segments == SEVEN_SEG_PATTERNS[0], "Should start at 0"

    # Wait one clock cycle
    await ClockCycles(dut.clk, 1)

    new_segments = int(dut.uo_out.value) & 0x7F
    dut._log.info(
        f"After 1 cycle: segments = 0b{new_segments:07b} (expected 0b{SEVEN_SEG_PATTERNS[1]:07b})"
    )
    assert new_segments == SEVEN_SEG_PATTERNS[1], (
        f"Expected digit 1 pattern, got 0b{new_segments:07b}"
    )

    dut._log.info("Test passed: Counter increments correctly")


@cocotb.test()
async def test_all_digits(dut):
    """Test that all digits 0-9 are displayed correctly and counter wraps"""
    dut._log.info("Start all digits test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # Test each digit from 0 to 9, then wrap to 0
    for expected_digit in range(11):  # 0 through 9, then wrap to 0
        digit = expected_digit % 10
        segments = int(dut.uo_out.value) & 0x7F
        expected_pattern = SEVEN_SEG_PATTERNS[digit]

        dut._log.info(
            f"Digit {digit}: segments = 0b{segments:07b}, expected = 0b{expected_pattern:07b}"
        )
        assert segments == expected_pattern, (
            f"Expected digit {digit} pattern (0b{expected_pattern:07b}), got 0b{segments:07b}"
        )

        # Wait for next increment (1 clock cycle)
        if expected_digit < 10:  # Don't wait after the last check
            await ClockCycles(dut.clk, 1)

    dut._log.info("Test passed: All digits display correctly and counter wraps at 10")


@cocotb.test()
async def test_wrap_around(dut):
    """Test that counter wraps from 9 back to 0"""
    dut._log.info("Start wrap around test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # Advance to digit 9
    await ClockCycles(dut.clk, 9)

    segments = int(dut.uo_out.value) & 0x7F
    dut._log.info(f"At digit 9: segments = 0b{segments:07b}")
    assert segments == SEVEN_SEG_PATTERNS[9], "Should be at digit 9"

    # One more clock should wrap to 0
    await ClockCycles(dut.clk, 1)

    segments = int(dut.uo_out.value) & 0x7F
    dut._log.info(f"After wrap: segments = 0b{segments:07b}")
    assert segments == SEVEN_SEG_PATTERNS[0], "Should wrap to digit 0"

    dut._log.info("Test passed: Counter wraps correctly from 9 to 0")


@cocotb.test()
async def test_decimal_point(dut):
    """Test that the decimal point (bit 7) is always off"""
    dut._log.info("Start decimal point test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # Check decimal point at several different counts
    for i in range(5):
        decimal_point = (int(dut.uo_out.value) >> 7) & 0x1
        dut._log.info(f"Check {i}: Decimal point bit = {decimal_point}")
        assert decimal_point == 0, f"Decimal point should be 0, got {decimal_point}"

        # Advance counter
        await ClockCycles(dut.clk, 1)

    dut._log.info("Test passed: Decimal point is always off")


@cocotb.test()
async def test_bidirectional_pins(dut):
    """Test that bidirectional pins are configured as inputs (not used)"""
    dut._log.info("Start bidirectional pins test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)

    # Check that uio_oe is 0 (all pins are inputs)
    assert int(dut.uio_oe.value) == 0, (
        f"Expected uio_oe to be 0, got {dut.uio_oe.value}"
    )

    # Check that uio_out is 0
    assert int(dut.uio_out.value) == 0, (
        f"Expected uio_out to be 0, got {dut.uio_out.value}"
    )

    dut._log.info("Test passed: Bidirectional pins correctly configured")
