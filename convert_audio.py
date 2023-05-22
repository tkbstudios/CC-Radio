import os
import ffmpeg

UNCONVERTED_MP3_TRACKS = os.listdir("unconverted/")

for tracktoconvname in UNCONVERTED_MP3_TRACKS:
    splitted_track_name = tracktoconvname.split(".")
    splitted_track_length = len(splitted_track_name)
    track_extension = splitted_track_name[splitted_track_length - 1]
    track_name_no_extension = tracktoconvname.replace(f".{track_extension}", "")

    print(f"Converting {track_name_no_extension}")
    try:
        output_filename = (
            track_name_no_extension.replace(" ", "")
            .replace("-", "")
            .replace("_", "")
            .replace("," ,"")
            )
        input_stream = ffmpeg.input(f"unconverted/{tracktoconvname}")
        output_stream = ffmpeg.output(input_stream, f"converted_to_wav/{output_filename}.wav")
        ffmpeg.run(output_stream, overwrite_output=True)

        print(f"Converted {track_name_no_extension}!")
    except KeyboardInterrupt:
        continue
    except ffmpeg.Error:
        print(f"Error converting {tracktoconvname}")
        os.remove(os.path.join("unconverted/", tracktoconvname))
        print(f"Removed {tracktoconvname}!")
        continue

    if os.path.exists(f"converted_to_wav/{output_filename}.wav"):
        os.remove(f"unconverted/{tracktoconvname}")
        print("Removed unconverted file!")

print(f"DONE CONVERTING {len(UNCONVERTED_MP3_TRACKS)} TO WAV")

unconverted_wav_tracks = os.listdir("converted_to_wav/")

for tracktoconvname in unconverted_wav_tracks:
    splitted_track_name = tracktoconvname.split(".")
    splitted_track_length = len(splitted_track_name)
    track_name_no_extension = tracktoconvname.replace(f".wav", "")
    output_filename = (
        track_name_no_extension
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace("," ,"")
        )
    print(f"Converting {track_name_no_extension}")

    input_file = "converted_to_wav/" + track_name_no_extension + ".wav"
    output_file = "converted_to_dfpwm/" + track_name_no_extension + ".dfpwm"

    ffmpeg.input(input_file).output(
            output_file,
            format="wav",
            acodec="dfpwm",
            ar=48000,
            ac=1
        ).run(quiet=True, overwrite_output=True)

    print(f"Converted {track_name_no_extension}!")
    converted_path = output_file
    if os.path.exists(input_file):
        os.remove(input_file)
        print(f"Removed unconverted {track_name_no_extension}!")

print(f"DONE CONVERTING {len(unconverted_wav_tracks)} TO DFPWM")

move_usr_input = input("Move to radio folder? (y or n): ")
if move_usr_input == "y":
    for track_to_move in os.listdir("converted_to_dfpwm/"):
        os.system("mv converted_to_dfpwm/*.* radio/*")

print("DONE CONVERTING")
