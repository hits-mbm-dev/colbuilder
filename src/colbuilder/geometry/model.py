import numpy as np
from  colbuilder.geometry import crosslink

class Model:
    """
    
    class for model that stores all relevant information about it:

    input   :   - id
                - transformation 
                - unit-cell 
                - neighbor contacts
                - fibril-id
                - class : crosslink 
                - type
                - mutate

    """
    def __init__(self,id=None,transformation=None,unit_cell=None,connect=None,
                 connect_id=None,pdb_file=None):
        self.id=id
        self.transformation=transformation
        self.unit_cell=unit_cell
        self.connect=connect
        self.connect_id=connect_id
        self.crosslink=self.add_crosslink(crosslink=crosslink.read_crosslink(pdb_file=pdb_file))
        self.type="".join(i for i in set([cross.type for cross in self.crosslink]))

    def add_connect(self,connect_id=None,connect=None):
        """
        
        add information about model's connections
        
        """
        self.connect_id=connect_id
        self.connect=connect
    
    def delete_connect(self,connect_id=None):
        """
        
        delete connect_id from model in system
        
        """
        self.connect=[i for i in self.connect if i !=connect_id]

    def add_crosslink(self,crosslink=None):
        """
    
        add and transform crosslink according to transformation matrix of model
    
        """
        try:
            for cross in crosslink:
                cross.set_transform(model_id=self.id,transform=self.transformation)

            self.cog=self.get_cog(crosslink=self.crosslink)
        except:
            crosslink=crosslink
        return crosslink

    def get_cog(self,crosslink=None):
        """
        
        get center-of-geometry of model
        
        """
        return np.mean([cross.position for cross in self.crosslink])

    def count_state(self,state=None):
        """
        
        count crosslinks with certain state (no, replace, protect) in model
        
        """
        return len([cross for cross in self.crosslink if cross.state==state])     