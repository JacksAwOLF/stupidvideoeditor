# every ffmpeg cut is a little too long
# so here's the offset
cut_offset = 0.02
cut_limit = 0.8


# file to follow to merge everything
file = "order" 							

# how many seconds is in one unit of time
beat = 1									

# how loud the audio from the video is (0-1)
vidaud = "1"								

textbox_alpha = "0.2"
resolution = "1920x1080"

# video, image, audido, where to store cuts, where to store video-images
folders = ["vids/","pics/","auds/","cuts/","pics/"]

# video, image, audio suffixes to loop through when suffix isn't specified in file
suffixes = [[".mp4", ".mov", ".MOV"], [".jpg", ".png"], [".mp3", ".wav"]]

# final output video name
output = "finalOutput.mp4"