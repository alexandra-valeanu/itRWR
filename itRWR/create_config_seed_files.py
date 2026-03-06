import glob
from typing import Optional


def compute_layer_tau(layers: list, priorities: Optional[dict] = None) -> list:
    """Compute tau weights for multiplex layers based on optional priorities.
    
    If no priorities are provided, all layers receive equal weight (uniform distribution).
    If priorities are provided, weights are normalized to sum to 1.0 for the layers present.
    
    Args:
        layers: List of layer filenames (e.g., ['Coexpression.tsv', 'PPI.tsv'])
        priorities: Optional dict mapping layer names to relative priority values.
                   Keys can be with or without '.tsv' extension.
                   Example: {'PPI': 3, 'Complexes': 3, 'Pathways': 2, 'Coexpression': 1}
                   Higher values = higher priority/weight in the random walk.
                   Layers not in the dict get priority 1 (lowest).
    
    Returns:
        List of tau values (summing to 1.0) in the same order as input layers.
    
    Example:
        >>> compute_layer_tau(['PPI.tsv', 'Coexpression.tsv'])
        [0.5, 0.5]  # uniform when no priorities
        
        >>> compute_layer_tau(['PPI.tsv', 'Coexpression.tsv'], {'PPI': 3, 'Coexpression': 1})
        [0.75, 0.25]  # weighted by priorities
    """
    size = len(layers)
    if size == 0:
        return []
    
    # No priorities specified -> uniform distribution
    if priorities is None:
        return [1.0 / size] * size
    
    # Normalize priority keys (remove .tsv if present for matching)
    normalized_priorities = {}
    for key, value in priorities.items():
        clean_key = key.replace('.tsv', '')
        normalized_priorities[clean_key] = value
    
    # Compute raw weights for each layer
    raw_weights = []
    for layer in layers:
        layer_name = layer.replace('.tsv', '')
        # Default priority is 1 for layers not in the priorities dict
        weight = normalized_priorities.get(layer_name, 1)
        raw_weights.append(weight)
    
    # Normalize to sum to 1.0
    total = sum(raw_weights)
    if total == 0:
        return [1.0 / size] * size
    
    tau = [w / total for w in raw_weights]
    return tau


def build_seeds_file(orpha_seeds: str) -> dict:
    """Function to build seeds file from an input
    file containing ORPHANET disease IDs and
    their corresponding causative genes.
    These causative genes are taken as 
    seeds for the iterative random walk with 
    restart

    Args:
        orpha_seeds (str): name of
        the file containing ORPHANET codes 
        of diseases and their corresponding
        seeds

    Return :
        dict : a dictionary with ORPHANET codes
        as keys and the list of associated seeds 
        as values
    """
    dico_seeds = {}
    with open(orpha_seeds, 'r') as fi:
        for line in fi:
            values = line.strip().split("\t")
            if len(values) > 1:
                # separate diseases from seeds in the input file
                disease = line.split("\t")[0]
                seeds_rsplit = line.split("\t")[1].rsplit()
                seeds = [genes.split(",") for genes in seeds_rsplit]
                # initialize key in dico for disease
                dico_seeds[disease] = []
                # writing one seeds file for each set of seeds
                # we take the ORPHANET code of the disease to name the seeds files
                with open(f"seeds_{disease}.txt", 'w') as fo:
                    for list_genes in seeds:
                        for genes in list_genes:
                            # add set of seeds in dico
                            dico_seeds[disease].append(genes)
                            # write seeds in the output file
                            fo.write(genes + "\n")
        return dico_seeds


def build_config_files(path: str, dico_diseases_seeds: dict, layer_priority: Optional[dict] = None) -> None:
    """Function to build configuration files for each disease.

    Args:
        path (str): path of the working directory
        dico_diseases_seeds (dict): dictionary containing disease ORPHANET 
            identifiers and their associated seeds
        layer_priority (dict, optional): dictionary mapping layer names to 
            relative priority values. Keys can be with or without '.tsv' extension.
            Example: {'PPI': 3, 'Complexes': 3, 'Pathways': 2, 'Coexpression': 1}
            Higher values = higher weight in the random walk.
            If None, all layers have equal weight.

    Return:
        None
    """
    layers = glob.glob(path + '/multiplex/1/*')
    size = len(layers)
    layers = sorted([layers[i].split('/multiplex/1/')[1] for i in range(size)])

    # Compute tau values using the prioritisation function
    tau = compute_layer_tau(layers, layer_priority)

    for disease in dico_diseases_seeds:
        file = open(path + f'/config_{disease}.yml', 'w')
        r = 0.7
        delta = 0.5
        eta = 1.0

        file.write(f'seed: seeds_{disease}.txt' + '\n')
        file.write('self_loops: 0' + '\n')
        file.write('r: ' + str(r) + '\n')
        temp = '{},'*size
        part = '[' + temp.rstrip(',') +']'
        file.write('eta: ' + '[' + str(eta) + ']' + '\n')
        file.write('multiplex:' + '\n')
        
        file.write('    ' + str(1) + ':' + '\n' + '        ' + \
                        'layers:' + '\n' + '            ')
        for i in range(size) :
            if i < size - 1 :
                file.write('- multiplex/' + str(1) + '/' + layers[i] + '\n' + '            ' )
            else :
                file.write('- multiplex/' + str(1) + '/' + layers[i] + '\n' + '        ')
        file.write('delta: {}'.format(str(delta)) + '\n' + '        ' )
        file.write('graph_type: ' + '[' + ('00, '*size).rstrip(', ') + ']' + '\n' + '        ' )
        file.write('tau: ' + str(tau) + '\n')
        file.close