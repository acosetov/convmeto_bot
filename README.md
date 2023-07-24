# Telegram Bot for Audio Messages and Image Analysis
### Project Overview:
This project aims to develop a Telegram bot that can handle audio messages and analyze images for the presence of faces. The bot will be built using Python and will utilize MongoDB for audio message storage and OpenCV for image analysis. The main functionalities of the bot include:
1. Saving audio messages from Telegram dialogs to a MongoDB database.
2. Converting audio messages to the WAV format with a sampling rate of 16kHz.
3. Analyzing images to determine if there is a face present, and saving only the images that meet this criterion.
### Project Features:
1. Audio Message Storage:
The bot will be able to receive and save audio messages from Telegram dialogs to a MongoDB database. Each user's audio messages will be associated with their unique identifier (UID) and stored in the following format:
`uid -> [audio_message_0, audio_message_1, ..., audio_message_N]`
2. Audio Conversion:
All audio messages received by the bot will be converted to the WAV format with a sampling rate of 16kHz. This conversion will ensure uniformity in audio file types and make further processing easier.
3. Image Analysis for Faces:
The bot will analyze images sent by users to determine if there are any faces present in them. For images containing faces, the bot will save them; otherwise, the image will not be stored.

### Technologies Used:
-   Python: The primary programming language for developing the Telegram bot and handling audio and image processing tasks.
-   MongoDB: To store audio messages from Telegram dialogs.
-   OpenCV: To perform image analysis and face detection on the received images.
-   Telegram API: To interact with Telegram and receive messages from users.
