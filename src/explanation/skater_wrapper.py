import shap
from dtreeviz.trees import dtreeviz
from skater.core.explanations import Interpretation
from skater.model import InMemoryModel

from src.encoding.common import retrieve_proper_encoder
from src.explanation.models import Explanation
from sklearn.externals import joblib
import os

from src.predictive_model.models import PredictiveModels


def explain(skater_exp: Explanation, training_df, test_df, explanation_target):
    job = skater_exp.job
    model = joblib.load(job.predictive_model.model_path)
    model = model[0]

    shap.initjs()

    features = list(training_df.drop(['trace_id', 'label'], 1).columns.values)
    interpreter = Interpretation(training_df, feature_names=features)
    X_train = training_df.drop(['trace_id', 'label'], 1)
    Y_train = training_df['label'].values

    model_inst = InMemoryModel(model.predict, examples=X_train, model_type=model._estimator_type, unique_values=[1, 2],
                               feature_names=features, target_names=['label'])
    surrogate_explainer = interpreter.tree_surrogate(model_inst, seed=5)

    surrogate_explainer.fit(X_train, Y_train, use_oracle=True, prune='post', scorer_type='default')
    surrogate_explainer.class_names = features

    viz = dtreeviz(surrogate_explainer.estimator_,
                   X_train,
                   Y_train,
                   target_name='label',
                   feature_names=features,
                   orientation="TD",
                   class_names=list(surrogate_explainer.class_names),
                   fancy=True,
                   X=None,
                   label_fontsize=12,
                   ticks_fontsize=8,
                   fontname="Arial")
    viz.save("skater_plot.svg")
    f = open("skater_plot.svg", "r")
    response = f.read()
    os.remove("skater_plot.svg")
    return response
