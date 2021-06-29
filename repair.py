import argparse
import os
import scripts.model_chain as model
import scripts.replace_chain as replace

def args():
	parser = argparse.ArgumentParser(description='Fix missing atoms/residues with Modeller')
	parser.add_argument('-t', '--template_file', type=str, help='Template pdb file', required=True)
	parser.add_argument('-a', '--align_file', type=str, help='File containing sequence alignment information', required=True)
	parser.add_argument('-s', '--sel_range', type=int, nargs='+', help='Keep atoms/residues outside this range static (overrides automodeller class)', required=False)	
	return parser.parse_args()

# note: protocol currently only works for repairing a single chain at a time
if __name__ == '__main__':
	args = args()
#	# create models of chain to be repaired
	models = model.repair_structure(args.template_file, args.align_file, sel_range = args.sel_range)
	# create new pdb of top model of chain merged with tempate 
	replace.create_new_structure(args.template_file, models[0]['name'])