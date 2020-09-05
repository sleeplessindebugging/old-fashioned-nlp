#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Update       : 2020-09-05 08:24:23
# @Author       : Chenghao Mou (mouchenghao@gmail.com)

"""Catboost text classifiers."""

from catboost import CatBoostClassifier
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfCatBooostClassifier(BaseEstimator):
    def __init__(self, **kwargs):
        """
        TfidfVectorizer + CatBoost Classifier. See get_params for details.

        Examples
        --------
        >>> model = TfidfCatBooostClassifier(tfidf__sublinear_tf=True, classifier__iterations=100, classifier__verbose=1)
        """
        self.tfidf = TfidfVectorizer(sublinear_tf=True)
        self.model = CatBoostClassifier(verbose=False)

        self.set_params(**kwargs)

    def set_params(self, **params):
        self.tfidf.set_params(
            **{
                k.split("__", 1)[-1]: v
                for k, v in params.items()
                if k.startswith("tfidf__")
            }
        )
        self.model.set_params(
            **{
                k.split("__", 1)[-1]: v
                for k, v in params.items()
                if k.startswith("classifier__")
            }
        )

    def get_params(self, deep=True):
        params = {"tfidf__" + k: v for k, v in self.tfidf.get_params(deep).items()}
        params.update(
            {"classifier__" + k: v for k, v in self.model.get_params(deep).items()}
        )
        return params

    def fit(self, X, y, **kwargs):
        vectors = self.tfidf.fit_transform(X)
        vectors.sort_indices()
        self.model.fit(vectors, y, **kwargs)

    def predict(self, X):
        vectors = self.tfidf.transform(X)
        vectors.sort_indices()
        return self.model.predict(vectors)

    def score(self, X, y):
        vectors = self.tfidf.transform(X)
        vectors.sort_indices()
        return self.model.score(vectors, y)
