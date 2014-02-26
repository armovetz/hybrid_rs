import numpy
import scipy

def predict(magician, train_matrix):
    """
        function that gives random predictions
    """
    
    start_user = magician.window_coords[0]
    stop_user  = magician.window_coords[1]
    start_item = magician.window_coords[2]
    stop_item  = magician.window_coords[3]
    
    test_users = range(start_user, stop_user) 
    test_items = range(start_item, stop_item + 1)
    
    prediction_matrix = numpy.ones((len(test_users), len(test_items)), dtype = int)
    
    magician.reporter.report("    matrix gen passed")
    
    matrix_to_save = scipy.sparse.csr_matrix(prediction_matrix)
    
    magician.reporter.report("    matrix compressed to csr format")
    
    scipy.io.mmio.mmwrite(magician.interval_path + "/results.mtx", matrix_to_save, field = 'integer')
    
    magician.reporter.report("    matrix saved")

# end of predict
