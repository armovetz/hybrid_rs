import sys
import os

if ".." not in sys.path:
    sys.path.insert(0, "..")
import misc_functions

# file with events meta descriptions
dataset_dir = "../../data/datasets"
dataset_name = "Timepad/raw"
events_file_name = "events.preprocessed"
events_file = open(dataset_dir + "/" + dataset_name + "/" + events_file_name, 'r')

# file to save new meta lines
meta_numb = 8
#meta_name = "headers"
meta_file = open(dataset_dir + "/" + dataset_name + "/times", 'w')

for line in events_file:
    ltw = ""
    #print line
    
    #id = misc_functions.getMeta(line, 0)
    #ltw = ltw + str(id) + '\t'
    
    meta = str( misc_functions.getMeta(line, meta_numb) )
    ltw += meta
    
    meta_file.write(ltw + '\n')
    
events_file.close()
meta_file.close()
