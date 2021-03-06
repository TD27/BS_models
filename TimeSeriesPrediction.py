# -*- coding: utf-8 -*-
"""Prediction pipeline #2 (class)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qAILSD0mQPrUOjHJKzovfAG3gzw2D1aG
"""

import pandas as pd
import datetime as dt
import numpy as np
import pickle


class DynamicRange:

    def __init__(self):
        self.df_train = pd.DataFrame({'Time': [], 'Data': []})
        self.record = {}
        self.df_analytic = pd.DataFrame({'Time': [],
                                         'Minute': [],
                                         'DayOfWeek': [],
                                         'Hour': [],
                                         'Day': [],
                                         'Sample': []})
        self.df_piv = pd.DataFrame()
        self.df_predict = pd.DataFrame({'Median': [],
                                        'Mean': [],
                                        'STD': [],
                                        'Min_Range': [],
                                        'Max_Range': [], })

    def append(self, record):
        self.record = record
        d_record = pd.DataFrame(self.record)
        self.df_train = self.df_train.append(d_record, ignore_index=True)
        self.df_train['Time'] = pd.to_datetime(self.df_train['Time'])

    def train(self):
        if len(self.df_train.index) == 0:
            return print(
                '<I cannot train the model. There is no data in the training dataset. Upload data to the training dataset at first. Use method append()>')

        self.df_analytic = self.df_train.set_index(self.df_train['Time'])

        self.df_analytic['Minute'] = self.df_analytic.index.minute
        self.df_analytic['DayOfWeek'] = self.df_analytic.index.dayofweek
        self.df_analytic['Hour'] = self.df_analytic.index.hour
        self.df_analytic['Day'] = self.df_analytic.index.dayofyear
        self.df_analytic['Sample'] = ((self.df_analytic['Hour'] * 60 + self.df_analytic['Minute']) / 5).astype(int)
        self.df_analytic = self.df_analytic.set_index(self.df_analytic['Sample'])
        self.df_analytic.index.name = 'Sample_in_day'

        self.df_piv = self.df_analytic.pivot_table(
            values='Data',
            index='Sample',
            columns='Day',
            aggfunc='mean')
        self.df_piv.index.name = 'Sample_in_day'

        # Calculate prediction
        self.df_predict['Median'] = self.df_piv.median(axis=1)
        self.df_predict['Mean'] = self.df_piv.mean(axis=1)
        self.df_predict['STD'] = 3 * self.df_piv.std(axis=1)
        self.df_predict['Min_Range'] = self.df_predict['Median'] - self.df_predict['STD']
        self.df_predict['Max_Range'] = self.df_predict['Median'] + self.df_predict['STD']
        self.df_predict.index.name = 'Sample_in_day'
        return print('<The model has been successfully trained.>')

    def get(self, timestamp):
        if len(self.df_predict.index) == 0: return print(
            '<I cannot return the values. The model is empty. Train the model at first, use method train().> ')

        self.timestamp = pd.to_datetime(timestamp)
        self.hour = self.timestamp.hour
        self.minute = self.timestamp.minute
        self.sample = int((self.hour * 60 + self.minute) / 5)
        self.min_range = self.df_predict.loc[self.sample, 'Min_Range']
        self.max_range = self.df_predict.loc[self.sample, 'Max_Range']
        return self.min_range, self.max_range





model = DynamicRange()


# Read a pickle file with data
dic = {}
dic = pd.read_pickle('O2SK_data_dict.pkl')

for i in range(0, len(dic[list(dic.keys())[0]])):
    record = {list(dic.keys())[0]: [dic[list(dic.keys())[0]][i]],
              list(dic.keys())[1]: [dic[list(dic.keys())[1]][i]]}
    model.append(record)


model.train()

print(model.df_predict)

#timestamp = '2020-06-08 00:10:00'
#model.get(timestamp)

#record = {'Time': ['2020-06-11 00:00:00'], 'Data': [5200]}
#model.append(record)

# pd.to_pickle(model.df_predict, '/content/Dynamic_Range_Daily_Predict.pkl')

# picklefile = open('/content/DynamicRangeModel.pkl', 'wb')
# pickle.dump(model, picklefile)
# picklefile.close()

print('--- PREDICTION ---')

for i in

timestamp = '2020-06-08 00:10:00'
model.get(timestamp)
