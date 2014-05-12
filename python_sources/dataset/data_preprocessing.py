import scipy
import scipy.io.mmio

import sys
if ".." not in sys.path:
    sys.path.insert(0, "..")

import misc_functions


# settings for dataset
trunk_dir = "../.."
dataset_dir = trunk_dir + "/data/datasets/"
dataset_name = "Timepad/raw"
history_file_name = dataset_dir + "/" + dataset_name + "/history.mm"
events_file_name = dataset_dir + "/" + dataset_name + "/events"
#users_file_name = dataset_dir + "/" + dataset_name + "/users"

MIN_EVENTS = 3  # minimum number of events for user to visit
                # to not be filtered out

TIME_META_POSITION = 7  # position of time stamp for event - 
                        # depends on meta data of events for
                        # current dataset

global_meta_list = []   # contains lines with meta data for events;
                        # used in several places in script;
                        # filled by <getGoodEvents> function

###################
# functions

def getGoodEvents():
    """
        get list of events ids that have meta data;
        IMPORTANT: fills list of meta data for events - global var <global_meta_list>
    """
    
    print "Getting list of events ids that have meta data..."

    events_file = open(events_file_name, 'r')
    events_with_meta_list = []

    for line in events_file:
        global_meta_list.append(line)

        event_id = misc_functions.getMeta(line, 0)
        if event_id not in events_with_meta_list:
            events_with_meta_list.append(event_id)
    
    events_file.close()
    
    print "Filtered events with meta data: ", len(events_with_meta_list)
    return events_with_meta_list
# end of getMetaEvents


def getGoodUsers():
    """
        get list of users ids that have visited greater or equal
        than <MIN_EVENTS> number of events
    """

    print "Getting list of users that have enough visits..."

    
    # fill dictionary of visits
    users_dict = {}
    
    history_file = open(history_file_name, 'r')
    # skip 3 lines of comments
    for i in range(3):
        history_file.readline()
    
    for line in history_file:
        user_id = misc_functions.getMeta(line, 0)
        item_id = misc_functions.getMeta(line, 1)
        
        if user_id in users_dict:
            users_dict[user_id].append(item_id)
        else:
            users_dict[user_id] = []

    # filter out users with less than <MIN_EVENTS> visits
    good_users_list = []
    for user_id in users_dict:
        if len(users_dict[user_id]) >= MIN_EVENTS:
            good_users_list.append(user_id)
    

    print "Filtered users with enough visits: ", len(good_users_list)
    return good_users_list
# end of getGoodUsers


def createNewUsersIDs(good_users_list):
    """
        create dictionary with key - old user ID, meaning - new user ID
    """
    
    print "Creating new IDs for users..."
    
    # start counting from 1
    new_user_id = 1

    users_IDs_map = {}
    
    for old_user_id in good_users_list:
        users_IDs_map[old_user_id] = new_user_id
        new_user_id += 1
    
    print "New IDs for users created."
    return users_IDs_map
# end of createNewUsersIDs


def createNewEventsIDs():
    """
        sorts events by time;
        creates dictionary with key - old event ID, meaning - new event ID
    """
    
    print "Creating new IDs for events..."
    
    print "Sorting events by time..."
    time_sorted_meta_list = misc_functions.sortMetaListByTime(global_meta_list, TIME_META_POSITION)
    
    # start counting from 1
    new_event_id = 1
    
    events_IDs_map = {}
    
    for event_line in time_sorted_meta_list:
        old_event_id = misc_functions.getMeta(event_line, 0)
        
        events_IDs_map[old_event_id] = new_event_id
        new_event_id += 1
    
    print "New IDs for events created."
    return [events_IDs_map, time_sorted_meta_list]
# end of createNewEventsIDs


def rewriteUsersData(users_IDs_map, good_users_list):
    """
        creates new file with users meta;
        in fact just replaces old users IDs with new IDs
    """
    print "Writing new users data..."

    users_file = open(users_file_name, 'r')
    
    good_users_lines = []
    
    for user_line in users_file:
        old_user_id = misc_functions.getMeta(user_line, 0)
        if old_user_id in good_users_list:
            rest_of_line = user_line[user_line.find('\t'):]
            good_users_lines.append(str(users_IDs_map[old_user_id]) + rest_of_line)

    users_file.close()
    
    # sort users lines by new user id
    sorted_users_lines = misc_functions.sortMetaListByMeta(good_users_lines, 0)
    
    # write new file with users data
    new_users_file = open(users_file_name + ".preprocessed", 'w')
    for user_line in sorted_users_lines:
        new_users_file.write(user_line)
    new_users_file.close()
    
    print "Users data with new IDs written."
# end of rewriteUsersData

def rewriteEventsData(events_IDs_map, time_sorted_meta_list):
    """
        creates new file with events meta;
        in fact just replaces old events IDs with new IDs;
        takes into account that seminars has been time sorted already
    """

    print "Writing new events data..."
    
    new_events_file = open(events_file_name + ".preprocessed", 'w')

    for event_line in time_sorted_meta_list:
        old_event_id = misc_functions.getMeta(event_line, 0)
        rest_of_line = event_line[event_line.find('\t'):]
        new_events_file.write(str(events_IDs_map[old_event_id]) + rest_of_line)

    new_events_file.close()
    
    print "Events data with new IDs and time-sorted events written."
# end of rewriteEventsData


def createVisitsMatrix( users_IDs_map,      events_IDs_map, \
                        good_users_list,    good_events_list):
    """
        creates new matrix of visits;
        
        result matrix contains only events with meta data
            and users with more than <MIN_EVENTS> visits each;
    """
    
    print "Creating new visits matrix..."
    
    old_history_file = open(history_file_name, 'r')

    
    # skip 3 lines of header
    for i in range(3):
        old_history_file.readline()
    
    new_history_lines = []
    
    for line in old_history_file:
        old_user_id  = misc_functions.getMeta(line, 0)
        old_event_id = misc_functions.getMeta(line, 1)
        
        if (old_user_id in good_users_list) and (old_event_id in good_events_list):
            ltw = str(users_IDs_map[old_user_id]) + '\t' + str(events_IDs_map[old_event_id]) + '\t' + '1' + '\n'
            new_history_lines.append(ltw)
    
    old_history_file.close()
    
    new_history_file = open(history_file_name + ".preprocessed", 'w')
    # write header for new history file
    new_history_file.write("%%MatrixMarket matrix coordinate integer general\n")
    new_history_file.write("%% Created by CTHULHU\n")
    new_history_file.write(str(len(good_users_list)) + '\t'  + \
                           str(len(good_events_list)) + '\t' + \
                           str(len(new_history_lines)) + '\n' )

    for line in new_history_lines:
        new_history_file.write(line)

    new_history_file.close()
    
    print "New visits matrix created."
# end of createVisitsMatrix


###############
# main script to run preprocess

print "Hello!\n"

good_events_list = getGoodEvents()
good_users_list = getGoodUsers()

users_IDs_map = createNewUsersIDs(good_users_list)
[events_IDs_map, time_sorted_meta_list] = createNewEventsIDs()

#rewriteUsersData(users_IDs_map, good_users_list)
rewriteEventsData(events_IDs_map, time_sorted_meta_list)

createVisitsMatrix( users_IDs_map,      events_IDs_map, \
                    good_users_list,    good_events_list )

print "\nFinished!\n"
