# this module implements _MAGICIAN_ framework for recommender system
# 
# framework plugs in:
#
#   ti (TIs) -  time intervals define behaviour of cross-validation
#               and data for cross-validation
#
#   dataset  -  object that describes type of data used and types
#               of events that are recommended
#
#   gear     -  module that realises recommendation algorythm
#
#   reporter -  (optional) module that logs work of magician
#
#   estimator-  (optional) module that run procedure of estimating
#               quality of recommendation
import os
import sys
import scipy
import scipy.io.mmio
import ConfigParser
import importlib

MAG_TRUNK_DIR = os.path.abspath("../..")
MAG_DATASET_DIR = MAG_TRUNK_DIR + "/data/datasets"
MAG_TI_DIR = MAG_TRUNK_DIR + "/data/time_intervals"
MAG_GEAR_DIR = "../gears"

if "../time_intervals_procedure" not in sys.path:
    sys.path.insert(0, "../time_intervals_procedure")
import TI


if "../dataset" not in sys.path:
    sys.path.insert(0, "../dataset")
import dataset

if ".." not in sys.path:
    sys.path.insert(0, "..")
import misc_functions

if "../gears" not in sys.path:
    sys.path.insert(0, "../gears")

if "../reporters" not in sys.path:
    sys.path.insert(0, "../reporters")

if "../estimators" not in sys.path:
    sys.path.insert(0, "../estimators")



class Magician:
    """
        Magician class implements frame for recommendation engines (Gears),
        reporter and estimator
    """
    
    def __init__(self, conf_file_name):
        """
            reads settings of TI from conf gile and sets the object
        """
        parser = ConfigParser.ConfigParser()
        parser.read(conf_file_name)
        
        # initialize TI by its contructor from its name from conf file
        self.ti = TI.TI(MAG_TI_DIR + "/" + parser.get("TI", "ti"))
        self.interval_size = int(parser.get("TI", "interval_size"))
        
        # load GEAR
        gear_module_name = parser.get("MODULES", "gear_module")
        if gear_module_name != "0":
            self.gear = importlib.import_module(gear_module_name)
            print "predict module <" + gear_module_name + "> loaded"
                
        # load REPORTER
        reporter_module_name = parser.get("MODULES", "reporter_module")
        if reporter_module_name != "0":
            self.reporter = importlib.import_module(reporter_module_name)
            print "reporter module <" + reporter_module_name + "> loaded"
        
        # load ESTIMATOR
        estimator_module_name = parser.get("MODULES", "estimator_module")
        if estimator_module_name != "0":
            self.estimator = importlib.import_module(estimator_module_name)
            print "estimator module <" + estimator_module_name + "> loaded"
        

        # set boolean settings for predict and estimate
        if parser.get("SETTINGS", "predict") == "true":
            self.need_predict = True
        else:
            self.need_predict = False
        
        if parser.get("SETTINGS", "estimate") == "true":
            self.need_estimate = True
        else:
            self.need_estimate = False
        
        # set file name for results log
        self.results_file_name = parser.get("SETTINGS", "results_file_name")
        
            
    # end of Magician.__init__
    
    def report(msg):
        """
            send message to the reporter if it is activated
        """
        if self.need_report:
            self.reporter.report(msg)
    # end of report
    
    def runCrossValidation(self):
        """
            launch cross validation procedure for loaded TI
        """
        
        ti_ctr = 1
        
        self.reporter.report("---")
        self.reporter.report("Cross-validation started\n")
        
        for interval_path in self.ti.intervals_list:
            
            self.reporter.report("  " + str(ti_ctr) + " of " + \
                str(len(self.ti.intervals_list)) + " intervals running")
            ti_ctr += 1
            
            self.interval_path = MAG_TI_DIR + "/" + interval_path

            self.window_coords = misc_functions.getWindowCoords(self.interval_path)

            if self.need_predict :
                train_matrix = scipy.io.mmio.mmread(MAG_TI_DIR + "/" + interval_path + "/train.mtx")
                self.reporter.report("    train mtx loaded")
                self.reporter.report("    prediction started")
                self.gear.predict(self, train_matrix)
            
            if self.need_estimate :
                test_matrix = scipy.io.mmio.mmread(MAG_TI_DIR + "/" + interval_path + "/test.mtx")
                self.reporter.report("    test mtx loaded")
                result_matrix = scipy.io.mmio.mmread(MAG_TI_DIR + "/" + interval_path + "/prediction.mtx")
                self.reporter.report("    results mtx loaded")
                self.reporter.report("    prediction started")
                self.estimator.estimate(self, test_matrix, result_matrix)
            
    # end of runCrossValidation

# end of Magician
