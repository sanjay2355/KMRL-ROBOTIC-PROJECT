import mutagen,os
from mutagen.wave import WAVE

def audio_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
  
    return hours, mins, seconds
path = os.path.join(os.getcwd(),"audios")
path = os.path.join(path,"2022-08-0114-45-19.036309.wav")
print(path)
#os.chdir(path)
audio = WAVE("C:\\Users\\rohit\\OneDrive\\Desktop\\random\\audios\\2022-08-0114:45:17.459769.wav")

audio_info = audio.info
length = int(audio_info.length)
hours, mins, seconds = audio_duration(length)
print('Total Duration: {}:{}:{}'.format(hours, mins, seconds))