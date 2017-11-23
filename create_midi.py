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

def create_midi(file_path, file_target):
	#read the csv
	log = open("create_midi_log.txt","a+");
	if not os.path.isfile(file_path):
		log.write("Failed to open " + file_path);
		log.close();
		return;
	df = pd.read_csv(file_path);
	#creating note_off (velocity 0)
	temp = [];
	for row in df.itertuples():
		temp.append([row.time, row.note, row.velocity]);
		temp.append([row.time + row.duration, row.note, 0]);
	#sorting based on time
	temp.sort();
	#creating file
	csv_target = open('temp.csv', "w");
	#start
	tempo = 375000;
	csv_target.write("0, 0, Header, 0, 1, 480" + "\n");
	csv_target.write("1, 0, Start_track" + "\n");
	csv_target.write("1, 0, Tempo, " + str(tempo) + "\n");
	csv_target.write("1, 0, Key_signature, 0, \"major\"" + "\n");
	csv_target.write("1, 0, Time_signature, 4, 2, 24, 8" + "\n");
	#writing the notes
	for row in temp:
		csv_target.write("1, " + str(row[0]) + ", " + "Note_on_c, 1, " + str(row[1]) + ", " + str(row[2]) + '\n');
	#end
	last_time = temp[-1][0] + 1;
	csv_target.write("1, " + str(last_time) + ", End_track" + "\n");
	csv_target.write("0, 0, End_of_file" + "\n");
	csv_target.close();
	try:
		subprocess.check_output("Csvmidi.exe<temp.csv>" + file_target, shell=True);
	except:
		log.write("Failed to execute CLI argument for " + file_path);
		log.close();
		return;
	os.remove("temp.csv");
	log.write("Converting " + file_path + " to " + file_target + " success!");
	log.close();

create_midi('predicted.csv', 'finish.mid')