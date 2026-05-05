import os
import random
import sys
import logging
import cocotb
from cocotb.triggers import RisingEdge, Timer

CLOCKPERIOD = 10
SIMTIME = 1000
N_RANDOM_TEST = 100


async def clock(dut):
    for _ in range(SIMTIME):
        dut.clk_i.value = 1
        await Timer(CLOCKPERIOD/2, "ns")
        dut.clk_i.value = 0
        await Timer(CLOCKPERIOD/2, "ns")

# Single directed test

@cocotb.test()
async def directed_test(dut):
    cocotb.log.info("Starting directed verification")
    
    # Start clock & reset state
    running_clk = cocotb.start_soon(clock(dut))
    dut.rst_i.value = 0
    dut.data_valid_i.value = 0
    dut.a.value = 0
    dut.b.value = 0
    dut.c.value = 0

    
    # de-assert reset
    await Timer(4*CLOCKPERIOD, "ns")
    dut.rst_i.value = 1
    
    await Timer(CLOCKPERIOD, "ns")
    await RisingEdge(dut.clk_i)
    dut.data_valid_i.value = 1
    dut.a.value = 1
    dut.b.value = 2
    dut.c.value = 3

    await RisingEdge(dut.clk_i)
    dut.data_valid_i.value = 0

    await RisingEdge(dut.clk_i)
    if dut.output_valid_o.value == 1:
        cocotb.log.info(f"SUM : {dut.sum.value}, carry : {dut.carry.value}")
        await running_clk
        cocotb.log.info("directed test finished")
    else:   
        raise AssertionError("output_valid_o never became 1")
    

# Randomized test

@cocotb.test()
async def random_test(dut):
    cocotb.log.info("Starting random test")

    # Init state
    running_clk = cocotb.start_soon(clock(dut))
    dut.data_valid_i.value = 0
    dut.a.value = 0
    dut.b.value = 0
    dut.c.value = 0

    await Timer(CLOCKPERIOD, "ns")

    for test in range(N_RANDOM_TEST):
        await RisingEdge(dut.clk_i)
        dut.data_valid_i.value = 1
        a = random.getrandbits(8)
        b = random.getrandbits(8)
        c = random.getrandbits(8)
        dut.a.value = a
        dut.b.value = b
        dut.c.value = c

        await RisingEdge(dut.clk_i)
        dut.data_valid_i.value = 0

        await RisingEdge(dut.clk_i)
        if dut.output_valid_o.value == 1:
            try:
                assert ((a+b+c) ==  dut.sum.value)
            except:
                ArithmeticError(f"Wrong value at the output for Test ID :{test} \n"
                f"expected : {a+b+c}, got {dut.sum.value}")
        else:   
            raise AssertionError("output_valid_o never became 1")
    
    await running_clk
    cocotb.log.info("Random test finished")        