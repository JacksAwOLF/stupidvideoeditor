import os
from config import *

# converts beats into a name, and its time
#
# beats: string with time signature
def get_name_length(beats):

	num = beats
	den = "1"
	if "/" in beats:
		num, den = beats.split("/")

	if not isnum(num) or not isnum(den):
		raise ValueError(beats+" isn't a number")

	return 	num+"-"+den, str(float(beat)*float(num)/float(den))


# check if a file is in a folder; if so, return full name
# other wise, raise error
#
# name: name of file (with or without suffix)
# folder: which folder to look for it (the prefix)
# list: list  of possible suffixes if one isn't in name
def find_file(name, folder, sufflist):
	
	name = folder+name

	dot = name.find('.', 1)
	if dot == -1:
		for suff in sufflist:
			if os.path.exists(name+suff):
				return name+suff
	elif os.path.exists(name):
		return name

	raise ValueError("Line "+str(linenumber)+": no such file '"+name+"' exists")



# retrive the length of a video
def get_length_video(name):
	cmd = "ffprobe -of default=noprint_wrappers=1:nokey=1 -show_entries format=duration -v error "+ name
	return float(os.popen(cmd).read()[:-1])



# retrieve the resolution of a video
def get_resolution(name):
	cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "
	return os.popen(cmd+name).read()[:-1]



# can the string x be interpreted as a number?
def isnum(x):
	return x.replace('.','',1).replace('/','',1).isdigit()


