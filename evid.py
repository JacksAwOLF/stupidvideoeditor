import sys
import time
import os

from cmd import *


if len(sys.argv) > 1:
	output = sys.argv[1]+'.mp4'

if __name__ == "__main__":

	stime = time.time()

	videos = []		# the list of videos in order
	audios = []		# audio files to addd
	textcmd = ""	# subtitiles to add
	t = 0  			# current running time
	linenumber = 0	# current line

	f = open(file, "r")
	comments = False

	for line in f:

		linenumber += 1

		# skip empty lines and comments
		if comments and '*/' in line:
			comments = False
			line = [line.find('*/')+2:]

		if '/*' in line:
			line = line[:line.find('/*')]
			comments = True

		if "#" in line:
			line = line[:line.find('#')]
		
		if line[0] == '\n' or line[0] == '#' or comments:
			continue

		words = line[:-1].split()



		# processing commands line by line

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
		elif words[0] == 'audio':
			processAudio(words)
		elif words[0] == 'overlay':
			# going to add this feature soon
			continue
			
		else:
			# video or images that take time
			index = "["+str(len(videos))+"]"

			vid = Video(words[(len(words)==1 ? 0 : 1)], index, vidaud)
			videos.append(vid)
			if len(words) > 1:
				name = "hi"
				cmd = ( len(words)==2 ? vid.loop(words[0], name)
						vid.cut(words[2], words[0], name) )
				os.system(cmd)

			t += float(vid.get_length())


	
	# start constructing the ultimate command
	final_video = "[vout1]"
	final_audio = "[aout1]"
	n = str(len(videos))

	# first we add all the inputs (video/images and audio)
	cmd = "ffmpeg"
	for vid in videos:
		cmd += " -i " + vid.source
	for aud in audios:
		cmd += " -i " + aud.source
	cmd += " -filter_complex '"
	
	# adjust each video's volume and merge it together
	for vid in videos:
		cmd += vid.volume() + ','
	for i in range(len(videos)):
		cmd += '[a'+str(i)+']'
	cmd += 'concat=n='+n+':v=0:a=1'+final_audio+';'

	# then we can add commands to convert any weird resolutions for videos
	for vid in videos:
		if vid.get_resolution != resolution:
			vid.resize()
			cmd += vid.cmd

	# now we merge all the video files
	for vid in videos:
		cmd += vid.name
	cmd += "concat=n="+str(len(videos))+final_video

	# add sutitles to the video
	if text_cmd != "":
		cmd += ';'
		cmd += final_video + text_cmd[:-1]
		final_video = "[vout2]"
		cmd += final_video


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




	# map the video and audio streams
	cmd += "' -map "+final_video+" -map "+final_audio+" -y "+output


	print(cmd)
	os.system(cmd)
	print("Done! Time elapsed: "+str(time.time()-stime))



# processing subtitles
def processText(words):

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


# processing audio
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
	audios.append(t+float(delta))



