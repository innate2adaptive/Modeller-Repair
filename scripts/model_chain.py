import argparse
import os
from modeller import *
from modeller.automodel import *    # Load the automodel class

class MyModel(automodel):

	def set_lims(self, lim1, lim2):
		self.lim1 = str(lim1)
		self.lim2 = str(lim2)

	def select_atoms(self):
		if self.blank_single_chain:
			return selection(self.residue_range(self.lim1, self.lim2))
		else:
			chain = self.chains[0].name
			return selection(self.residue_range(self.lim1+":"+chain, self.lim2+":"+chain))

def args():
	parser = argparse.ArgumentParser(description='Fix missing atoms/residues with Modeller')
	parser.add_argument('-t', '--template_file', type=str, help='Template pdb file', required=True)
	parser.add_argument('-a', '--align_file', type=str, help='File containing sequence alignment information', required=True)
	parser.add_argument('-s', '--sel_range', type=int, nargs='+', help='Keep atoms/residues outside this range static (overrides automodeller class)', required=False)	
	return parser.parse_args()

def get_name_from_template_file(template_file):
	return os.path.splitext(os.path.basename(template_file))[0]

def read_align_data(align_file):
	align_data = []
	with open(align_file, "r") as afile:
		for i, line in enumerate(afile):
			line = line.rstrip()
			if line[0] == '>':
				protein_data = []
				p_start = i
				protein_data.append(line)
			if i == p_start + 1:
				protein_data.append(line)
			elif i == p_start + 2:
				protein_data.append(line)
				align_data.append(protein_data)
	return align_data

def get_seq_name_from_align_file(align_file):
	# assume first protein with type 'sequence' is desired model
	align_name = None
	align_data = read_align_data(align_file)
	for protein_data in align_data:
		if protein_data[1][:8].lower() == 'sequence':
			align_name = protein_data[0].split(';')[1]
			break
	return align_name


#def set_up_models(input_files, sel_range):
def	set_up_models(template_file, align_file, sel_range = None):
	template_path = os.path.dirname(os.path.abspath(template_file))
	align_path = os.path.dirname(os.path.abspath(align_file))

	template_name = get_name_from_template_file(template_file)
	seq_align_name = get_seq_name_from_align_file(align_file)

	if not template_path == align_path:
		print("Warning: template pdb and alignment file are not in same directory")
#	indir, pdb, alignf, known, seq = input_files
	log.verbose()
	env = environ()
	# directories for input atom files
	env.io.atom_files_directory = [template_path]

	if sel_range:
		lim1, lim2 = sel_range
		a = MyModel(env, alnfile = align_file,
              knowns = template_name, sequence = seq_align_name, assess_methods=(assess.DOPE))
		a.set_lims(lim1, lim2)
	else:
		a = automodel(env, alnfile = align_file,
              knowns = template_name, sequence = seq_align_name, assess_methods=(assess.DOPE))
	
	a.blank_single_chain = False
	return(a)

def create_models(a, start=1, end=10):
	a.starting_model= start
	a.ending_model  = end
	a.make()
	# Get a list of all successfully built models from a.outputs
	ok_models = list(filter(lambda x: x["failure"] is None, a.outputs))
	return ok_models

def get_top_model(ok_models):
	# Rank the models by DOPE score
	k = "DOPE score"
	ok_models.sort(key = lambda a: a[k])
	# get top model
	top_model = ok_models[0]
	print("Top model: %s (DOPE score %.3f)" % (top_model["name"], top_model[k]))
	return top_model

def write_log(models, logfile="dope.log", key = "DOPE score", sel_range=None):
	with open(logfile, "w") as logf:
		if sel_range:
			lim1, lim2 = sel_range
			logf.write("Repair limited between residues: " +  str(lim1) + "," +str(lim2) + "\n")
		else:
			logf.write("Repair not set to limited range of residues.\n")
		for m in models:
			logf.write(",".join([m['name'],str(m[key])])+"\n")
	print("log file written to " +  logfile)

def repair_structure(template_file, align_file, sel_range=None):
	#input_files = get_input_files(input_dir)
	#a = set_up_models(input_files, sel_range)
	a = set_up_models(template_file, align_file, sel_range)
	ok_models = create_models(a)
	top_model = get_top_model(ok_models)
	if sel_range:
		write_log(ok_models, sel_range=sel_range)
	else:
		write_log(ok_models)
	return ok_models

if __name__ == '__main__':
	args = args()
	ok_models = repair_structure(args.template_file, args.align_file, sel_range = args.sel_range)