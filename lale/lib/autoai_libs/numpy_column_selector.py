# Copyright 2020 IBM Corporation
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
import autoai_libs.transformers.exportable

class NumpyColumnSelectorImpl():
    def __init__(self, columns):
        self._hyperparams = {
            'columns': columns}
        self._autoai_tfm = autoai_libs.transformers.exportable.NumpyColumnSelector(**self._hyperparams)

    def fit(self, X, y=None):
        return self._autoai_tfm.fit(X, y)

    def transform(self, X):
        return self._autoai_tfm.transform(X)

_hyperparams_schema = {
    'allOf': [{
        'description': 'This first object lists all constructor arguments with their types, but omits constraints for conditional hyperparameters.',
        'type': 'object',
        'additionalProperties': False,
        'required': ['columns'],
        'relevantToOptimizer': [],
        'properties': {
            'columns': {
                'description': 'List of indices to select numpy columns.',
                'anyOf': [
                {   'type': 'array',
                    'items': {'type': 'integer', 'minimum': 0}},
                {   'enum': [None]}],
                'default': None}}}]}

_input_fit_schema = {
    'type': 'object',
    'required': ['X'],
    'additionalProperties': False,
    'properties': {
        'X': {
            'type': 'array',
            'items': {'type': 'array', 'items': {'laleType': 'Any'}}},
        'y': {
            'laleType': 'Any'}}}

_input_transform_schema = {
    'type': 'object',
    'required': ['X'],
    'additionalProperties': False,
    'properties': {
        'X': {
            'type': 'array',
            'items': {'type': 'array', 'items': {'laleType': 'Any'}}}}}

_output_transform_schema = {
    'description': 'Features; the outer array is over samples.',
    'type': 'array',
    'items': {'type': 'array', 'items': {'laleType': 'Any'}}}

_combined_schemas = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': """Operator from `autoai_libs`_. Selects a subset of columns of a numpy array.

.. _`autoai_libs`: https://pypi.org/project/autoai-libs""",
    'documentation_url': 'https://lale.readthedocs.io/en/latest/modules/lale.lib.autoai.numpy_column_selector.html',
    'type': 'object',
    'tags': {
        'pre': [],
        'op': ['transformer'],
        'post': []},
    'properties': {
        'hyperparams': _hyperparams_schema,
        'input_fit': _input_fit_schema,
        'input_transform': _input_transform_schema,
        'output_transform': _output_transform_schema}}

if (__name__ == '__main__'):
    lale.helpers.validate_is_schema(_combined_schemas)

lale.docstrings.set_docstrings(NumpyColumnSelectorImpl, _combined_schemas)

NumpyColumnSelector = lale.operators.make_operator(NumpyColumnSelectorImpl, _combined_schemas)
