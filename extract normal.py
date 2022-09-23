from dataclasses import replace
import mysql.connector
import time,sys,uuid
import librosa
from tqdm import tqdm
import base64,os
import datetime,json



path = os.path.join(os.getcwd(), "b")

# os.mkdir(path)



mydb = mysql.connector.connect(
host="13.232.6.212",
user="kmrl_project",
password="kmrl#321",
database="kmrl_data_collection"
)
mycursor = mydb.cursor()

print("Connected to database\n")
time.sleep(2)
# w = [")","("]
# def filter_word(word):
#     for k in w:
#         word = word.replace(k,"")
#     return word

def audio_duration(path):
    return round(librosa.get_duration(filename=path),7)

mycursor.execute(f"SELECT count(*) from text_audio_dataset")
myresult = mycursor.fetchall()

# count = myresult[0][0]
count = 10

dataset = []

for i in tqdm(range(count)):
    mycursor.execute(f"SELECt word,size,gender,mobile,audio from text_audio_dataset limit 1 offset {i}")
    myresult = mycursor.fetchall()
    for result in myresult:
        a = {}
        decoded = base64.decodebytes(result[4])
        now = datetime.datetime.now()
        # file_path  = "b/" + str(now).replace(" ","").replace(":","_").replace("-","_") + ".wav"
        file_path ="b/" + uuid.uuid4().hex + ".wav"
        f = open(file_path, "wb")
        f.write(decoded)
        f.close()
        duration = audio_duration( os.path.join(os.getcwd(),file_path))
        a["audio_filepath"] = file_path
        a["duration"] = duration
        a["text"] = result[0]
        
        dataset.append(a)
    

print("Fetching Finished")

dataset_file = open("b.json","w", encoding="utf8")

dataset_file.write(json.dumps(dataset,ensure_ascii=False))
        
dataset_file.close()

print("Dataset created")
# with open(file_name,"r") as f:
#     for i in tqdm(range(total_words)):
#         word = f.readline()
#         if word == " " or len(word) < 2:
#             continue
#         mycursor.execute(f"INSERT INTO text_doc(word) VALUES('{filter_word(word.strip())}'")
#         if i % 10 == 0:
#             mydb.commit()
#         time.sleep(3)
#mydb.commit()
