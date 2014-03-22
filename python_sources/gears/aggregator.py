####
# Loading settings for current gear

import ConfigParser
import sys
import scipy

#sys.path.insert(0, "..")
import clusters
import misc_functions

parser = ConfigParser.ConfigParser()
parser.read("../gears/aggregator.conf")


interval_size_exe = int(parser.get("INTERVALS", "interval_size"))

#########


# TBD: add option to conf file later to get ability switch to different 
# systems of metrics

ndcg_clusters = True


# external function 
def predict(magician, train_matrix):
    """
        external function that will be called for gear launch
    """

    if ndcg_clusters:
        ndcgPrediction(magician, train_matrix)
    

def ndcgPrediction(magician, train_matrix):
    """
    
    """
    
    prediction_file_name = magician.interval_path + "/prediction.mtx"
    train_file_name      = magician.interval_path + "/train.mtx"
    
    clusters_list = clusters.getClustersListFromClustersFile(magician.interval_path, magician.interval_size)
    
    coords = misc_functions.getWindowCoords(magician.interval_path)
    
    test_users = range(coords[0], coords[1]) 
    test_items = range(coords[2], coords[3] + 1)
    
    prediction_matrix = scipy.zeros((len(test_users), len(test_items)), dtype = float)
    training_matrix = scipy.io.mmio.mmread(train_file_name).tocsr()
    
    # later?
    #item_X_meta_matrix = scipy.io.mmio.mmread("../../../well_done/items-metas_global.mtx").toarray()
    
    for user_cluster in clusters_list:
        user_id = int (user_cluster[0].split("\t")[1])
        #print "user #", user
        
        #user_metas = {} - changed to list because of problem with dimension
        user_metas = []
        
        
        #for item in test_items:
        for cluster in user_cluster[1 : ]:
            start_cluster_item = int(cluster.split("\t")[0])
            stop_cluster_item  = int(cluster.split("\t")[2])

            cluster_items = range(start_cluster_item, stop_cluster_item + 1)
            
            #for item in cluster_items:
        prediction_matrix[user_id - 1] = scipy.zeros((len(test_items)), dtype=float)
    
    # end of user-row cycle
    #########
    
    result_matrix = scipy.sparse.csr_matrix(prediction_matrix)
    scipy.io.mmio.mmwrite(prediction_file_name, result_matrix, field = 'real', precision = 5)

# end of 
