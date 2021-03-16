

model = DynamicRange()

# An example of reading a dataset from pickle file
dic = {}
dic = pd.read_pickle('O2SK_data_dict.pkl')

for i in range(0, len(dic[list(dic.keys())[0]])):
    record = {list(dic.keys())[0]: [dic[list(dic.keys())[0]][i]],
              list(dic.keys())[1]: [dic[list(dic.keys())[1]][i]]}
    model.append(record)



model.train()

print(model.df_predict)

# timestamp = '2020-06-08 00:10:00'
# model.get(timestamp)

# record = {'Time': ['2020-06-11 00:00:00'], 'Data': [5200]}
# model.append(record)

# pd.to_pickle(model.df_predict, '/content/Dynamic_Range_Daily_Predict.pkl')

# picklefile = open('/content/DynamicRangeModel.pkl', 'wb')
# pickle.dump(model, picklefile)
# picklefile.close()

print('--- PREDICTION ---')

timestamp = '2020-06-08 00:10:00'
model.get(timestamp)
