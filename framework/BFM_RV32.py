# Copyright [2023] [MERL-DSU]

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
import enum
import logging
import random
import pandas as pd

from pyuvm import utility_classes

def get_int(signal):
	try:
		sig = int(signal.value)
	except ValueError:
		sig = 0
	return sig


#The BFM for Risk V Single Cycle Core

class RV32_BFM(metaclass=utility_classes.Singleton):

	def __init__(self):
		self.dut = cocotb.top
		self.instruction_Address_result_Monitor_list =[]
		self.instruction_result_Monitor_list =[]
		self.result_monitor_list = []
		self.transmit = 0 

	# Define the Clock for RTL
	async def CLOCK_RV32(self):       
		while True:
			self.dut.clk.value = 0
			await Timer(2, units = "ns")
			self.dut.clk.value = 1            
			await Timer(2, units = "ns")     


	# Define the Reset for RTL as per design Requirments                       
	async def reset_m(self,rst):

		self.dut.rst.value = rst
  
	# Simple Protocol Communication to RTL
	
	async def send_values_bfm(self,rv32_pc, rv32_value):

		if (self.transmit == 0):
			await self.instruction_transmitter_bfm(rv32_pc, rv32_value)
			
			if (rv32_value == "0x00000073"):
				await FallingEdge(self.dut.clk)
				self.dut.Instruction_Write_Enable.value = 0
				self.transmit = 1
			else:
				self.transmit = 0
		elif(self.transmit == 1):
			
			await self.data_transmitter_bfm(rv32_pc, rv32_value)
			if (get_int(self.dut.rst) == 1):
				self.transmit = 2
			else:
				self.transmit = 1
		else:
			pass

	# This below function call in Send Values BFM and Send the values to RTL
	async def instruction_transmitter_bfm(self,rv32_pc, rv32_value):
		await FallingEdge(self.dut.clk)
		self.dut.Instruction_Write_Enable.value = 1
		self.dut.Instruction_Address.value = int(rv32_pc,16)
		self.dut.Instruction_Write.value = int(rv32_value,16)
	
	# This below function call in Send Values BFM and Send the Data to RTL
	async def data_transmitter_bfm(self,rv32_pc, rv32_data):
		await FallingEdge(self.dut.clk)
		self.dut.Data_write_Address.value = int(rv32_pc,16)
		self.dut.Data_write_Data.value = int(rv32_data,16)

	# This below function recieve the signals from RTL while running driver	
	async def command_monitor(self):
		await RisingEdge(self.dut.clk)
		self.rv32_instr_add_cmd_mon=("0x"+((hex(self.dut.Instruction_Address_cmd_Monitor.value)[2:]).zfill(8)))
		self.rv32_instr_cmd_mon=("0x"+((hex(self.dut.Instruction_cmnd_Monitor.value)[2:]).zfill(8)))


		cmd_mon = (self.rv32_instr_add_cmd_mon,self.rv32_instr_cmd_mon)
		return cmd_mon
	
	# This below function recieve the RTL reults
	async def result_monitor(self):       
		await RisingEdge(self.dut.rst)
		while self.dut.Finish_Prog.value == 0:
			await RisingEdge(self.dut.clk)
			self.instruction_Address_result_Monitor_list.append("0x"+((hex(self.dut.Instruction_Address_result_Monitor.value )[2:]).zfill(8)))
			self.instruction_result_Monitor_list.append("0x"+((hex(self.dut.Instruction_result_Monitor.value)[2:]).zfill(8)))
			self.result_monitor_list.append("0x"+((hex(self.dut.Result_result_Monitor.value)[2:]).zfill(8)))
			
		res_rv32 = (self.instruction_Address_result_Monitor_list,self.instruction_result_Monitor_list,self.result_monitor_list)
		return res_rv32
          
        # This is autonomous function                             
	async def start_tasks(self):   
		cocotb.start_soon(self.CLOCK_RV32())
		cocotb.start_soon(self.reset_m(1))

          
  
