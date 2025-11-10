# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

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

    dut._log.info("Test 8-bit adder")

    # Test 1: Basic addition (20 + 30 = 50)
    dut._log.info("Test 1: 20 + 30 = 50")
    dut.ui_in.value = 20
    dut.uio_in.value = 30
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 50, f"Expected 50, got {dut.uo_out.value}"

    # Test 2: Zero addition (0 + 0 = 0)
    dut._log.info("Test 2: 0 + 0 = 0")
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0, f"Expected 0, got {dut.uo_out.value}"

    # Test 3: Adding with zero (42 + 0 = 42)
    dut._log.info("Test 3: 42 + 0 = 42")
    dut.ui_in.value = 42
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 42, f"Expected 42, got {dut.uo_out.value}"

    # Test 4: Maximum values without overflow (100 + 100 = 200)
    dut._log.info("Test 4: 100 + 100 = 200")
    dut.ui_in.value = 100
    dut.uio_in.value = 100
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 200, f"Expected 200, got {dut.uo_out.value}"

    # Test 5: Overflow test (200 + 100 = 44, due to 8-bit overflow)
    dut._log.info("Test 5: 200 + 100 = 44 (overflow)")
    dut.ui_in.value = 200
    dut.uio_in.value = 100
    await ClockCycles(dut.clk, 1)
    expected = (200 + 100) & 0xFF  # 300 & 0xFF = 44
    assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"

    # Test 6: Maximum value addition (255 + 255 = 254, due to overflow)
    dut._log.info("Test 6: 255 + 255 = 254 (overflow)")
    dut.ui_in.value = 255
    dut.uio_in.value = 255
    await ClockCycles(dut.clk, 1)
    expected = (255 + 255) & 0xFF  # 510 & 0xFF = 254
    assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"

    # Test 7: Random test (123 + 67 = 190)
    dut._log.info("Test 7: 123 + 67 = 190")
    dut.ui_in.value = 123
    dut.uio_in.value = 67
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 190, f"Expected 190, got {dut.uo_out.value}"

    dut._log.info("All tests passed!")
