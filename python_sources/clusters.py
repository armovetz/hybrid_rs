import datetime
import sys
#import ini
#from ini import *
import numpy


def ifTimeInterval(time_string1, time_string2, days_interval):
    time1 = datetime.datetime.strptime(time_string1, "%Y-%m-%d %H:%M:%S")
    time2 = datetime.datetime.strptime(time_string2, "%Y-%m-%d %H:%M:%S")
    
    """
    print "time1 = ", time1
    print "time2 = ", time2
    print "time1 - time2 = ", abs(time1 - time2)
    print "time1 - time2.days = ", (abs(time1 - time2)).days
    print "time1 - time2.hours = ", (abs(time1 - time2))
    exec("help(time1 - time2)")
    step()
    """
    
    if abs((time1 - time2)).days >= days_interval:
        return True
    else:
        return False
# end of ifTimeInterval

def getTimeInterval(item_id, item_X_time_list, coords, days_interval, items_numb):
    
    low_bound = -1
    high_bound = -1
    
    i = item_id
    
    #print "i=", i
    #print "days_interval = ", days_interval
    
    while not ifTimeInterval(item_X_time_list[i], item_X_time_list[item_id], days_interval):
        if (i - 1) < coords[1]:
            break
        i -= 1
    low_bound = i
    
    i = item_id
    #print "len(item_X_time_list) = ", len(item_X_time_list)
    #print "item_id = ", item_id
    #print items_numb
    while not ifTimeInterval(item_X_time_list[i], item_X_time_list[item_id], days_interval):
        if ((i + 1) > coords[3]) or ((i + 1) >= items_numb - 1):
            break
        i += 1
        #print "i = ", i
    high_bound = i
    
    return [low_bound, high_bound]
# end of getTimeInterval

def getClustersListFromClustersFile(interval_path, days_interval):
    
    clusters_file = open(interval_path + "/test_clusters_" + str(days_interval), 'r')
    
    # skip header 
    clusters_file.readline()
    user0 = int(clusters_file.readline().split("\t")[1]) 
    
    clusters_list = []
    cur_cluster = ["user" + "\t" + str(user0)]

    # reading clusters info to local lists
    for line in clusters_file:
        #print line

        # if new user
        if line.find("user") != -1:
            clusters_list.append(cur_cluster)
            cur_cluster = [line]
        else:
            cur_cluster.append(line)
    # appending last cluster
    clusters_list.append(cur_cluster)
    clusters_file.close()
    
    return clusters_list
# end of getClustersListFromClustersFile
