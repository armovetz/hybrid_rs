import scipy
from scipy import *
import numpy
from numpy import *
import sys
import scipy.sparse
from scipy.sparse import *
import scipy.io.mmio
from scipy.io.mmio import *

def MetaDataToStrings(input_file, output_file):
	""" functions reads data from <input_file> and deletes 
	newlines symbols (turns them to whitespaces). Thus every object
	will be represented on one string with its 17 attributes separated
	with \t """
	
	char = 'a'
	meta_numb = 17
	i = 1
	
	while char != "":
		print j
		char = input_file.read(1)
		
		if(char == '\t'):
			if i == meta_numb:
				i = 1
				output_file.write('\n')
			else:
				i += 1
				output_file.write('\t')
			continue
		
		if(char == '\n'):
			if i == meta_numb:
				i = 1
				output_file.write('\n')
			else:
				output_file.write(' ')
			continue
	
		output_file.write(char)

	output_file.write("")
	
	input_file.close()
	output_file.close()


def GetNumerousAttributes():
	
	input_file = open("../../data/well_made/meta", 'r')
	output_file = open("../../data/well_made/often_numerous_attributes", 'w')

	#attr_positions_list = [0, 3, 4, 6, 9, 11, 15]
	attr_positions_list = [0, 3, 5, 6, 15]

	for line in input_file:
		attr_list = line.split('\t')
		line_to_write = ""
		for attr in attr_positions_list:
			line_to_write += attr_list[attr]
			line_to_write += '\t'
		line_to_write = line_to_write[0:len(line) - 1] + '\n'
		output_file.write(line_to_write)

	output_file.close()
	input_file.close()
