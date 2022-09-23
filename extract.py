import mysql.connector
import time,uuid
import librosa,argparse
from tqdm import tqdm
import base64,os
import json



parser = argparse.ArgumentParser(description ='Fetch audio records from KMRL database')

parser.add_argument('--start','-s', 
                    type = int,
                    default=0,
                    help ='start offset')
parser.add_argument('--end','-e', 
                    type = int,
                    help ='end offset')
parser.add_argument('--file','-f', 
                    type = str,
                    required=True,
                    help ='Name of the file in which the dataset should be saved')
parser.add_argument('--directory','-D', 
                    type = str,
                    help ='Name of the directory in which the audios should be saved')
parser.add_argument('-y', 
                   action='store_true',
                    help ='Ignore all warnings')

args = parser.parse_args()
FILE_NAME = args.file
AUDIO_DIR ="audios"
default_choice = 'y' if args.y else 'n'
start = args.start
end = args.end

if end and start >= end:
    print("Start offset should be less than end offset")
    exit(0)



if args.directory:
    AUDIO_DIR = args.directory


audio_path = os.path.join(os.getcwd(), AUDIO_DIR)

if os.path.isdir(AUDIO_DIR):
    if default_choice == 'n' and os.listdir(AUDIO_DIR):
        confirm = input(f"Directory {audio_path} is not empty.\nType y to continue : ")
        if confirm.lower() != 'y':
            exit(0)
        
else:
    print("Created directory")
    os.mkdir(audio_path)

if default_choice == 'n' and os.path.isfile(FILE_NAME):
    confirm = input(f"\n{FILE_NAME} already exists.\n\n• Type n for overwrite the file\n• Type y for continuing with this file\n")
    if confirm.lower() == 'n':
        os.remove(FILE_NAME)
    elif confirm.lower() != 'y':
        exit(0)


dataset_file = open(FILE_NAME,"a", encoding="utf8")

print("\nConnecting to database ...")

mydb = mysql.connector.connect(
host="13.232.6.212",
user="kmrl_project",
password="kmrl#321",
database="kmrl_data_collection"
)
mycursor = mydb.cursor()

print("Connected to database\n")
time.sleep(2)


def audio_duration(path):
    return round(librosa.get_duration(filename=path),7)


if not end:
    mycursor.execute(f"SELECT count(*) from text_audio_dataset")
    myresult = mycursor.fetchall()

    end = myresult[0][0]
    

dataset = []

for i in tqdm(range(start,end)):
    mycursor.execute(f"SELECt word,size,gender,mobile,audio from text_audio_dataset limit 1 offset {i}")
    myresult = mycursor.fetchall()
    for result in myresult:
        a = {}
        decoded = base64.decodebytes(result[4])
        file_path = AUDIO_DIR +"/" + uuid.uuid1().hex + ".wav"
        f = open(file_path, "wb")
        f.write(decoded)
        f.close()
        duration = audio_duration( os.path.join(os.getcwd(),file_path))
        a["audio_filepath"] = file_path
        a["duration"] = duration
        a["text"] = result[0]
        
        dataset_file.write(json.dumps(a,ensure_ascii=False))
        dataset_file.write("\n")
    


# dataset_file.write(json.dumps(dataset,ensure_ascii=False))
mydb.close()
dataset_file.close()

print(f"\nDataset saved at location {os.path.join(os.getcwd(), FILE_NAME)}\nAudio files saved at location {audio_path}")
