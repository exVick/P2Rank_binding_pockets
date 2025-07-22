# P2Rank_binding_pockets
This is my solution for the Binding Pocket challenge 2025 in the AI Master's course *Structural Bioinformatics* at JKU Linz.

# Workflow

1. **Data Exploration** 

    To visualize the proteins I installed UCSF ChimeraX 1.9 from source. With a bit of manipulations of the PDB files one could also visualize the provided bindingpocket residues from the train.csv.
    
    In total we've got 16379 PDBs in train and 3064 PDBs in test dataset (to be predicted for the submission).

    The train.csv file contained the residues formatted like "chain_resid" and each row was linked to a protein via the "id". A few proteins had residues with additional information "xx", formatted like "chain_resid_xx"
    
    Below I analyzed how many of the proteins had the additional information residues.


2. **Data Preparation**

    PDB files were collected with their relative paths in a dataset for further modelling.

3. **Baseline**

    I decided to use P2Rank due to it's robustness and simplicity. The result was quite good, so I committed to improving the model as you can later see.
    
    Used scripts:

    - `my_metric.py`
    - `format_submissions.py`
    - `most_probable.py` 


4. **Evaluation**

    After local evaluation on the training set, I uploaded my predictions to the challenge server.


5. **Further Experiments**

    I wanted to finetune the RF model of P2Rank on our training dataset using it's internal functions. However, this attempt remains to be continued in future experiments
