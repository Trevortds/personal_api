import datetime
import json

from app import app
from app import db
from flask import jsonify, request, abort, make_response
from app.models import State, CommuteTimeEntry

import numpy as np
from scipy.stats import norm, beta
import matplotlib.pyplot as plt
from scipy.optimize import fmin
import pandas as pd
import math


class CommuteModel:
    __instance = None

    @staticmethod
    def get_instance():
        if CommuteModel.__instance is None:
            CommuteModel()
        return CommuteModel.__instance

    def __init__(self, _lambda=0.05, fourier_o=2, fourier_degree=3):
        ''' This is a private constructor, do not call it '''
        if CommuteModel.__instance is not None:
            raise Exception("Attempted to construct a duplicate singleton!")
        else:
            CommuteModel.__instance = self
        self._lambda = _lambda
        self.start_time = []
        self.data = []
        self.basis = lambda x: self.fourier_basis(x, fourier_o, fourier_degree)
        self.mean = 0
        self.w = []
        self.s_2 = 0
        self.X = None
        self.t = None
        self.fit_fn = None

        self.refresh()

    def refresh(self):
        '''
        TODO turn this into a rabbit job or whatever. make it asynchronous, it can take a while.
        :return:
        '''
        start_time = []
        data = []
        for entry in CommuteTimeEntry.query.all():
            start_time.append(entry.departure_time.hour + entry.departure_time.minute / 60)
            data.append(entry.travel_time)
        self.start_time = np.asarray(start_time)
        self.data = np.asarray(data)

        if len(data) != len(start_time):
            raise Exception("Data and start-time are not of equal length!")

        self.mean = sum(data)/len(data)

        self.X = self.basis(start_time)
        self.t = self.data - self.mean

        # w = (X^TX + |X|λI)^-1 * X^Tt
        self.w = np.dot(np.linalg.inv(np.dot(self.X.T, self.X) +
                                      len(self.X) * self._lambda * np.identity(self.X.shape[1])),
                        np.dot(self.X.T, self.t))

        # s^2 = 1/N * (t^Tt - t^TX * w)
        self.s_2 = 1/len(data) * (np.dot(self.t.T, self.t) - np.dot(np.dot(self.t.T, self.X), self.w))

        self.fit_fn = lambda x: np.dot(self.basis(x), self.w) + self.mean

        return self.fit_fn

    def predict(self, time: datetime.datetime):
        '''
        make a prediction
        :param time: in datetime format
        :return: float of minutes to work if you leave now
        '''

        return self.fit_fn(time.hour+time.minute/60)

    def get_plot(self):
        bleh = np.arange(7.0, 10.6, 0.01)
        last_n = 3
        fig = plt.figure()
        # plt.subplot(212)
        plt.plot(self.start_time, self.t + self.mean, 'go',
                 bleh, self.fit_fn(bleh), '-k',
                 self.start_time[-last_n:], self.t[-last_n:] + self.mean, 'sr'
                 )
        # plt.ylim(30, 70)
        plt.xlim(7, 10.6)
        return fig

    def get_histogram(self):

        # Fit a normal distribution to the data:
        mu, std = norm.fit(self.data)
        # Fit a beta distribution to the data
        betaparams = beta.fit(self.data)

        fig = plt.figure()
        # plt.subplot(211)

        # Plot the histogram.
        plt.hist(self.data, bins=2*len(self.data), normed=True, alpha=0.6, color='g')

        # Plot the PDF.
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        b = beta.pdf(x, *betaparams)
        plt.plot(x, b, 'r', linewidth=2)
        title = "Normal fit: mu = %.2f,  std = %.2f" % (mu, std)
        plt.suptitle(title)
        subtitle = "black: normal, red: beta"
        plt.title(subtitle)

        return fig

    def get_normal_confidence_interval(self, conf=0.68):
        mu, std = norm.fit(self.data)
        return norm.interval(conf, mu, std)

    def get_beta_confidence_interval(self, conf=0.68):
        betaparams = beta.fit(self.data)
        beta.interval(conf, *betaparams)

    def get_normal_percentile_confidence(self, conf=0.60):
        '''
        I am conf percent sure that I will be there in :return: minutes or less
        invert conf for "minutes or more". eg 0.10== 90 percent sure it'll take at least...
        '''
        mu, std = norm.fit(self.data)
        return norm.ppf(conf, mu, std)

    def get_beta_percentile_confidence(self, conf=0.60):
        '''
        I am conf percent sure that I will be there in :return: minutes or less
        invert conf for "minutes or more". eg 0.10== 90 percent sure it'll take at least...
        '''
        betaparams = beta.fit(self.data)
        return beta.ppf(conf, *betaparams)

    @staticmethod
    def fourier_basis(x, o=1, degree=1):
        try:
            X_0 = pd.DataFrame(x)
            X = pd.DataFrame(x)
        except:
            X = pd.DataFrame([x])
            X_0 = pd.DataFrame([x])
        X[0] = 1 # b
        for i in range(0, degree):
            X[2*i+1] = X_0.apply(lambda y: math.sin((i+1)*o*y), axis=1)
            X[2*i+2] = X_0.apply(lambda y: math.cos((i+1)*o*y), axis=1)
        return X

    @staticmethod
    def poly_basis(x, degree=1):
        X = pd.DataFrame(x)
        X[1] = X[0]
        X[0] = 1
        for i in range(0, degree+1):
            X[i] = X[1]**i
        return X


def predict():
    now = datetime.datetime.now()
    model = CommuteModel.get_instance()
    return model.predict(now)[0]


def add_time_entry(start_datetime, end_datetime, twitter_delay=None, maps_prediction=None):
    new_elem = CommuteTimeEntry()
    new_elem.departure_time = start_datetime
    new_elem.arrival_time = end_datetime
    new_elem.travel_time = (end_datetime - start_datetime).seconds/60
    if twitter_delay:
        new_elem.twitter_delay = twitter_delay
    if maps_prediction:
        new_elem.maps_prediction = maps_prediction

    db.session.add(new_elem)
    db.session.commit()

    CommuteModel.get_instance().refresh()
    return True
