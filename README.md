# Modeller-Repair

Repository for repairing protein structures with missing residues or residues with missing atoms using Modeller.

Used to repair subset of benchmark TCR and pMHC structures found in [https://github.com/innate2adaptive/ExpandedBenchmark](https://github.com/innate2adaptive/ExpandedBenchmark), which feature in the publication [Peacock and Chain (2021)](https://doi.org/10.3389/fimmu.2021.686127).

## Install Modeller with Conda

* Obtain a Modeller license key, [following Modeller registration instructions](https://salilab.org/modeller/registration.html) 

* If conda is installed, create a new virtual environment (initial install only):

  ```bash
  conda create --name modeller python=3.7
  ```
* activate your new virtual environment:
 
  ```bash
  source activate modeller
  ```
* Install Modeller:

  ```bash
  conda install -c salilab modeller
  ```
* Follow instructions provided when running previous command to add your Modeller license key to the Modeller config file (should be similiar to `/home/usr/conda/envs/modeller/lib/modeller-10.1/modlib/modeller/config.py`).

* Install Biopython:
  ```bash
  conda install -c conda-forge biopython
  ```
## Repairing a structure

The `repair.py` script can be used to repair protein structures with missing residues.

The structure can be repaired using:
  ```bash
  python repair.py -t template.pdb -a alignment.ali
  ```
where the `-t` argument provides the template structure with missing residues, and the `-a` argument provides the alignment file, containing the desired chain sequence and the names of the template and output pdb files (see section below for an example).

The modelling can be limited to a specific region of the structure by using the `-s` argument:
  ```bash
  python repair.py -t template.pdb -a alignment.ali -s 20 26
  ```
where `20` and `26` can be replaced with the start and end residue number from the template pdb file.

## Example

The process of repairing a structure is illustrated using an example provided in this repository.

The `example` directory contains the following files:

* `2nx5_r_u.pdb` is pdb file containing data relating to the structure of an unbound T cell receptor protein. This structure is taken from the set of TCR Benchmark structures that can be found in the `raw` directory of the [Expanded Benchmark Repository](https://github.com/innate2adaptive/ExpandedBenchmark). This file is missing the residue `SER.95` and neighbouring atoms in residues `ALA.94` and `GLY.96`  in a region of the protein `A` chain that is critical to its function.

* `2nx5_r_u_processed.pdb` is a cleaned version of the `2nx5_r_u.pdb` file described above. The solvent atoms have been removed, as have the incomplete `ALA.94` and `GLY.96` residues.

* `2nx5_r_u.ali` contains the PIR format required by Modeller for homology modelling. The first three lines provide information about the processed template structure and sequence. Gaps are included in the sequence for the residues that need to be repaired. The second three lines provide information about the correct sequence required in the output models. Further details for customising this file can be found in the Modeller documentation about the [Alignment file format](https://salilab.org/modeller/8v2/manual/node176.html).

The structure can be repaired around this region by entering the `example` directory and using the `repair.py` script:
```bash
cd example && python ../repair.py -t 2nx5_r_u_processed.pdb -a 2nx5_r_u.ali -s 94 96
```
This will produce 10 models of the repaired chain and then replace the broken chain in the template with the best model (ranked by Modeller DOPE score).

The final repaired model is saved to `2nx5_r_u_processed_repaired.pdb`

