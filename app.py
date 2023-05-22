from flask import Flask, render_template, send_from_directory, Response
import os
import random
import threading
import time

app = Flask(__name__)

app.config['RADIO_FOLDER'] = "radio/"
app.config['UNCONVERTED_FOLDER'] = "unconverted/"
app.config['CONVERTED_TO_WAV_FOLDER'] = "converted_to_wav/"
app.config['CONVERTED_TO_DFPWM_FOLDER'] = "converted_to_dfpwm/"

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

RADIO_FOLDER_CONTENT = os.listdir(app.config['RADIO_FOLDER'])
RADIO_FOLDER_SIZE = get_dir_size(path='radio/')

def update_RADIO_FOLDER_CONTENT_list():
    global RADIO_FOLDER_CONTENT
    while True:
        RADIO_FOLDER_CONTENT = os.listdir(app.config['RADIO_FOLDER'])
        time.sleep(20)

def update_RADIO_FOLDER_SIZE():
    global RADIO_FOLDER_SIZE
    while True:
        RADIO_FOLDER_SIZE = get_dir_size(path='radio/')
        time.sleep(20)

def get_track():
    tracks = RADIO_FOLDER_CONTENT
    if len(tracks) == 1:
        return tracks[0]
    else:
        choosentrack = random.choice(tracks)
        return choosentrack

@app.route('/', methods=['GET'])
def index():
    available_tracks = len(RADIO_FOLDER_CONTENT)
    tracks_waiting_to_wav = len(os.listdir(app.config['UNCONVERTED_FOLDER']))
    tracks_waiting_to_dfpwm = len(os.listdir(app.config['CONVERTED_TO_WAV_FOLDER']))
    tracks_waiting_added_to_radio = len(os.listdir(app.config['CONVERTED_TO_DFPWM_FOLDER']))
    radio_folder_size_tp_var = round(RADIO_FOLDER_SIZE / (1024*1024*1024), 2)
    return render_template('index.html', available_tracks=available_tracks,
                           tracks_waiting_to_wav=tracks_waiting_to_wav,
                           tracks_waiting_to_dfpwm=tracks_waiting_to_dfpwm,
                           tracks_waiting_added_to_radio=tracks_waiting_added_to_radio,
                           radio_folder_size=radio_folder_size_tp_var
                           )

@app.route('/ping', methods=['GET'])
def ping_flask_app():
    return "pong!"

@app.route('/radio', methods=['GET'])
def radio_route():
    track = get_track()
    with open(os.path.join(app.config['RADIO_FOLDER'], track), "rb") as f:
        track_data = f.read()
    return Response(track_data, content_type="application/octet-stream")


@app.route('/radio/random', methods=['GET'])
def radio_random_route():
    track = get_track()
    return track

@app.route('/track/<track>', methods=['GET']) # type: ignore
def track_route(track):
    if os.path.isfile(app.config['RADIO_FOLDER'] + track):
        return send_from_directory(app.config['RADIO_FOLDER'], track, as_attachment=True)
    else:
        return "Track not found"

@app.route('/songs', methods=['GET'])
def songs_route():
    return RADIO_FOLDER_CONTENT


if __name__ == "__main__":
    update_RADIO_FOLDER_CONTENT_thread = threading.Thread(target=update_RADIO_FOLDER_CONTENT_list)
    update_RADIO_FOLDER_CONTENT_thread.name = "UpdateRadioFolderListThread"
    update_RADIO_FOLDER_CONTENT_thread.start()

    update_RADIO_FOLDER_SIZE_thread = threading.Thread(target=update_RADIO_FOLDER_SIZE)
    update_RADIO_FOLDER_SIZE_thread.name = "UpdateRadioFolderSizeThread"
    update_RADIO_FOLDER_SIZE_thread.start()

    app.run('127.0.0.1', 5000, True, True)
