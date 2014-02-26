import numpy
import scipy

def estimate(magician, test_matrix, result_matrix):
    """
        function estimates overwhole procents of wrong predictions.
        It's very simple.
    """

    test_matrix_csr = test_matrix.tocsr()
    result_matrix_csr = result_matrix.tocsr()
    
    matrix_size = test_matrix_csr.shape[0] * test_matrix_csr.shape[1]
    
    diff_matrix_csr = (test_matrix_csr - result_matrix_csr).__abs__()
    
    percents = 100.0 * (float(diff_matrix_csr.sum()) / float(matrix_size))
    
    magician.reporter.report("RESULT = " + str(percents))


# end of estimate
