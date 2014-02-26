import datetime
import sys
import ini
from ini import *
import numpy

def gag():

    print "!!!!!!!!!!!!!!!!!"
    print " SHAME ON YOU!!!!"
    print " It'S A GAG!!!!!!"
    print "!!!!!!!!!!!!!!!!!"

def getEventDatetime(event_str, time_position):
    """
    
    """
    
    event_time_str = split
    
# end of getEventDatetime

def dayTime(date_string):
    time = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    
    if time.hour < 0:
        raise Exception("FUCK")
    
    if (time.hour >= 0) and (time.hour <= 7):
        return 1
    elif (time.hour > 7) and (time.hour <= 12):
        return 2
    elif (time.hour > 12) and (time.hour <= 16):
        return 3
    elif (time.hour > 16) and (time.hour <= 20):
        return 4
    elif (time.hour > 20):
        return 5
        
def priceToPriceCat(rubles):
    if rubles < 0:
        raise Exception("Negative price: " + str(rubles))
            
    if rubles == 0:
        return 1
    elif (rubles > 0) and (rubles <= 100):
        return 2
    elif (rubles > 100) and (rubles <= 500):
        return 3
    elif (rubles > 500) and (rubles <= 1000):
        return 4
    elif (rubles > 1000) and (rubles <= 5000):
        return 5
    else:
        return 6


def getMeta(seminar_meta_string, meta_position_id):
    
    #print "GET META"
    #print "meta_position_id = ", meta_position_id
    #print "seminar_meta_string = ", seminar_meta_string
    #step()
    
    # DAYTIME
    if meta_position_id == 17:
        stri = seminar_meta_string.split('\t')[5]
        return dayTime(stri)
    
    stri = seminar_meta_string.split('\t')[meta_position_id]
    try:
        int(stri)
    except ValueError:
        return 0
    
    if stri == "" or (int(stri) < 0):
        return 0
    else:
        return int(stri)
        
def getMetaString(seminar_meta_string, meta_position_id):
    return seminar_meta_string.split('\t')[meta_position_id]


def getWindowCoords(path = "."):
    window_coords_file = open(path + "/window_coords", 'r')
    coords = []
    for line in range(4):
        coords.append(int(window_coords_file.readline().split()[2]))
    window_coords_file.close()
    return coords

def sortMetaListByTime(meta_list, time_meta_position):
    
    def cmpTime(op1, op2):
        """
            compares time, that is written in format YYYY-MM-DD HH:MM:SS 
        """
        time_string1 = op1.split('\t')[time_meta_position]
        time_string2 = op2.split('\t')[time_meta_position]
        time1 = datetime.datetime.strptime(time_string1, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime(time_string2, "%Y-%m-%d %H:%M:%S")
        if time1.__ge__(time2):
            return 1
        else:
            return -1

    return sorted(meta_list, cmpTime)
# enf of sortMetaListByTime

def sortMetaListByMeta(meta_list, meta_id_position):
    
    def my_cmp(op1, op2):
        if op1.split('\t')[meta_id_position] == "":
            return -1
        if op2.split('\t')[meta_id_position] == "":
            return 1
        return int(op1.split('\t')[meta_id_position]) - int(op2.split('\t')[meta_id_position])

    def cmpTime(op1, op2):
        """ compares time, that is written in format YYYY-MM-DD HH:MM:SS """
        time_string1 = op1.split('\t')[5]
        time_string2 = op2.split('\t')[5]
        time1 = datetime.datetime.strptime(time_string1, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime(time_string2, "%Y-%m-%d %H:%M:%S")
        if time1.__ge__(time2):
            return 1
        else:
            return -1
            
    def cmpHour(op1, op2):
        """ compares time, that is written in format YYYY-MM-DD HH:MM:SS """
        time_string1 = op1.split('\t')[5]
        time_string2 = op2.split('\t')[5]
        time1 = datetime.datetime.strptime(time_string1, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime(time_string2, "%Y-%m-%d %H:%M:%S")
        if time1.hour >= time2.hour:
            return 1
        else:
            return -1

    """
    # PRICE HEURISTIC IMPLEMENTING
    price_meta_list = list(meta_list)
    if meta_id_position == 8:
        for line in price_meta_list:
            if (line.split('\t')[meta_id_position] == "") or (line.split('\t')[meta_id_position] == 0)
    """
    # TIME COMPARE
    if meta_id_position == 5:
        # if we need to sort list by time
        return sorted(meta_list, cmpTime)
    elif meta_id_position == 17:
        # sort by dayTime
        return sorted(meta_list, cmpHour)
    else:
        return sorted(meta_list, my_cmp)
        
def cmpTime(time_string1, time_string2):
        """ compares time, that is written in format YYYY-MM-DD HH:MM:SS """
        
        time1 = datetime.datetime.strptime(time_string1, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime(time_string2, "%Y-%m-%d %H:%M:%S")
        if time1.__ge__(time2):
            return 1
        else:
            return -1
            
def ifTimeInterval(time_string1, time_string2):
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
    
    if abs((time1 - time2)).days >= DAYS_INTERVAL_PREPARE:
        return True
    else:
        return False

def getTimeInterval(item_id, item_X_time_list, coords):
    
    low_bound = -1
    high_bound = -1
    
    i = item_id
    while not ifTimeInterval(item_X_time_list[i], item_X_time_list[item_id]):
        if (i - 1) < coords[1]:
            break
        i -= 1
    low_bound = i
    
    i = item_id
    #print "len(item_X_time_list) = ", len(item_X_time_list)
    #print "item_id = ", item_id
    while not ifTimeInterval(item_X_time_list[i], item_X_time_list[item_id]):
        if ((i + 1) > coords[3]) or ((i + 1) >= ITEMS_NUMB - 1):
            break
        i += 1
        #print "i = ", i
    high_bound = i
    
    return [low_bound, high_bound]
    
def step():
    print "Press any key to continue:"
    sys.stdin.read(1)


def cosineSimilarity(vec1, vec2):
    result = float(numpy.dot(abs(vec1), abs(vec2)))

    denominator = (float(numpy.sum(abs(vec1) ** 2)) ** 0.5) * (float(numpy.sum((vec2) ** 2)) ** 0.5)
    
    if denominator == 0.0:
        return 0
    else:
        return (result / denominator)

def getClustersListFromClustersFile(days_interval):
    
    clusters_file = open("test_clusters_" + str(days_interval), 'r')
    
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
