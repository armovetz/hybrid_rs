"""this module launch some routines for absolutely raw data 
of visits and meta-attributes. 

As result - this script generates 2 files that contain ids of
seminars that both have history of visits and meta attributes.
And they are sorted.

"""

import meta_parser
from meta_parser import *

print "Started!"


############    1    #######################
# turn every seminar into single string
print "step 1/6 \n turning seminars into single strings..."
raw_file = open("../../data/raw/seminars-notabs.tsv", 'r')
output_file = open("../../data/tmp/_step1", 'w')
MetaDataToStrings(raw_file, output_file)
raw_file.close()
output_file.close()

############    2    #######################
# get list of id of seminars that have meta data
print "step 2/6 \n getting list of id of seminars that have meta data"
input_file = open("../../data/tmp/_step1", 'r')
meta_id_list = []
for line in input_file:
	meta_id_list.append(int(line.split('\t')[0]))
	#meta_id_list.append(int(getAttr(line, 0)))
input_file.close()

# get list of id of seminars that have history of visits
print "getting list of id of seminars that have history of visits"
input_file = open("../../data/raw/seminars-users.tsv", 'r')
hist_id_list = []
for line in input_file:
	cur_id = int(line.split()[1])
	if cur_id not in hist_id_list:
		hist_id_list.append(cur_id)
input_file.close()

# creating list of id's that have both meta-attributes and history of visits
print "creating list of id's that have both meta-attributes and history of visits"
nnz_list = []
for id in hist_id_list:
	if id in meta_id_list:
		nnz_list.append(id)

nnz_list = sort(nnz_list)

# write nnz ids into file
nnz_file = open("../../data/tmp/_nnz_ids", 'w')

for id in nnz_list:
	nnz_file.write(str(id) + '\n')
nnz_file.close()

############    3    #######################
# sorting history of visits by seminars_id and writing both files into 
# new files
print "step 3/6 \n sorting history of visits by seminars_id and writing both files into new files"
def compare_meta(op1, op2):	
	return (int(op1.split('\t')[0]) - int(op2.split('\t')[0]))
def compare_hist(op1, op2):
	return (int(op1.split('\t')[1]) - int(op2.split('\t')[1]))

meta_file = open("../../data/tmp/_step1", 'r')
hist_file = open("../../data/raw/seminars-users.tsv", 'r')

meta_line_list = []
for line in meta_file:
	meta_line_list.append(line)
sorted_meta_line_list = sorted(meta_line_list, cmp = compare_meta)

hist_line_list = []
for line in hist_file:
	hist_line_list.append(line)
sorted_hist_line_list = sorted(hist_line_list, cmp = compare_hist)

meta_file.close()
hist_file.close()

sorted_meta_file = open("../../data/tmp/_sorted_meta", 'w')
sorted_hist_file = open("../../data/tmp/_sorted_hist", 'w')

for line in sorted_meta_line_list:
	sorted_meta_file.write(line)
for line in sorted_hist_line_list:
	sorted_hist_file.write(line)

sorted_meta_file.close()
sorted_hist_file.close()


############    4    #######################
# write files that contain only seminars of history and meta
print "step 4/6 \n writing files that contain only seminars of history and meta..."
nnz_meta_file = open("../../data/tmp/_nnz_meta", 'w')
nnz_hist_file = open("../../data/tmp/_nnz_hist", 'w')

for line in sorted_meta_line_list:
	if int(line.split()[0]) in nnz_list:
		nnz_meta_file.write(line)

for line in sorted_hist_line_list:
	if int(line.split()[1]) in nnz_list:
		nnz_hist_file.write(line)
nnz_meta_file.close()
nnz_hist_file.close()


############    5    #######################
# giving new id's for seminars
print "step 5/6 \n giving new numbers for 'non-sero' seminars"

input_meta_file = open("../../data/tmp/_nnz_meta", 'r')
input_hist_file = open("../../data/tmp/_nnz_hist", 'r')
output_meta_file = open("../../data/well_made/meta", 'w')
output_hist_file = open("../../data/tmp/_new_sem_id_hist", 'w')

#loop that gives new numbers for 'non-zero' seminars
new_id = 0

for line in input_meta_file:
	new_id += 1
	tail = (line.split('\t', 1))[1]
	output_meta_file.write(str(new_id) + '\t' + tail)
output_meta_file.close()
input_meta_file.close()

seminars_numb = new_id

new_id = 0
prev_id = 0
for line in input_hist_file:
	split_list = line.split('\t')
	if int(split_list[1]) != prev_id:
		new_id += 1
		prev_id = int(split_list[1])
	output_hist_file.write(split_list[0] + '\t' + str(new_id) + "\t 1 \n")
output_hist_file.close()
input_hist_file.close()

############    6    #######################
# giving new id's for users
print "step 6/7 \n sorting history by users id"

input_file = open("../../data/tmp/_new_sem_id_hist", 'r')
output_file = open("../../data/tmp/_sorted_by_users_hist", 'w')

list = []
for line in input_file:
	list.append(line)

def cmp_line_by_users(op1, op2):
	return int(op1.split()[0]) - int(op2.split()[0])
	

srtd_by_users_list = sorted(list, cmp_line_by_users)

for line in srtd_by_users_list:
	output_file.write(line)

output_file.close()

############    7    #######################
# giving new id's for users
print "step 7/7 \n giving new numbers for 'non-zero' users"

input_file = open("../../data/tmp/_sorted_by_users_hist", 'r')

#loop that gives new numbers for 'non-zero' users
list = []
for line in input_file:
	list.append(line)
input_file.close()

srtd_by_users_list = sorted(list, cmp_line_by_users)

new_id = 0
prev_id = 0

lines_to_write = []
visits_numb = 0

for line in srtd_by_users_list:
	visits_numb += 1
	split_list = line.split()
	if int(split_list[0]) != prev_id:
		new_id += 1
		prev_id = int(split_list[0])
	lines_to_write.append(str(new_id) + '\t' + split_list[1] + "\t 1 \n")
users_numb = new_id

mm_file = open("../../data/well_made/history.mm", 'w')
mm_file.write("%%MatrixMarket matrix coordinate integer general \n")
import datetime

now = datetime.datetime.now()
now_string = now.strftime("%Y-%m-%d %H:%M")
mm_file.write("%Generated " + now_string + '\n')
mm_file.write(str(users_numb) + '\t' + str(seminars_numb) + '\t' + str(visits_numb) + '\n')

for line in lines_to_write:
	mm_file.write(line)
mm_file.close()

print "TOTAL SUCCESS"
