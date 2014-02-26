"""
TIME SORTER

This script sorts meta strings by time of seminars.
It also sorts history according to meta strings.
It saves mapping between 

RESULT:
new files in data are created:
    - data/well_done/time_sorted_history.mm
        * seminars (columns) are sorted by time
    - data/well_done/time_sorted_meta
        * seminars (strings) are sorted by time
    - some temporary trash (debug) files are created in data/tmp

"""

import sys
sys.path.append("..")
#import Bar
import os
#os.chdir("..")
import misc_functions
from misc_functions import *

#os.chdir("data_preprocessing")

old_meta_list = []
old_meta_file = open("../../data/well_done/meta", 'r')
for line in old_meta_file:
    old_meta_list.append(line)
old_meta_file.close()

# =====================
# DEBUG PRINT
print "old_meta_list"
for i in range(10):
    print getMetaString(old_meta_list[i], 0) + "--" + getMetaString(old_meta_list[i], 1)

print "===== \n"
# =====================

# sort seminar strings by time meta
time_sorted_meta_list = misc_functions.sortMetaListByMeta(old_meta_list, 5)

# =====================
# DEBUG PRINT
print "time_sorted_meta_list"
for i in range(10):
    print getMetaString(time_sorted_meta_list[i], 0) + "--" + getMetaString(time_sorted_meta_list[i], 1)

print "===== \n"
# =====================


#print len(old_meta_list)
#print len(time_sorted_meta_list)

"""
for i in range(20):
    print misc_functions.getMetaString(old_meta_list[i], 0), misc_functions.getMetaString(old_meta_list[i], 5)
    
print "==========" 

for i in range(20):
    print misc_functions.getMetaString(sorted_meta_list[i], 0), misc_functions.getMetaString(sorted_meta_list[i], 5)
"""

id_map_list = []
time_sorted_meta_file = open("../../data/well_done/time_sorted_meta", 'w')
new_id = 0
for line in time_sorted_meta_list:
    time_sorted_meta_file.write(str(new_id) + line[line.find("\t") : len(line)])
    id_map_list.append(misc_functions.getMetaString(line, 0) + "\t" + str(new_id))
    #sorted_id_list.append(misc_functions.getMeta(line, 0)
    new_id += 1
time_sorted_meta_file.close()

# =====================
# DEBUG PRINT
print "id_map_list"
for i in range(10):
    print id_map_list[i]

print "===== \n"
# =====================

# ==========================
#   giving new ids to history matrix
# ==========================

old_history_file = open("../../data/well_done/history.mm", 'r')
time_sorted_history_file = open("../../data/tmp/_time_sorted_history.mm", 'w')

# sort <id_map_list> by old_id
sorted_id_map_list = misc_functions.sortMetaListByMeta(id_map_list, 0)

sorted_id_map_file = open("../../data/tmp/_sorted_id_map_file", 'w')
for line in sorted_id_map_list:
    sorted_id_map_file.write(line + "\n")
sorted_id_map_file.close()

# =====================
# DEBUG PRINT
print "sorted_id_map_list"
for i in range(10):
    print sorted_id_map_list[i]
print "===== \n"

# =====================

# copy comment strings to new history file
for i in range(3):
    time_sorted_history_file.write(old_history_file.readline())
    
"""
# === MAIN PART of sorting history
for i in range(len(sorted_id_map_list)):
    #print "line #", i
    line = old_history_file.readline()
    old_item_id = getMeta(line, 1)
    new_item_id = getMeta(sorted_id_map_list[old_item_id - 1], 1)
    # line to write
    ltw = getMetaString(line, 0) + "\t" + str(new_item_id) + "\t1\n"
    time_sorted_history_file.write(ltw)
"""

# === MAIN PART of sorting history
for line in old_history_file:
    #print "line #", i
    old_item_id = getMeta(line, 1)
    new_item_id = getMeta(sorted_id_map_list[old_item_id - 1], 1)
    # line to write
    ltw = getMetaString(line, 0) + "\t" + str(new_item_id) + "\t1\n"
    time_sorted_history_file.write(ltw)

time_sorted_history_file.close()
old_history_file.close()

# ===========================
#   sort history by user and item to look it more accurate
# ===========================

def cmpHistStr(line1, line2):
    """
    cmp string in file of history, supposing they must go in increasing
    order of first id (user) and second id (item)
    """

    if getMeta(line1, 0) == getMeta(line2, 0):
        return getMeta(line1, 1) - getMeta(line2, 1)
    else:
            return getMeta(line1, 0) - getMeta(line2, 0)


time_sorted_history_file = open("../../data/tmp/_time_sorted_history.mm", 'r')
finally_sorted_history_file = open("../../data/well_done/time_sorted_history.mm", 'w')
for i in range(3):
    finally_sorted_history_file.write(time_sorted_history_file.readline())

history_line_list = []
for line in time_sorted_history_file:
    history_line_list.append(line)

print "1"
sorted_history_line_list = sorted(history_line_list, cmpHistStr)
print "2"

for line in sorted_history_line_list:
    finally_sorted_history_file.write(line)

time_sorted_history_file.close()
finally_sorted_history_file.close()

id_map_file = open("../../data/tmp/sorted_id_map", 'w')
for line in sorted_id_map_list:
    id_map_file.write(line + "\n")
id_map_file.close()
    
