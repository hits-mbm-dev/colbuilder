import numpy as np

class System:
    """

    base class representing a system of models 
    dict { model_id: model }

    """
    def __init__(self,crystal=None,crystalcontacts=None,pdb_fibril=str):
        self.system={ }
        self.connect={ }
        self.models=[]
        self.crystal=crystal
        self.crystalcontacts=crystalcontacts
        self.size_models=0
        self.is_line=('ATOM  ', 'HETATM', 'ANISOU', 'TER   ')
        self.size=0
        self.type=''
        self.pdb_fibril=pdb_fibril

    def add_model(self,model):
        """

        add model to the system
        
        """
        self.system.update({model.id : model})
    
    def set_crystal(self,crystal=None):
        """
        
        set crystal information for model
        
        """
        if crystal==None: crystal=self.crystal
        for model in self.system:
            self.system[model].crystal=crystal       

    def get_size(self,system=None):
        """
        
        get length of system
        
        """
        self.size=len(self.system)
        return self.size
    
    def get_connect_size(self,system=None):
        """
        
        get length of system with only connected models
        
        """
        return len([model for model in self.models if self.get_model(model_id=model).connect!=None])
    
    def get_model(self,model_id=None):
        """
        
        get model from system by id
        
        """
        return self.system[model_id]
    
    def get_models(self):
        """

        get models from system
        
        """
        self.models=[model for model in self.system]
        return self.models

    def get_connect(self,connect=None):
        """
        
        get crystal contacts for a model in system
        
        """
        self.connect={ self.get_model(model_id=key).id : [] for key in self.get_models() } 
        for idx in self.get_models():
            self.connect[self.get_model(model_id=idx).id]=self.get_model(model_id=idx).connect
        return self.connect

    def delete_model(self,model_id=int):
        """
        
        delete model in system
        
        """
        del self.system[model_id]
        return self.system
    
    def translate_system(self,crystal=None,center=None):
        """
    
        translate the whole system to a certain position (0,0,400)
    
        """
        translate=[0,0,center[2]-self.center_system(crystal=crystal)]
        for model_id in self.get_models():
            if self.get_model(model_id=model_id).connect!=None:
                for connect_id in self.get_model(model_id=model_id).connect:
                    crystal.translate_crystal(pdb=self.get_model(model_id=model_id).type+"/"+str(int(connect_id))+".caps",
                                              translate=translate,bool_system=True)
    
    def center_system(self,crystal=None):
        """
        
        center system at a certain position, we use (x,y,z)=(0,0,400)
        
        """
        cog=[]
        for model_id in self.get_models():
            if self.get_model(model_id=model_id).connect!=None:
                for connect_id in self.get_model(model_id=model_id).connect:
                    cog.append(crystal.get_cog(pdb=self.get_model(model_id=model_id).type+"/"+str(int(connect_id))+".caps"))
        return np.mean(cog)

    def count_states(self,state=str):
        """
        
        counts all models with certain state (no, mut, prot)
        
        """
        cnt=0
        for key in self.get_models():
            cnt+=self.get_model(model_id=key).count_state(state=state)
        return cnt

    def write_pdb(self,pdb_out=str,fibril_length=float):
        """
        
        writes system to a pdb-file 
        
        """
        with open(pdb_out+'.pdb','w') as f:
            f.write(open(self.crystal.pdb_file+'.pdb').readline())
            for model in self.get_models():
                if self.get_model(model_id=model).connect!=None:
                    if len(self.get_model(model_id=model).connect)!=1 or fibril_length<=float(300):
                        for connect in self.get_model(model_id=model).connect:
                            pdb_model=open(str(self.get_model(model_id=model).type)+'/'+str(int(connect))+'.caps.pdb','r').readlines()
                            f.write("".join(i for i in pdb_model if i[0:6] in self.is_line and i[0:3]!='TER'))
            f.write("END")
        f.close()