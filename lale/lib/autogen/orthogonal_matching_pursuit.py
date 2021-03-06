
from sklearn.linear_model.omp import OrthogonalMatchingPursuit as SKLModel
import lale.helpers
import lale.operators
from numpy import nan, inf

class OrthogonalMatchingPursuitImpl():

    def __init__(self, n_nonzero_coefs=None, tol=None, fit_intercept=True, normalize=True, precompute='auto'):
        self._hyperparams = {
            'n_nonzero_coefs': n_nonzero_coefs,
            'tol': tol,
            'fit_intercept': fit_intercept,
            'normalize': normalize,
            'precompute': precompute}
        self._sklearn_model = SKLModel(**self._hyperparams)

    def fit(self, X, y=None):
        if (y is not None):
            self._sklearn_model.fit(X, y)
        else:
            self._sklearn_model.fit(X)
        return self

    def predict(self, X):
        return self._sklearn_model.predict(X)
_hyperparams_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'inherited docstring for OrthogonalMatchingPursuit    Orthogonal Matching Pursuit model (OMP)',
    'allOf': [{
        'type': 'object',
        'required': ['n_nonzero_coefs', 'tol', 'fit_intercept', 'normalize', 'precompute'],
        'relevantToOptimizer': ['n_nonzero_coefs', 'tol', 'fit_intercept', 'normalize', 'precompute'],
        'additionalProperties': False,
        'properties': {
            'n_nonzero_coefs': {
                'anyOf': [{
                    'type': 'integer',
                    'minimumForOptimizer': 500,
                    'maximumForOptimizer': 501,
                    'distribution': 'uniform'}, {
                    'enum': [None]}],
                'default': None,
                'description': 'Desired number of non-zero entries in the solution'},
            'tol': {
                'anyOf': [{
                    'type': 'number',
                    'minimumForOptimizer': 1e-08,
                    'maximumForOptimizer': 0.01,
                    'distribution': 'uniform'}, {
                    'enum': [None]}],
                'default': None,
                'description': 'Maximum norm of the residual'},
            'fit_intercept': {
                'type': 'boolean',
                'default': True,
                'description': 'whether to calculate the intercept for this model'},
            'normalize': {
                'type': 'boolean',
                'default': True,
                'description': 'This parameter is ignored when ``fit_intercept`` is set to False'},
            'precompute': {
                'enum': [True, False, 'auto'],
                'default': 'auto',
                'description': 'Whether to use a precomputed Gram and Xy matrix to speed up calculations'},
        }}],
}
_input_fit_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Fit the model using X, y as training data.',
    'type': 'object',
    'required': ['X', 'y'],
    'properties': {
        'X': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': 'number'},
            },
            'description': 'Training data.'},
        'y': {
            'anyOf': [{
                'type': 'array',
                'items': {
                    'type': 'number'},
            }, {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'number'},
                }}],
            'description': 'Target values'},
    },
}
_input_predict_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Predict using the linear model',
    'type': 'object',
    'required': ['X'],
    'properties': {
        'X': {
            'anyOf': [{
                'type': 'array',
                'items': {
                    'laleType': 'Any',
                    'XXX TODO XXX': 'item type'},
                'XXX TODO XXX': 'array_like or sparse matrix, shape (n_samples, n_features)'}, {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'number'},
                }}],
            'description': 'Samples.'},
    },
}
_output_predict_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Returns predicted values.',
    'type': 'array',
    'items': {
        'type': 'number'},
}
_combined_schemas = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Combined schema for expected data and hyperparameters.',
    'documentation_url': 'https://scikit-learn.org/0.20/modules/generated/sklearn.linear_model.OrthogonalMatchingPursuit#sklearn-linear_model-orthogonalmatchingpursuit',
    'type': 'object',
    'tags': {
        'pre': [],
        'op': ['estimator'],
        'post': []},
    'properties': {
        'hyperparams': _hyperparams_schema,
        'input_fit': _input_fit_schema,
        'input_predict': _input_predict_schema,
        'output_predict': _output_predict_schema},
}
if (__name__ == '__main__'):
    lale.helpers.validate_is_schema(_combined_schemas)
OrthogonalMatchingPursuit = lale.operators.make_operator(OrthogonalMatchingPursuitImpl, _combined_schemas)

