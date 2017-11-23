import os
import subprocess
import pandas as pd
import numpy as np
import copy

def flatten_input(input):
	#input = 4 x 4
	arr = []
	for x in input:
		for y in x:
			arr.append(y)
	return arr

def read_datatrain(file_path):
	df = pd.read_csv(file_path)
	data = np.array(df.as_matrix())
	#print (data)
	data = absolute_time_to_different_time(data)
	data = np.array(data)
	return data

def absolute_time_to_different_time(data):
	new_data = []
	first = True
	now = 0
	for x in data:
		note = []
		if first:
			note = copy.deepcopy(x)
			note[0] = 0
			new_data.append(note)
			first = False
		else:
			note = copy.deepcopy(x)
			note[0] = x[0] - now
			new_data.append(note)
		now = x[0]
		#print (x[0])

	return new_data

def create_datatrain(data, n_note_terakhir):
	#print (data)
	data_length = len(data)
	data_train = []
	data_target = []
	for i in range(n_note_terakhir, data_length):
		note_data_train = []
		for j in range(i-n_note_terakhir, i):
			note_data_train.append(data[j])
		note_data_train = flatten_input(note_data_train)
		data_train.append(note_data_train)
		data_target.append(data[i])
	return np.array(data_train), np.array(data_target)

def myround(x, base=5):
    return int(base * round(float(x)/base))

def round_data(data):
	new_data = [];
	for x in data:
		new_note = []
		new_note = fix_note(x)
		new_data.append(new_note)
	return new_data

def fix_note(single_note):
	new_note = []
	for y in range(0, 4):
			if y == 3 or y == 0:
				duration = myround(single_note[y],40)
				if duration < 1:
					duration = 40
				new_note.append(duration)
			if y == 2 or y == 1:
				note = myround(single_note[y], 1)
				if note > 127:
					note = 127
				new_note.append(note)	
	return new_note

def check_highest(data):
	max_time = -10000
	max_duration = -10000
	for x in data:
		max_time = max(max_time, x[0])
		max_duration = max(max_duration, x[3])
	print ('Max time = ', max_time)
	print ('Max duration = ', max_duration)

def normalize_input(data):
	data = data.tolist()
	new_data = []
	for x in data:
		note = []
		note.append(float(x[0] * 1.0 / 1920.0))
		note.append(float(x[1] * 1.0 / 128.0))
		note.append(float(x[2] * 1.0 / 128.0))
		note.append(float(x[3] * 1.0 / 1920.0))
		new_data.append(note)
	return np.array(new_data)

def train_and_test(collection_length, n_note_terakhir = 4, hidden_layer = 2):
	from keras.models import Sequential
	from keras.layers import Dense
	import random
	import numpy

	# create model
	if hidden_layer < 2 or hidden_layer > 4:
		hidden_layer = 2

	model = Sequential()
	model.add(Dense(n_note_terakhir * 4, input_dim=n_note_terakhir * 4, kernel_initializer='normal', activation='sigmoid'))
	for x in range(hidden_layer - 1):
		model.add(Dense(n_note_terakhir * 4, kernel_initializer='normal', activation='sigmoid'))
	# model.add(Dense(128))
	# model.add(Dense(128))
	# model.add(Dense(128))
	model.add(Dense(4, kernel_initializer='normal', activation = 'sigmoid'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')

	for x in range(1,collection_length):
		file_path = "csv/" + str(x) + ".csv"
		data = read_datatrain(file_path)
		data = normalize_input(data)
		X, Y = create_datatrain(data, n_note_terakhir)
		model.fit(X, Y, epochs = 5, batch_size = 1)

	file_path = "csv/" + str(collection_length) + ".csv"
	data = read_datatrain(file_path)
	data = normalize_input(data)
	X, Y = create_datatrain(data, n_note_terakhir)
	prediction = copy.deepcopy(data[:4])

	prediction = prediction.tolist()

	for x in range(n_note_terakhir,1000):
		X = prediction[x - n_note_terakhir:x]
		X = [flatten_input(X)]
		X = np.array(X)
		Y = model.predict(X)
		Y = Y[0]
		#print(Y)
		prediction.append(Y)
		#print(prediction)
		#break

	# prediction = model.predict(X)
	#prediction = round_data(prediction)
	#prediction = different_time_to_absolute_time(prediction)
	#for x in Y:
	#		print (x)
	for x in prediction:
	 	print (x)
	#create_predicted_csv(prediction)

def different_time_to_absolute_time(data, start_time = 2840):
	now = start_time
	for x in data:
		now = now + x[0]
		x[0] = now
	return data

def create_predicted_csv(data):
	labels = ['time', 'note', 'velocity', 'duration']
	data = data.tolist()
	df = pd.DataFrame.from_records(data, columns=labels)
	create_csv('predicted.csv', df)

def create_csv(file_path,df):
	ensure_dir_exist(file_path)
	df.to_csv(file_path,index = 0)

def ensure_dir_exist(file_path):
    directory = os.path.dirname(file_path)
    if (len(directory) > 1):
	    if not os.path.exists(directory):
	        os.makedirs(directory)

train_and_test(43)
