import json
import os
import subprocess

# getfilePathsRecursively gets path of any video file in any subdirectory and returns a list of filepaths relative to rootdir
# Only cares about these filetypes: mkv, mp4 and mov
def getfilePathsRecursively(directory):
    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in [f for f in filenames if f.lower().endswith((".mkv", ".mp4",".mov"))]:
            files.append(os.path.join(dirpath, filename))
    return files

# getVideoCodec uses ffmpegs ffprobe to get stream information in JSON format
# Note: FFMPEG needs to be added to your path for this to work
def getVideoCodec(file_path):
    # define command
    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name',
        '-of', 'json',
        file_path
    ]
    
    # execute command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # parse JSON output
    try:
        ffprobe_output = json.loads(result.stdout)
        codec_name = ffprobe_output['streams'][0]['codec_name']
        return codec_name
    except (KeyError, IndexError, json.JSONDecodeError):
        return None

def main():
    rootdir = ".\\"
    fileList = getfilePathsRecursively(rootdir)
    for file in fileList:
        codec = getVideoCodec(file)
        if codec:
            print(f'{codec}:\t{file}:')
        else:
            print(f'{file}: Could not determine the video codec.')

main()
# USAGE: Put python script in rootfolder and it will check any video file in any subdir and tell you its video codec.