import os, time, ctypes, subprocess, sys, re
from functions import list_video_files_from_path, resize_string, write_pid_to_file, file_is_video, get_frames_count, printProgressBar
from preferences import local_folders, videoformats, FFmpeg, FFmpeg_preset, FFmpeg_acodec, FFmpeg_vcodec


def convert_function(cmd, frames_count):
    print(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        if "frame=" in line:
            try:
                line = re.sub(' +', ' ', line)
                ogline = line
                line = line.replace("= ", "=")
                line = line.split(" ")

                fps = line[1]
                fps = fps.split("=")
                fps = fps[1]
                if fps == "0.0":
                    fps = "1.1"
                fps = float(fps)

                frame = line[0]
                frame = frame.split("=")
                frame = int(frame[1])
                #prog_percent = frame/int(frames_count)
                #prog_percent = str(prog_percent)
                try:
                    estimated_time_sec = float(frames_count)/fps
                except Exception as e:
                    print(e)
                    estimated_time_sec = 1
                m, s = divmod(estimated_time_sec, 60)
                h, m = divmod(m, 60)

                msg = "FPS: {} Remaining time: {}:{}:{} Files: {} Finished: {}".format(fps, int(h), int(m), int(s),
                                                                                       videos_count,
                                                                                       original_videos_count - videos_count)
                printProgressBar(msg, frame, int(frames_count), length=60)
            except Exception as e:
                print(e)
                print(line)
        else:
            print(line)

def convert_file(self):
    split_path = self.split(";")
    file_path = split_path[0]
    file_name = split_path[1]

    input_file = "{}\\{}".format(file_path, file_name)
    output_file = "{}\\HEVC_{}".format(file_path, file_name)

    FFmpeg_rescale = resize_string(input_file)
    print(FFmpeg_rescale)

    frames_count = get_frames_count(input_file)

    cmd = FFmpeg + " \"" + input_file + "\"" + FFmpeg_rescale + FFmpeg_preset + " " + FFmpeg_acodec + " " + FFmpeg_vcodec + " \"" + output_file + "\""
    # cmd_raw = "ffmpeg -i \"{}\" {} -threads 1 -c:v libx265 -preset veryslow -f mp4 -x265-params crf=32:numa-pools=none:threads=1 -strict -2 -c:a mp3 -q:a 8 \"{}\"".format(input_file_path, FFmpeg_rescale, output_file_path)

    time_1 = time.time()
    #p = os.popen(cmd).readline()  # Changed from read to readline
    with open (os.getcwd()+"/lastFile.txt", "w+") as f:
        f.write(output_file)

    convert_function(cmd, frames_count)
    conv_time = time.time() - time_1

    if conv_time > 10:
        print("Removing original file")
        if delete_original_video_file: os.remove(input_file)



def file_counter(list):
    file_count = 0
    for video_file in list:
        if file_is_video(video_file):
            if not "HEVC" in video_file: file_count = file_count + 1
    return file_count

if __name__ == "__main__":
    print("started")
    write_pid_to_file()
    dir_path = "e:/training/waiting_to_convert/"
    delete_original_video_file = True
    videos_list = list_video_files_from_path(dir_path)
    videos_count = len(videos_list)
    original_videos_count = videos_count

    with open(os.getcwd()+"/video_list.txt", "w+")as f:
        for video_file in videos_list:
            if not "HEVC" in video_file: f.write(video_file+"\n")

    for video_file in videos_list:
        if not "HEVC" in video_file:
            videos_list = list_video_files_from_path(dir_path)
            if os.name == 'nt':
                ctypes.windll.kernel32.SetConsoleTitleW("Remaining files: {} Finished: {}".format(videos_count, original_videos_count - videos_count))
            convert_file(video_file)
            videos_count = videos_count - 1
