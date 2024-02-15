from colbuilder.sequence import alignment,system,modeller


def build_sequence(path_wd=str,pdb_file=None,collagen_type=int,
                      dict_chain={},register=[],crosslink={}):
    """
    
    build sequence from an uncrossed collagen triple helix
    
    """
    print('-- Building the sequence of the Collagen Triple Helix --')

    print('-- Read PDB-file --')
    system_=system.System(pdb_filename=pdb_file,collagen_type=collagen_type,register=register)
    system_.read_pdb(pdb_filename=pdb_file)
    system_.prepare_pdb(atoms=system_.atoms)
    system_.write_pdb(pdb_filename=pdb_file,atoms=system_.atoms,modified=True)

    print('-- Convert PDB to Fasta format --')
    system_.pdb_to_fasta(atoms=system_.atoms)

    print('-- Sequence Alignment with Muscle --')
    file_='tmp_'+"".join([i for i in register])
    alignment_=alignment.Alignment(atoms=system_.atoms,file=file_)
    alignment_.align_sequence(atoms=system_.atoms)

    print('-- Prepare triple helical structure with MODELLER --')
    
    modeller_=modeller.Modeller(system=system_,sequence=alignment_.sequence,file=file_,fasta=alignment_.fasta)
    modeller_.prepare_alignment(muscle_file=file_+'.afa',register=register)
    modeller_.write_alignment(alignment_file=file_+'_mod',system=system_)
    modeller_.check_alignment(alignment_file=file_+'_mod')