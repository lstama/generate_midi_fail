import numpy as np
import pandas as pd
import os
import subprocess
from collections import namedtuple

def ensure_dir_exist(file_path):
    directory = os.path.dirname(file_path)
    if (len(directory) > 1):
	    if not os.path.exists(directory):
	        os.makedirs(directory)

def create_csv(file_path,df):
	ensure_dir_exist(file_path)
	df.to_csv(file_path,index = 0)

def create_data(file_path, file_target):
	#logging
	log = open("create_data_train_log.txt","a+");
	if not os.path.isfile(file_path):
		log.write("Failed to open " + file_path);
		log.close();
		return;
	#running cli argument to convert midi to unprocessed csv
	try:
		subprocess.check_output("Midicsv.exe<" + file_path + "|replace.exe|simplify.exe>temp.csv", shell=True);
	except:
		log.write("Failed to execute CLI argument for " + file_path);
		log.close();
		return;
	#read that csv
	df = pd.read_csv("temp.csv");
	#create array to save note length
	#features :time, velocity
	total_note, total_channel, total_features = 256, 256, 2;
	matrix = [[[0 for z in range(total_features)] for x in range(total_note)] for y in range(total_channel)];
	#create tuple for saving note
	Note = namedtuple('Note', 'time note velocity duration');
	tuple_list = [];
	#iterate df
	try:
		for row in df.itertuples():
			if (row.velocity > 0):
				if (matrix[row.channel][row.note][1] == 0):
					matrix[row.channel][row.note][0] = row.time;
					matrix[row.channel][row.note][1] = row.velocity;
			else:
				if (matrix[row.channel][row.note][1] > 0):
					duration = abs(row.time - matrix[row.channel][row.note][0]);
					temp = Note(matrix[row.channel][row.note][0], row.note, matrix[row.channel][row.note][1], duration);
					tuple_list.append(temp);
					matrix[row.channel][row.note][0] = 0;
					matrix[row.channel][row.note][1] = 0;
	except:
		log.write("Failed to iterate dataframe of " + file_path);
		log.close();
		return;
	#create new dataframe with duration 
	try:
		new_df = pd.DataFrame(tuple_list, columns=tuple_list[0]._fields);
		new_df = new_df.sort_values(by = ['time', 'note']);
		new_df.drop_duplicates(subset = ['time'], keep = 'last', inplace = True)
	except:
		log.write("Failed to create new dataframe for " + file_path);
		log.close();
		return;
	#create csv
	create_csv(file_target,new_df);
	os.remove("temp.csv");
	log.write("Converting " + file_path + " to " + file_target + " success!");
	log.close();

for x in range(1,43):
	file_path = "midi/"+ str(x) + ".mid"
	file_target = "csv/"+ str(x) + ".csv"
	if (os.path.isfile(file_path)):
		create_data(file_path,file_target)
		#exit()