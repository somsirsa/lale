
from sklearn.impute import MissingIndicator as SKLModel
import lale.helpers
import lale.operators
from numpy import nan, inf

class MissingIndicatorImpl():

    def __init__(self, missing_values='nan', features='missing-only', sparse='auto', error_on_new=True):
        self._hyperparams = {
            'missing_values': missing_values,
            'features': features,
            'sparse': sparse,
            'error_on_new': error_on_new}

    def fit(self, X, y=None):
        self._sklearn_model = SKLModel(**self._hyperparams)
        if (y is not None):
            self._sklearn_model.fit(X, y)
        else:
            self._sklearn_model.fit(X)
        return self

    def transform(self, X):
        return self._sklearn_model.transform(X)
_hyperparams_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'inherited docstring for MissingIndicator    Binary indicators for missing values.',
    'allOf': [{
        'type': 'object',
        'required': ['missing_values', 'features', 'sparse', 'error_on_new'],
        'relevantToOptimizer': [],
        'additionalProperties': False,
        'properties': {
            'missing_values': {
                'anyOf': [{'type': 'number'},
                          {'type': 'string'},
                          {'enum': [nan]},
                          {'enum': [None]}],
                'description': 'The placeholder for the missing values.',
                'type': 'number',
                'default': nan},
            'features': {
                'type': 'string',
                'default': 'missing-only',
                'description': 'Whether the imputer mask should represent all or a subset of'},
            'sparse': {
                'anyOf': [{'type': 'boolean'},
                          {'enum': ['auto']}],
                'description': 'Whether the imputer mask format should be sparse or dense.',
                'default': 'auto'},
            'error_on_new': {
                'type': 'boolean',
                'default': True,
                'description': 'If True (default), transform will raise an error when there are'},
        }}, {
        'description': 'error_on_new, only when features="missing-only"',
        'anyOf': [{
            'type': 'object',
            'properties': {
                'error_on_new': {
                    'enum': [True]},
            }}, {
            'type': 'object',
            'properties': {
                'features': {
                    'enum': ['missing-only']},
            }}]}],
}
_input_fit_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Fit the transformer on X.',
    'type': 'object',
    'required': ['X'],
    'properties': {
        'X': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': 'number'},
            },
            'description': 'Input data, where ``n_samples`` is the number of samples and'},
    },
}
_input_transform_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Generate missing values indicator for X.',
    'type': 'object',
    'required': ['X'],
    'properties': {
        'X': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': 'number'},
            },
            'description': 'The input data to complete.'},
    },
}
_output_transform_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'The missing indicator for input data.',
    'type': 'array',
    'items': {'type': 'array', 
        'items':{
            'type': 'boolean'}}
}
_combined_schemas = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Combined schema for expected data and hyperparameters.',
    'documentation_url': 'https://scikit-learn.org/0.20/modules/generated/sklearn.impute.MissingIndicator.html#sklearn-impute-missingindicator',
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
MissingIndicator = lale.operators.make_operator(MissingIndicatorImpl, _combined_schemas)

