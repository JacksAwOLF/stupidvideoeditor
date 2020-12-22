HOW TO MAKE YOUR OWN VIDEO PROJECT
WITH THIS THINGY


1. Get all the videos in one folder, named.
ffprobe: check video dimensions
TODO: write script to make all videos same dimension and SAR


2. Map out the video
which videos/images to cut
where to cut
how much to cut
ffplay: check where to cut vids


3. Write a file mapping

HOW COMMENTS WORK

# are comments
# in line comments work too
videos are just names but you can add a length after it too to make it more readable
also, /* */


HOW NUMBERS WORK

	If the number has a decimal point (ie: 1.0 1.5), then the unit is seconds.
	Otherwise (ie: 1/5 2) the unit is in beats, which by default is 1.

# 'beat' number: sets 'beat' to 'number' seconds


HOW TIMING WORKS

	Video and images are like timestamps.
	When inserting audio/text, if placed before a video/image
and it will insert the audio/text at the time that the
following video/image is displayed.

# videofile
# numbeats imagefile
# numbeats videofile startpos 



HOW FILES WORK



HOW AUDIO WORKS

	The audio stream for all the videos and images in the project
are merged into the output audio track. 
  Image audio is silence
	Video by default comes with audio, which can be dimmed with 'vidaud'
	1 meaning full volume, 0 meaning no volume

# 'vidaud' multiplier-between-0-and-1

	On top of that audio stream, you can add audio clips
which are merged with the previous audio stream
	Weight is the loudness of this audio clip if the main audio stream
has a loudness of 100. It's a relative number.
	Delta is a number that accounts for how much to shift the start
of this audio clip by. This is useful if you want a clip to play
in the middle of a video/image. It can be a negative number.

# 'audio' file start end (weight) (delta)
# 'audio' file (weight) (delta)



HOW TEXTS WORK

	Similar to audio, this is text.
# 'text' x,y duration size color text

Hello, j is a k.		

HOW CUTS WORK

	In any project, there are inevitablyy stuff that you want to fiddle 
around with and other stuff that you are pretty set on. You could utilize
comments to do so, or you could specify that.
	By default, all cuts of a video will be saved in cuts/ with the name
			originalname__(cutlength)__(cutposition).originalsuffix
and images are saved with
			originalname__(looplength).videosuffix
	The numbers are in unit seconds up to 2 decimals, and the '.' is 
replaced with '-'. ie: 1.25 => __1-25__
	
	Future cuts of the same videoname, start, and cutlength would just 
return this video instead.
	This saves some time, but uses plenty storage. You can run 'make clean'
to clean the cuts, or add an '*' at the end of a line to disable this 
behavior for that line. 'disable savecuts' can be added at the start to 
disable entirely.


4.  Open evid.py and configure variables at the top
how many seconds per beat
where are the video files
where to store the cuts

5. run "python evid.py" in terminal!





# resizing resolution
ffmpeg -i xxx  -vf scale=1920x1080,setsar=1:1

# mixing audios
ffmpeg -i input0.mp3 -i input1.mp3 -filter_complex amix=inputs=2:duration=longest output.mp3

# mix video and  audio
ffmpeg -i  vid -i aud  -map  0:v  -map 1:a output




https://ffmpeg.org/ffmpeg-utils.html#color-syntax