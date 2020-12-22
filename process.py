# reads a file
# if sees --- stops and merges the video files beforehand
# also makes sure the number of -'s is the length of the video in beats
# stops the reading when sees *
# IMPORTANT: ALL IMAGES IN JPG AND ALL VIDEOS IN MP4 SAME SIZE SAME EVERYTHING

import sys
import time
import os

from cmd import *


if len(sys.argv) > 1:
	output = sys.argv[1]+'.mp4'

if __name__ == "__main__":

	stime = time.time()


	videos = []
	inputv = "" # -i video -i video ...
	cmdvol = "" # [0:a]volume=0[a0],[1:a]...
	vinputs = "" # [0:v][1:v]...
	ainputs = "" # [a0][a1][a2]...

	audios = []
	inputa = ""	# -i audio -i audio ...
	adelays = "" # [] adelay=5000|5000 [ia0], ...
	aweights = "" # 100 50 50 1 

	text_cmd = "" 	# cmd to add text
	cmdconvert = "" #  cmd to convert video resolutions

	

	t = 0   # current running time
	linenumber = "0"	# current line
	x = 0		# current running #vids



	f = open(file, "r")
	for line in f:

		linenumber = str(int(linenumber)+1)

		# skip empty lines and comments
		if line[0] == '\n' or line[0] == '#':
			continue
		if "#" in line:
			line = line[:line.find('#')]
		words = line[:-1].split()

		print(words)

		# print time stamp
		if words[0] == 'print':
			print("time in vid: "+str(t))
					

		# change the beat or vidaud percentage
		elif words[0] == 'beat' or words[0] == 'vidaud':
			if len(words) < 2 or not isnum(words[1]):
				raise ValueError("Line "+str(linenumber)+" expected value")
			if words[0] == 'beat':
				beat = float(words[1])
			else:
				vidaud = words[1]




		# subtitle addition
		elif words[0] == 'text':
			# 'text' x,y duration size color text
			x,y = words[1].split(",")
			length = get_name_length(words[2])[1] if "/" in length else words[2]
			size = words[3]
			color = words[4]
			text = words[5:].join(" ")

			if x == "-1":
				x = "(w-text_w)/2"
			if y == "-1":
				y = "(h-text_h)/2"
			if color == "-1":
				color = "white"

			text_cmd += "drawtext=enable='between(t,"+str(t)+","+str(t+float(length))+")'"
			text_cmd += ":box=1:boxcolor=black@"+textbox_alpha+":fontsize="+size+":fontcolor="+color
			text_cmd += ":x="+x+":y="+y+":text="+text+","
			




		# video and audio
		else:


			# index of array folders and suffixes
			# 0=>video; 1=>image; 2=>audio
			iid = 2 if words[0] == 'audio' else (1 if len(words) == 2 else 0)

			# name of input file with suffix and folder name
			name = find_file( words[0] if len(words) == 1 else (words[3] if isnum(words[1]) else words[1]), folders[iid], suffixes[iid])

			# pre: name of file; suf: suffix of file
			pre, suf = os.path.basename(name).split('.')
			suf = "."+suf



			# 'audio' start end file (weight) (delta)
			# 'audio' file (weight) (delta)
			if iid == 2:
				if len(words) < 2:
					raise ValueError("Line "+linenumber)
				# get final audio name
				outname = ""
				wstart = 4
				if isnum(words[1]):
					outname = folders[2]+pre+"__"+words[1]+"__"+words[2]+suf
					cut(name, words[1], words[2], outname, True)
				else:
					outname = name
					wstart = 2
				# get optional data
				delta = 0
				weight = "100"
				if len(words) > wstart:
					weight = words[wstart]
					if len(words) > wstart+1:
						bname, blen = get_name_length(words[wstart+1])
						delta = blen
				# update ffmpeg commands	 
				inputa += " -i "+outname
				aweights += str(weight)+" "
				audios.append(t+float(delta))


			
			# video
			# length image
			# length video start
			else:
			
				# get names and stuff
				if len(words) == 1:
					video_name = name
					t += float(get_length_video(name))	
				else:
					bname, blen = get_name_length(words[0])
					if iid == 1:
						video_name = folders[1] + pre + "__" + bname + suffixes[0][0]
						loop_image(words[0], name, video_name)
					else:
						video_name = folders[3] + pre + "__" + bname + "__"+words[2].replace(".","-")+suf
						cut(name, words[2], blen, video_name)
					t  += float(blen)

				# update ffmpeg commands
				x = str(x)
				inputv += "-i "+video_name+" "

				cmdvol += "["+x+":a]volume="+vidaud+"[a"+x+"],"
				ainputs += "[a"+x+"]"

				if get_resolution(video_name) != resolution:
					cmdconvert += "["+x+"]scale=1920:1080,setsar=1:1[con"+x+"];"
					vinputs += "[con"+x+":v]"
				else:
					vinputs += "["+x+":v]"

				

				x = int(x) + 1



	

	cmd = "ffmpeg "+inputv+inputa+" -filter_complex '"
	final_video = "[vout1]"
	final_audio = "[aout1]"
	#x = str(len(videos
	x = str(x)

	cmd += cmdconvert	# convert any video files
	cmd += vinputs+"concat=n="+x+final_video+";"	# merge the video files
	cmd += cmdvol+ainputs+"concat=n="+x+":v=0:a=1"+final_audio # merge the audio files


	# add some additional audio if needed
	if len(audios) > 0:
		cmd += ";"
		adelays = ""
		iainputs = ""
		for i in range(len(audios)):
			y = str(int(round(audios[i]*1000)))
			adelays += "["+str(int(x)+i)+"] adelay="+y+"|"+y+"[ia"+str(i)+"],"	
			iainputs += "[ia"+str(i)+"]"
		cmd += adelays+final_audio+iainputs+"amix=inputs="+str(len(audios)+1)
		cmd += ":duration=first:weights=100 "+aweights
		final_audio = "[aout2]"
		cmd += final_audio


	# add the text if needed
	if text_cmd != "":
		cmd += ";" + final_video + text_cmd[:-1]
		final_video = "[vout2]"
		cmd += final_video


	# merge everything together
	cmd += "' -map "+final_video+" -map "+final_audio+" -y "+output



	print(cmd)
	os.system(cmd)
	print("Done! Time elapsed: "+str(time.time()-stime))




f = open(file, "r")
for line in f:

	linenumber = str(int(linenumber)+1)








def processLine(line):
	global beat
	global vidaud

	# skip empty lines and comments
	if line[0] == '\n' or line[0] == '#':
		return
	if "#" in line:
		line = line[:line.find('#')]
	words = line[:-1].split()


	# processing each thing
	if words[0] == 'print':
		print("time in vid: "+str(t))

	elif words[0] == 'beat':
		if not isnum(words[1]):
			raise ValueError("Line "+str(linenumber)+" expected float")
		beat = float(words[1])

	elif words[0] == 'vidaud':
		if not isnum(words[1]):
			raise ValueError("Line "+str(linenumber)+" expected integer")
		vidaud = words[1]

	elif words[0] == 'text':
		processText(words)

	elif words[0] == 'overlay':
		# going to add this soon

	elif words[0] == 'audio':
		processAudio(words)

	else:
		processVideoImages(words)

# adding subtitles
def processText(words):
	global t
	global text_cmd

	x,y = words[1].split(",")
	length = get_name_length(words[2])[1] if "/" in length else words[2]
	size = words[3]
	color = words[4]
	text = words[5:].join(" ")

	if x == "-1":
		x = "(w-text_w)/2"
	if y == "-1":
		y = "(h-text_h)/2"
	if color == "-1":
		color = "white"

	text_cmd += "drawtext=enable='between(t,"+str(t)+","+str(t+float(length))+")'"
	text_cmd += ":box=1:boxcolor=black@"+textbox_alpha+":fontsize="+size+":fontcolor="+color
	text_cmd += ":x="+x+":y="+y+":text="+text+","

def processAudio(words):

	# 'audio' start end file (weight) (delta)
	# 'audio' file (weight) (delta)

	# get final audio name
	outname = ""
	wstart = 4
	if isnum(words[1]):
		outname = folders[2]+pre+"__"+words[1]+"__"+words[2]+suf
		cut(name, words[1], words[2], outname, True)
	else:
		outname = name
		wstart = 2

	# get optional data
	delta = 0
	weight = "100"
	if len(words) > wstart:
		weight = words[wstart]
		if len(words) > wstart+1:
			bname, blen = get_name_length(words[wstart+1])
			delta = blen

	# update ffmpeg commands	 
	inputa += " -i "+outname
	aweights += str(weight)+" "
	audios.append(t+float(delta))



# video/images/audio
def processVideoImages(words):

	global folders

	# index of array folders and suffixes
	# 0=>video; 1=>image; 2=>audio
	iid = 2 if words[0] == 'audio' else (1 if len(words) == 2 else 0)

	# name of input file with suffix and folder name
	name = find_file( words[0] if len(words) == 1 else (words[3] if isnum(words[1]) else words[1]), folders[iid], suffixes[iid])

	# pre: name of file; suf: suffix of file
	pre, suf = os.path.basename(name).split('.')
	suf = "."+suf





	
	# video
	# length image
	# length video start
	else:
	
		# get names and stuff
		if len(words) == 1:
			video_name = name
			t += float(get_length_video(name))	
		else:
			bname, blen = get_name_length(words[0])
			if iid == 1:
				video_name = folders[1] + pre + "__" + bname + suffixes[0][0]
				loop_image(words[0], name, video_name)
			else:
				video_name = folders[3] + pre + "__" + bname + "__"+words[2].replace(".","-")+suf
				cut(name, words[2], blen, video_name)
			t  += float(blen)

		# update ffmpeg commands
		x = str(x)
		inputv += "-i "+video_name+" "

		cmdvol += "["+x+":a]volume="+vidaud+"[a"+x+"],"
		ainputs += "[a"+x+"]"

		if get_resolution(video_name) != resolution:
			cmdconvert += "["+x+"]scale=1920:1080,setsar=1:1[con"+x+"];"
			vinputs += "[con"+x+":v]"
		else:
			vinputs += "["+x+":v]"

		

		x = int(x) + 1




