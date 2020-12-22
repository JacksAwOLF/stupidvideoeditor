import os
from config import *
from helper import *


class Video:
	def __init__(self, source, name, volume):

		if not os.exists(source):
			raise ValueError("FILE "+source+" DOESN'T EXIST!")

		self.source = source
		self.name = "[" + name + "]"
		self.volume = volume
		self.cmd = ""
	
	def update_name(self, prefix):
		last_position = -1
		if ':' in self.name
			last_position = self.name.find(':')
		self.name = "[" + prefix + self.name[1:last_position] + "]"
		self.cmd += self.name + ";"

	def volume(self):
		ind = self.name.find(']')
		cmd = self.name[:ind]+':a]volume='+self.volume
		cmd += '[a'+self.name[1:]
		return cmd

	def loop(self, length, output):
		global resolution
		cmd = "ffmpeg -i "+self.source+" -filter_complex '"
		cmd += "loop=-1:size=1,trim=0:"+str(length)+","
		cmd += "pad="+resolution+",setsar=1:1,format=yuv420p' "
		cmd += "-y -loglevel quiet "+output
		self.source = output
		return cmd

	#def get_resolution():
	#	return get_resolution(self.source)
	def resize(self, res=resolution, stretch_fit=False)
		self.cmd = self.name+"scale="+res
		if not stretch_fit:
			self.cmd += ":force_original_aspect_ratio=decrease"
			self.cmd += ",pad="+res+":-1:-1" # default is centered with black background
		self.cmd += ",setsar=1:1"
		update_name("r")

	def cut(self, start, length, output):
		cmd = "ffmpeg -i "+self.source+" -ss "+start+" -t "
		cmd += length + " -loglevel quiet -y " + output
		self.source = output
		return cmd 




class Audio:
	def __init__(self, source, name):
		self.source = source
		self.name = "[" + name + "]"
		self.cmd = ""

	def update_name(prefix):
		self.name = "[" + prefix + self.name[1:-1] + "]"
		self.cmd += self.name

	def delay()





# cut a media file with ffmpeg
#
# name: name of input file
# start: position in seconds to start cut
# length: either the length in seconds of cut, or
#		the position to end cut; depening to
# final_name: output file name
# to: if to is true, length is the position to end cut
def cut(name, start, length, out, to=False):
	
	# error process
	if not os.path.exists(name):
		raise ValueError("FILE "+name+" DOESN'T EXIST!")

	if os.path.exists(out):
		return
	start = str(start)
	length = str(length)
	if not isnum(start) or not isnum(length):
		raise ValueError("Cutting "+name+" error")

	# length offset
	if "/" in length:
		nn, ll = get_name_length(length)
		length = ll
	if float(length) > cut_limit:
		length = str(float(length) - cut_offset)
	
	# the cut
	cmd = "ffmpeg -i "+name+" -ss "+start+(" -to " if to else " -t ")+length+" -loglevel quiet -y "+out
	print(cmd)
	os.system(cmd)



# loop an image when given the name
def loop_image(beats, name, final_name):

	if os.path.exists(final_name):
		return

	# get image length and fraction name
	frac, image_len = get_name_length(beats)


	image_name = name

	temp_name = "temp/"+name+".mp4"
	if name.find(".") != -1:
		temp_name = "temp/"+name[:name.find(".")]+".mp4"

	# make sure image is scaled
	cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "
	res = os.popen(cmd+image_name).read()[:-1]
	if not res == "1920x1080":
		cmd = 'ffmpeg -i '+image_name+' -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -loglevel quiet -y '
		os.system(cmd+temp_name)
		os.system("ffmpeg -i "+temp_name+" -vf scale=1920:1080,setsar=1:1 -y -loglevel quiet "+image_name)
		print("THIS IS THE RES: "+res)

	# get video from image
	cmd  = "ffmpeg -loop 1 -i "+image_name+" -c:v libx264 -t "+image_len
	cmd += " -pix_fmt yuv420p -loglevel quiet -y "+temp_name
	os.system(cmd)

	# add audio into video
	cmd  = "ffmpeg -i "+temp_name
	cmd += " -i music/silence.mp3 -map 0:v -map 1:a -shortest -loglevel quiet -y "
	cmd += " "+final_name
	os.system(cmd)

	# delete redundant thing
	os.system("rm "+temp_name)
	print(final_name+" image looped")

ffmpeg -i young_abe.jpg

ffmpeg -i young_abe.jpg -i up.mp4 -filter_complex "\
[0:v]loop=-1:size=1,\
trim=0:10, \
setsar=1:1, \
format=yuv420p" -vsync 2 -y b.mp4


ffmpeg -i up.mp4 -filter_complex "trim=10:12, setpts=PTS-STARTPTS" -y out.mp4

ffmpeg -i up.mp4 -i a.mp4 -filter_complex "concat=a=1" -vsync 2 out.mp4


ffmpeg -i hs20.mp4 -filter_complex "pad=1920:1080:-1:-1" up.mp4
ffmpeg -i up.mp4 -i ig.mp4 -filter_complex "[0][1]concat=n=2" -y out.mp4

ffmpeg -i hs20.mp4 -i young_abe.jpb -filter_complex \
"[1] pad=1920:1080, " -y out.mp4 
