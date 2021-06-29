import os
import sys
import argparse
from Bio.PDB import *

def args():
	parser = argparse.ArgumentParser(description='Fix missing atoms/residues with Modeller')
	parser.add_argument('-p1', '--pdb1', type=str, help='Original pdb file', required=True)
	parser.add_argument('-p2', '--pdb2', type=str, help='Model pdb file', required=True)	
	parser.add_argument('-c', '--chains', type=str, nargs='+', help='Specify chains in original to replace with chains from model', required=False)	
	return parser.parse_args()

def parse_structures(original_pdb, model_chain_pdb):
	parser = PDBParser(QUIET=True, PERMISSIVE=0)
	original_structure = parser.get_structure("original_structure", original_pdb)
	model_structure = parser.get_structure("model_structure", model_chain_pdb)
	return original_structure, model_structure

def get_chains_from_model(model_structure):
	return [chain.id for chain in model_structure.get_chains()]

def replace_chains(chains, original_structure, model_structure):
	for c in chains:
		print("replacing chain:", c, 'in', original_structure.id, 'with chain', c, 'in',
				model_structure.id, " ...")
		new_chain = model_structure[0][c]
		# detach chains from original structure
		original_structure[0].detach_child(c)
		# attach modelled chain from modeller structure
		original_structure[0].add(new_chain)

def get_output_name_from_original(original_pdb):
	return os.path.splitext(original_pdb)[0] + "_repaired.pdb"

def save_merged_pdb(structure, output_pdb):
	io = PDBIO()
	io.set_structure(structure)
	io.save(output_pdb, preserve_atom_numbering=True)
	print("Structure saved to", output_pdb)

def check_chains_exist(structure, chains):
	structure_chains = [c.id for c in structure.get_chains()]
	for chain in chains:
		if chain not in structure_chains:
			print("Error: chain", chain, "not found in", structure.id)
			sys.exit()	

def create_new_structure(original_pdb, model_pdb, chains=None):
	original_structure, model_structure = parse_structures(original_pdb, model_pdb)
	if not chains:
		chains = get_chains_from_model(model_structure)
	check_chains_exist(original_structure,chains)
	check_chains_exist(model_structure,chains)
	replace_chains(chains, original_structure, model_structure)
	output_pdb = get_output_name_from_original(original_pdb)
	save_merged_pdb(original_structure, output_pdb)

if __name__ == '__main__':
	args = args()
	# note: args.chains must currently match id between original and model
	create_new_structure(args.pdb1, args.pdb2, args.chains)