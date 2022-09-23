import json
import librosa
from tqdm import tqdm
import os

# def audio_duration(length):
#     hours = length // 3600  # calculate in hours
#     length %= 3600
#     mins = length // 60  # calculate in minutes
#     length %= 60
#     seconds = length  # calculate in seconds
  
#     return hours, mins, seconds

def audio_duration(path):
    return round(librosa.get_duration(filename=path),7)

# print(audio_duration("audios/2022-08-0114-45-17.459769.wav"))
# audio = WAVE("alarm.wav")


d = open("dataset.json","r",encoding="utf8")

dataset = json.loads(d.read())
d.close()  
for i in tqdm(range(len(dataset))):
    result = dataset[i]
    path = result["audio_filepath"].replace(":","-")
    
    # path = os.path.join(path,result["audio_filepath"].replace("audios/",""))
   
    duration = audio_duration(path)
    
    result["duration"] = duration
    
f = open("final.json","w",encoding="utf8")
f.write(json.dumps(dataset,ensure_ascii=False))




