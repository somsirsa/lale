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

from imblearn.over_sampling import SMOTE as OrigModel
import lale.helpers
import lale.operators
from typing import Any, Dict, Optional

class SMOTEImpl():

    def __init__(self, sampling_strategy='auto', random_state=None, k_neighbors=5, n_jobs=1):
        self._hyperparams = {
            'sampling_strategy': sampling_strategy,
            'random_state': random_state,
            'k_neighbors': k_neighbors,
            'n_jobs': n_jobs}
    
        self._sklearn_model = OrigModel(**self._hyperparams) #calling it _sklearn_model due to legacy :)

    def fit(self, X, y=None):
        if (y is not None):
            self._sklearn_model.fit(X, y)
        else:
            self._sklearn_model.fit(X)
        return self

    def transform(self, X, y=None):
        if y is None:
            #If y is not passed, or it is passed as None, we assume this means resampling is not to be applied.
            return X, y
        else:
            #If a not None value is passed for y, this would mean a call during fit, and hence resampling to be done.
            return self._sklearn_model.fit_resample(X, y)

_input_fit_schema = {
  '$schema': 'http://json-schema.org/draft-04/schema#',
  'type': 'object',
  'required': ['X', 'y'],
  'additionalProperties': False,
  'properties': {
    'X': {
      'description': 'Features; the outer array is over samples.',
      'type': 'array',
      'items': {'type': 'array', 'items': {'type': 'number'}}},
    'y': {
      'description': 'Target class labels; the array is over samples.',
        'anyOf': [
            {'type': 'array', 'items': {'type': 'number'}},
            {'type': 'array', 'items': {'type': 'string'}}]}}}

_input_transform_schema = {
  '$schema': 'http://json-schema.org/draft-04/schema#',
  'type': 'object',
  'required': ['X', 'y'],
  'additionalProperties': False,
  'properties': {
    'X': {
      'description': 'Features; the outer array is over samples.',
      'type': 'array',
      'items': {'type': 'array', 'items': {'type': 'number'}}},
    'y': {
      'description': 'Target class labels; the array is over samples.',
      'laleType': 'Any'
}}}

_output_transform_schema:Dict[str, Any] = {}

_hyperparams_schema = {
    'allOf': [
    {   'type': 'object',
        'relevantToOptimizer': [],
        'additionalProperties': False,
        'properties': {
            'sampling_strategy': {
                'description': """sampling_strategy : float, str, dict or callable, default='auto'. 
Sampling information to resample the data set.
""",
                'anyOf': [
                    {   'description':"""When ``float``, 
it corresponds to the desired ratio of the number of 
samples in the minority class over the number of samples in the
majority class after resampling. Therefore, the ratio is expressed as
:math:`\\alpha_{os} = N_{rm} / N_{M}` where :math:`N_{rm}` is the
number of samples in the minority class after resampling and
:math:`N_{M}` is the number of samples in the majority class.
.. warning::
    ``float`` is only available for **binary** classification. An
    error is raised for multi-class classification.""",
                        'type': 'number'},
                    {   'description':"""When ``str``, specify the class targeted by the resampling. 
The number of samples in the different classes will be equalized.
Possible choices are:
``'minority'``: resample only the minority class;
``'not minority'``: resample all classes but the minority class;
``'not majority'``: resample all classes but the majority class;
``'all'``: resample all classes;
``'auto'``: equivalent to ``'not majority'``.""",
                        'enum': ['minority','not minority','not majority', 'all', 'auto']},
                    {   'description':"""- When ``dict``, the keys correspond to the targeted classes. 
The values correspond to the desired number of samples for each targeted
class.""",
                        'type': 'object'},
                    {   'description':"""When callable, function taking ``y`` and returns a ``dict``. 
The keys correspond to the targeted classes. The values correspond to the
desired number of samples for each class.""",
                        'laleType': 'Any'}],
                'default': 'auto'},
            'random_state': {
            'description':
                'Control the randomization of the algorithm.',
            'anyOf': [
                { 'description': 'RandomState used by np.random',
                'enum': [None]},
                { 'description': 'The seed used by the random number generator',
                'type': 'integer'},
                { 'description': 'Random number generator instance.',
                'laleType':'Any'}],
            'default': None},
            'k_neighbors':{
                'description': """If ``int``, number of nearest neighbours to used to construct synthetic samples.  
If object, an estimator that inherits from
:class:`sklearn.neighbors.base.KNeighborsMixin` that will be used to
find the k_neighbors.""",
                'anyOf': [
                    {'laleType':'Any'},
                    {'type': 'integer'}],
                'default': 5},
            'n_jobs': {
                'description': 'The number of threads to open if possible.',
                'type': 'integer',
                'default': 1}}}]}

_combined_schemas = {
  '$schema': 'http://json-schema.org/draft-04/schema#',
  'description': """ """,
  'documentation_url': '',
  'type': 'object',
  'tags': {
    'pre': ['~categoricals'],
    'op': ['resampler'],
    'post': []},
  'properties': {
    'hyperparams': _hyperparams_schema,
    'input_fit': _input_fit_schema,
    'input_transform': _input_transform_schema,
    'output_transform': _output_transform_schema,
}}

SMOTE = lale.operators.make_operator(SMOTEImpl, _combined_schemas)