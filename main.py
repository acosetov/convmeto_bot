import os
import io
import numpy as np
import cv2
import pymongo
import telebot
from pydub import AudioSegment
from dotenv import load_dotenv, find_dotenv

# Take environment variables from .env
load_dotenv(find_dotenv())

# Initialize the Telegram bot
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

# Initialize MongoDB connection
mongo_client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client[os.getenv("MONGODB_DB_NAME")]
collection = db[os.getenv("MONGODB_COLLECTION_NAME")]

def process_audio_message(user_id, file_id):
    # Download audio file from Telegram
    file_info = bot.get_file(file_id)
    audio_path = file_info.file_path
    audio_file = bot.download_file(audio_path)
    print(file_info)

    # Convert audio to WAV with 16kHz sampling rate using pydub
    audio = AudioSegment.from_file(io.BytesIO(audio_file), format="ogg")
    audio = audio.set_frame_rate(16000)
    wav_file_path = f"{file_id}.wav"
    audio.export(wav_file_path, format="wav")

    # Save audio file to MongoDB
    with open(wav_file_path, "rb") as wav_file:
        collection.update_one({"user_id": user_id}, {"$push": {"audio_messages": wav_file.read()}}, upsert=True)

    # Remove the temporary WAV file
    os.remove(wav_file_path)

    # Send completion message to the user
    bot.send_message(user_id, "Audio message processing is complete!")

def process_photo_message(user_id, file_id):
    # Download photo from Telegram
    file_info = bot.get_file(file_id)
    photo_path = file_info.file_path
    photo_file = bot.download_file(photo_path)

    # Detect face using OpenCV
    np_arr = np.frombuffer(photo_file, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Save photo to MongoDB if face is detected
    if len(faces) > 0:
        collection.update_one({"user_id": user_id}, {"$push": {"photos": photo_file}}, upsert=True)
        bot.send_message(user_id, "Photo processing is complete!")
    else:
        bot.send_message(user_id, "Sorry, I can't detect a face in the image. Please try loading another image.")

@bot.message_handler(content_types=['voice'])
def handle_audio_message(message):
    user_id = message.from_user.id
    file_id = message.voice.file_id
    process_audio_message(user_id, file_id)

@bot.message_handler(content_types=['photo'])
def handle_photo_message(message):
    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    process_photo_message(user_id, file_id)

def main():
    bot.polling()

if __name__ == "__main__":
    main()
