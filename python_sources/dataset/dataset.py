import ConfigParser

class Dataset:
    """
        Class represents dataset of historical and meta data - 
        corresponding to dataset stored in magical place
    """
    
    def __init__ (self, dataset_dir):     
        
        #print dataset_dir
        
        parser = ConfigParser.ConfigParser()
        parser.read(dataset_dir + "/dataset.conf")
        
        # PATHS
        self.name = dataset_dir + "/" + parser.get("PATHS", "name")
        self.history_file_name = dataset_dir + "/" + parser.get("PATHS", "history_file_name")
        self.events_file_name = dataset_dir + "/" + parser.get("PATHS", "events_file_name")
        
        # CONTENTS
        self.users_numb = int( parser.get("CONTENTS", "users_numb") )
        self.events_numb = int( parser.get("CONTENTS", "events_numb") )
        self.visits_numb = int( parser.get("CONTENTS", "visits_numb") )

        # METAS
        self.metas = parser.get("METAS", "metas")
        self.metas_enum = parser.get("METAS", "metas_enum")
        self.time_meta_position = int( parser.get("METAS", "time_meta_position") )
        
    # end of Dataset.__init__
    
    def printDataset(self):
        print "Name = ", self.name
        print "History file = ", self.history_file_name
        print "Meta file = ", self.meta_file_name
    
    
