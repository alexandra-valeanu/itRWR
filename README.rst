=============================================================================================
itRWR: MultiXrank-based Community Identification with Iterative Random Walk with Restart
=============================================================================================

.. image:: https://github.com/anthbapt/itRWR/workflows/CI/badge.svg
    :target: https://github.com/anthbapt/itRWR/actions?query=branch%3Amaster+workflow%3ACI
 
This repository presents an algorithm to perform an iterative Random Walk with Restart (itRWR) on a multiplex network (i.e., a network composed of multiple layers of interactions sharing the same nodes but different types of edges). Communities are identified around seed(s) defined as input.
itRWR is based on MultiXrank (https://github.com/anthbapt/multixrank), a Python package allowing Random Walk with Restart on universal multilayer networks (i.e., networks composed of any combination of multiplex and monoplex networks connected with their bipartite relationships).

-----------------
 Installation
-----------------

                                
.. code-block:: bash    

  $ python setup.py install

         
-----------------
 Library Codes
-----------------

* ``community.py``: Python script containing the function for community identification based on iterative Random Walk with Restart (itRWR)
* ``create_config_seed_files.py``: Python script to generate the configuration yml files and the files containing the seeds to be used for the Random Walk with Restart. To identify disease-associated communities, for instance, the seeds can be the disease-causative gene(s)
* ``run_community_ID.py``: Main Python script containing the function to automatize the community identification for different sets of node(s) used as seed(s)


-----------------
Data
-----------------


``ToyExample/multiplex``: This folder contains a toy example of a multiplex biological network composed of five layers of interactions (PPI, Pathways, Co-expression, Complexes, Disease involvement). This toy subset has been extracted from the complete multiplex network, which layers are available on the NDEX server: `<https://www.ndexbio.org/index.html#/search?searchType=All&searchString=cecile.beust&searchTermExpansion=false>`_

``data/orpha_codes_PA.txt``: File containing Premature Aging disease identifiers and their associated causative genes from ORPHANET (`<https://www.orpha.net/consor4.01/www/cgi-bin/?lng=ENG>`_). The disease causative genes are used as seed(s) in our analysis

-----------------
Usage
-----------------

Make sure that the networks you wish to use are stored in a folder named ``multiplex/1/`` in your current directory.
After having checked and/or modified the script parameters in accordance with your data, set the desired number of iterations for itRWR and run the following Python code: 

.. code-block:: python

    from itRWR import community_identification 
    import os

    path = os.path.dirname(os.path.realpath(__file__))
    path = path + '/'
    os.chdir(path)

    list_disease = "orpha_codes_PA.txt"
    num_iteration = 10
    community_identification(path, list_disease, num_iteration)


This will create a seed file, a configuration file, and output folders needed for each community. For instance, the community identified for a given disease will be contained in the file ``seeds_ID.txt`` (In this example, ID is the ORPHANET identifier of the disease) inside the corresponding output folder.

--------------------------
Layer Prioritisation
--------------------------

By default, all layers in the multiplex network are weighted equally in the random walk. You can prioritize specific layers by passing a ``layer_priority`` dictionary to the ``community_identification`` function. Higher values correspond to higher weights in the random walk.

**Basic usage (uniform weights):**

.. code-block:: python

    # All layers have equal weight
    community_identification(path, list_disease, num_iteration)

**With layer prioritisation:**

.. code-block:: python

    # Define priorities: higher values = higher weight in the random walk
    layer_priority = {
        'PPI': 3,           # High priority
        'Complexes': 3,     # Same priority as PPI
        'Pathways': 2,      # Medium priority
        'Coexpression': 1,  # Low priority
        'Diseases_involvement': 1,  # Low priority
    }
    
    community_identification(path, list_disease, num_iteration, layer_priority)

**How it works:**

- Priorities are relative values that get normalized to sum to 1.0
- Example: ``{PPI: 3, Complexes: 3, Pathways: 2, Coexpression: 1, Diseases_involvement: 1}`` → tau = ``[0.1, 0.3, 0.1, 0.3, 0.2]``
- Layer names can be specified with or without the ``.tsv`` extension
- Layers not included in the dictionary receive a default priority of 1
- If some layers are not present in your multiplex network, they are simply ignored

**Usage:**

.. code-block:: python
    
    from itRWR import community_identification 
    import os

    path = os.path.dirname(os.path.realpath(__file__))
    path = path + '/'
    os.chdir(path)

    list_disease = "orpha_codes_PA.txt"
    num_iteration = 10

    # Optional: Define layer priority for the random walk
    layer_priority = {
        'PPI': 3, 
        'Complexes': 3,
        'Pathways': 2,
        'Coexpression': 1,
        'Diseases_involvement': 1,
    }

    community_identification(path, list_disease, num_iteration, layer_priority)

-----------------
Example
-----------------
To test the algorithm on a simple example you can run the version of the script ``run.py`` contained in the ``ToyExample`` folder. This will apply community identification for one disease, Hutchinson-Gilford Progeria Syndrome (ORPHANET code: 740), using its two causative genes (LMNA and ZMPSTE24) as seeds, on the toy multiplex network, with a number of iterations set to 10 for the itRWR algorithm. 

This simple example will generate the following output folder ``results_10_740`` containing the following files:

* ``config.yml``: a copy of the configuration file for the disease
* ``multiplex_1.tsv``: a file containing the ranking for each node of the multiplex network after the itRWR algorithm has been applied
* ``seeds_740.txt``: a file containing the nodes of the community identified for the disease. Since we applied 10 iterations of the algorithm, and that the disease has 2 starting seeds, the obtained final community contains 12 nodes. 


-----------------
References
-----------------
* Baptista, A., Gonzalez, A. & Baudot, A. Universal multilayer network exploration by random walk with restart. en. Communications Physics 5, 170. ISSN: 2399-3650. doi:10.1038/s42005-022-00937-9 (July 2022).

* Rath, A. et al. Representation of rare diseases in health information systems: The orphanet approach to serve a wide range of end users. Human Mutation 33, 803–808. ISSN:10597794. doi:10.1002/humu.22078 (2012)
