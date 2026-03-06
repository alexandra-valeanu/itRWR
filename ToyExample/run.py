#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from itRWR import community_identification
import os

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

diseases = "orpha_codes_toy_ex.txt"
num_iteration = 10

# Optional: Define layer priority for the random walk
# Higher values = higher weight. Layers not listed get priority 1 (lowest).
# If set to None, all layers have equal weight (uniform distribution).
layer_priority = {
    'PPI': 3,           # High priority (physical  interactions)
    'Complexes': 3,     # High priority (same as PPI - physical  interactions)
    'Pathways': 2,      # Medium priority
    'Coexpression': 1,  # Low priority
    'Diseases_involvement': 1,  # Low priority
}

community_identification(path, diseases, num_iteration, layer_priority)
