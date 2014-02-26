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
	
	#input_file = open("seminars-notabs.tsv", 'r')
	#output_file = open("new_seminars-notabs.tsv", 'w')

	char = 'a'
	meta_numb = 17
	i = 1
	
	while char != "":
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
	output_file.close()
	input_file.close()


def getAttr(seminar_str, attr_numb):
	"""parses <seminar_str> string that contains attributes of the object
	and returns attribute with <attr_numb> number"""
	
	attr_list = seminar_str.split('\t')

	return attr_list[attr_numb]


def CreateMetaMatrix():
	""" This function reads history of visits from <history_file_name> file and
	metadata of seminars from <meta_file_name> file. It computes multiple 
	visits of seminars with current meta - for each user. And create 
	appropriate rectangle <meta_matrix_name> matrix.
	"""

	# META ID POSITIONS
	# 0 = seminar_id
	# 1 + 2 = date
	# 3 = topic (category_id)
	# 4 = title

	print "HAVE YOU EVEN CHANGED #.INI PARAMETERS?\n LOOOOOL! CHECK IT OUT"

	# .INI parameters
	print ".INI parameters:"
	semin_id_position = 0
	print "semin_id_position = ", semin_id_position
	meta_id_position = 0
	print "meta_id_position = ", meta_id_position
	meta_file_name = "history_data/topics"
	print "meta_file_name = ", meta_file_name
	history_file_name = "history_data/users_went_mm"
	print "history_file_name = ", history_file_name
	meta_matrix_file_name = "topic_matrix"
	print "meta_matrix_file_name = ", meta_matrix_file_name

	# opening files
	print "opening files..."
	meta_file = open(meta_file_name, 'r')
	history_file = open(history_file_name, 'r')
	meta_matrix_file = open(meta_matrix_file_name, 'w')
	
	# reading history matrix from file
	print "reading history..."
	history_matrix = mmread(history_file).tocsr()
	users_numb = history_matrix.shape[0]
	items_numb = history_matrix.shape[1]

	# creating new matrix
	meta_matrix = zeros((users_numb, 0), dtype = int)
	
	# some routine before main loop
	cur_meta_items = []
	cur_meta_id = 0

	# MAIN LOOP
	print "start of filling <meta_matrix>"
	for line in meta_file:
		#line_meta_id = line.split()[meta_id_position]
		line_meta_id = getAttr(line, meta_id_position)
		#line_semin_id = line.split()[semin_id_position]
		line_meta_id = getAttr(line, semin_id_position)
	
		# new meta_id detected
		if line_meta_id != cur_meta_id:
			new_meta_col = zeros((users_numb, 0), dtype = int)
			for cur_item in cur_meta_items:
				cur_item_col = history_matrix[:,cur_item].toarray()
				new_meta_col = new_meta_col + cur_item_col
			meta_matrix = hstack((meta_matrix, new_meta_col))
			
		# clean list if new meta_id begins
		cur_meta_items = []
		cur_meta_id = line_meta_id
			
		cur_meta_items.append(line_semin_id)	
		
	# writing new <meta_matrix> to file	
	print "writing new <meta_matrix> to file"
	now = datetime.datetime.now()
	now_string = now.strftime("%Y-%m-%d %H:%M")
	mmwrite(meta_matrix_file, meta_matrix, now_string, 'integer')
	
	# closing files
	print "closing files"
	meta_file.close()
	history_file.close()
	meta_matrix_file.close()

#def seminarHasVisitors(history_matrix, meta_matrix)
