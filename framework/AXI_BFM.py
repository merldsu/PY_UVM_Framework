# Copyright 2023 MERL-DSU

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.






import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge ,Timer,RisingEdge,ClockCycles
from cocotb.queue import QueueEmpty, Queue
import logging
import random
import pandas as pd
import pyuvm
from pyuvm import *

from pyuvm import utility_classes

# function of convert binary into integer
def get_int(signal):
	try:
		sig = int(signal.value)
	except ValueError:
		sig = 0
	return sig


#The BFM for Risk V Single Cycle Core

class AXI_BFM(metaclass=utility_classes.Singleton):

	def __init__(self):
		self.dut = cocotb.top
		self.Queue_axi_value = Queue(maxsize = 2)

	# Define the Clock for RTL
	async def CLOCK_RV32(self):       
		while True:
			self.dut.clk.value = 0
			await Timer(2, units = "ns")
			self.dut.clk.value = 1            
			await Timer(2, units = "ns")     


	# Define the Reset for RTL as per design Requirments                       
	async def reset_m(self,rst, rst_dbg):

		self.dut.rst_l.value = rst
		self.dut.dbg_rst_l.value = rst_dbg
  
	# AXI DATA BUS Protocol Communication to RTL
	async def send_values_bfm(self, pc , value):
	
		self.my_tuple = (value, pc)		
		await self.Queue_axi_value.put(self.my_tuple)

		if self.Queue_axi_value.qsize()== 1 :
			pass
			
		elif self.Queue_axi_value.qsize() == 2:
			self.result_tuple= await self.Queue_axi_value.get()
			self.result_tuples= await self.Queue_axi_value.get()
			(self.value, self.pc )= self.result_tuple
			(self.values, self.pcs )= self.result_tuples
			
			self.value_1 = (self.value[2:])
			self.value_2 = (self.values[2:])
			self.pc_1 = (self.pc[2:])
			self.value1 = self.value_1
			self.value2 = self.value_2
			self.concatenated = (self.value2) + (self.value1) 
			self.dut.preload.value = 1
			self.dut.axi_awid.value = 1
			self.dut.axi_awvalid.value = 1
			self.dut.axi_awaddr.value = (int(self.pc, 16))
			self.dut.axi_awregion.value = 0
			self.dut.axi_awlen.value = 0
			self.dut.axi_awsize.value = 0b011
			self.dut.axi_awburst.value = 0
			self.dut.axi_awlock.value = 0
			self.dut.axi_awcache.value = 0
			self.dut.axi_awprot.value = 0
			self.dut.axi_awqos.value = 0
			self.dut.axi_awready.value = 0
			self.dut.axi_wvalid.value = 1
			self.dut.axi_wdata.value = int(self.concatenated,16)
			self.dut.axi_wstrb.value = 0xFF
			self.dut.axi_wlast.value = 1
			await RisingEdge(self.dut.axi_bvalid)
			self.dut.axi_bready.value = 1
			self.dut.axi_awvalid.value = 0
			await RisingEdge(self.dut.clk)
			self.dut.axi_bready.value = 0
			self.dut.preload.value = 0

	
	# This below function recieve the RTL reults
	async def result_monitor(self):     
		await RisingEdge(self.dut.rst_l)
		while self.dut.finish_ecall.value == 0:
			await RisingEdge(self.dut.clk)
		print("after 1 ecall")
		while (self.dut.finish_ecall.value == 1 and self.dut.terminate_count.value != 0x7):
			print("after ecall", self.dut.terminate_count.value)
			await RisingEdge(self.dut.clk)
		await RisingEdge(self.dut.clk)
          
        # This is autonomous function                             
	async def start_tasks(self):   
		cocotb.start_soon(self.CLOCK_RV32())
		cocotb.start_soon(self.reset_m(0, 0))

			
          
  
