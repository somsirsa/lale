# Copyright 2019 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import lale.docstrings
import lale.helpers
import lale.operators
import lale.type_checking
import functools
import numpy as np
import pandas as pd
import scipy.sparse
import lale.pretty_print
try:
    import torch
    torch_installed=True
except ImportError:
    torch_installed=False

class ConcatFeaturesImpl():
    def __init__(self):
        pass

    def transform(self, X):
        def is_pandas(d):
            return isinstance(d, pd.DataFrame) or isinstance(d, pd.Series)
        if functools.reduce(lambda accum, d: accum and is_pandas(d), X, True):
            result = pd.concat(X, axis=1)
            return result

        np_datasets = []
        #Preprocess the datasets to convert them to 2-d numpy arrays
        for dataset in X:
            if is_pandas(dataset):
                np_dataset = dataset.values
            elif isinstance(dataset, scipy.sparse.csr_matrix):
                np_dataset = dataset.toarray()
            elif torch_installed and isinstance(dataset, torch.Tensor):
                np_dataset = dataset.detach().cpu().numpy()
            else:
                np_dataset = dataset
            if hasattr(np_dataset, 'shape'):
                if len(np_dataset.shape) == 1: #To handle numpy column vectors
                    np_dataset = np.reshape(np_dataset, (np_dataset.shape[0], 1))
            np_datasets.append(np_dataset)
            
        result = np.concatenate(np_datasets, axis=1)
        return result

    def transform_schema(self, s_X):
        """Used internally by Lale for type-checking downstream operators."""
        min_cols, max_cols, elem_schema = 0, 0, None
        def add_ranges(min_a, max_a, min_b, max_b):
            min_ab = min_a + min_b
            if max_a == 'unbounded' or max_b == 'unbounded':
                max_ab = 'unbounded'
            else:
                max_ab = max_a + max_b
            return min_ab, max_ab
        for s_dataset in s_X['items']:
            if s_dataset.get('laleType', None) == 'Any':
                return {'laleType': 'Any'}
            arr_1d_num = {'type': 'array', 'items': {'type': 'number'}}
            arr_2d_num = {'type': 'array', 'items': arr_1d_num}
            s_decision_func = {'anyOf': [arr_1d_num, arr_2d_num]}
            if lale.type_checking.is_subschema(s_decision_func, s_dataset):
                s_dataset = arr_2d_num
            assert 'items' in s_dataset, lale.pretty_print.to_string(s_dataset)
            s_rows = s_dataset['items']
            if 'type' in s_rows and 'array' == s_rows['type']:
                s_cols = s_rows['items']
                if isinstance(s_cols, dict):
                    min_c = s_rows['minItems'] if 'minItems' in s_rows else 1
                    max_c = s_rows['maxItems'] if 'maxItems' in s_rows else 'unbounded'
                    elem_schema = lale.type_checking.join_schemas(elem_schema, s_cols)
                else:
                    min_c, max_c = len(s_cols), len(s_cols)
                    for s_col in s_cols:
                        elem_schema = lale.type_checking.join_schemas(elem_schema, s_col)
                min_cols, max_cols = add_ranges(min_cols,max_cols,min_c,max_c)
            else:
                elem_schema = lale.type_checking.join_schemas(elem_schema, s_rows)
                min_cols, max_cols = add_ranges(min_cols, max_cols, 1, 1)
        s_result = {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'array',
            'items': {
                'type': 'array',
                'minItems': min_cols,
                'items': elem_schema}}
        if max_cols != 'unbounded':
            s_result['items']['maxItems'] = max_cols
        lale.helpers.validate_is_schema(s_result)
        return s_result
    
_hyperparams_schema = {
    'allOf': [
      { 'description':
          'This first sub-object lists all constructor arguments with their '
          'types, one at a time, omitting cross-argument constraints, if any.',
        'type': 'object',
        'additionalProperties': False,
        'relevantToOptimizer': [],
        'properties': {}}]}

_input_transform_schema = {
    'type': 'object',
    'required': ['X'],
    'additionalProperties': False,
    'properties': {
        'X': {
            'description': 'Outermost array dimension is over datasets.',
            'type': 'array',
            'items': {
                'description': 'Middle array dimension is over samples (aka rows).',
                'type': 'array',
                'items': {
                    'description': 'Innermost array dimension is over features (aka columns).',
                    'anyOf': [{
                        'type': 'array',
                        'items': {
                            'type': 'number'},
                    }, {
                        'type': 'number'}]}}}}}

_output_transform_schema = {
    'description': 'Features; the outer array is over samples.',
    'type': 'array',
    'items': {
      'type': 'array',
      'description': 'Outer array dimension is over samples (aka rows).',
      'items': {
        'description': 'Inner array dimension is over features (aka columns).',
        'type': 'number'}}}

_combined_schemas = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': """Horizontal stacking concatenates features (aka columns) of input datasets.

Examples
--------
>>> A = [ [11, 12, 13],
...       [21, 22, 23],
...       [31, 32, 33] ]
>>> B = [ [14, 15],
...       [24, 25],
...       [34, 35] ]
>>> ConcatFeatures.transform([A, B])
NDArrayWithSchema([[11, 12, 13, 14, 15],
                   [21, 22, 23, 24, 25],
                   [31, 32, 33, 34, 35]])""",
    'documentation_url': 'https://lale.readthedocs.io/en/latest/modules/lale.lib.lale.concat_features.html',
    'type': 'object',
    'tags': {
        'pre': [],
        'op': ['transformer'],
        'post': []},
    'properties': {
        'hyperparams': _hyperparams_schema,
        'input_transform': _input_transform_schema,
        'output_transform': _output_transform_schema}}

if (__name__ == '__main__'):
    lale.helpers.validate_is_schema(_combined_schemas)

lale.docstrings.set_docstrings(ConcatFeaturesImpl, _combined_schemas)

ConcatFeatures = lale.operators.make_operator(ConcatFeaturesImpl, _combined_schemas)
