import os, csv, time, logging, subprocess
from preferences import local_folders, videoformats, FFmpeg, FFmpeg_preset, FFmpeg_acodec, FFmpeg_vcodec, FB_UID, fb_email, fb_password, send_FB_message
from preferences import max_video_width

def printProgressBar (asd, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), asd, end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def resize_string(self):
    # Getting video's width using mediainfo
    get_width = get_video_file_width(self)
    video_file_width = int(get_width)  # Getting width of video file
    logging.info('Width of video file / max width: {}/{}'.format(video_file_width, max_video_width))
    if int(video_file_width) > max_video_width:  # Setting output file's width
        logging.info("Resizing video to: {}".format(max_video_width))
        FFmpeg_rescale = " -vf scale={}:-1 ".format(max_video_width)
    else:
        logging.info("No resizing needed")
        FFmpeg_rescale = " "
    return FFmpeg_rescale

def file_is_video(self):
    if ".mp4" in self: return True
    else:
        if ".MP4" in self: return True
        else:
            return False

def list_video_files_from_path(self):
    video_list = []
    for root, dirs, files in os.walk(self, topdown=False):
        for name in files:
            file = os.path.join(root, name)
            if file_is_video(file) == True:
                if not "HEVC" in name: video_list.append(root + ";" + name)
    return video_list

def load_filenames():
    file = 'file_names.csv'
    dict = {}
    if os.path.isfile(file):
        f = open(file, 'r')
        for key, val in csv.reader(f, delimiter=';'):
            dict[key] = val
        f.close()
        logging.info('File names loaded successfully!')
        return dict
    else:
        logging.info('Could not load file names')

def create_local_folders():
    for folder in local_folders:
        if not os.path.isdir(os.getcwd() + "/" + local_folders[folder]):
            try:
                os.mkdir(os.getcwd() + "/" + local_folders[folder], 777)
            except Exception as e:
                logging.info("Failed to create directory: " + str(e))
        # else:
        #     logging.info(str(os.getcwd() + "/" + local_folders[folder]))

def get_video_file_width(self):
    cmd_FFProbe = "ffprobe -v error -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 \"" + self + "\""
    cmd_mediainfo = "mediainfo '--Inform=Video; %Width%/String%'" + " \"" + self + "\""

    logging.info(cmd_mediainfo)
    video_width = os.popen(cmd_mediainfo).read()
    logging.info(video_width)
    video_width = video_width.split('\n')
    for line in video_width:
        if "Width" in line:
            line = line.split(':')
            line = line[1]
            line = line[1:-7]
            line = line.replace(" ", "")
            return line

def convert_string_characters(self):
    #self = self.replace(' ', '\ ')
    #self = self.replace('\'', '\\\' ')
    #self = self.replace('\"', '\\\" ')
    #self = self.replace('&', '\&')
    #self = self.replace('#', '\#')
    #self = self.replace('(', '\(')
    #self = self.replace(')', '\)')
    return self

def convert_function(cmd):
    print("STDOUTTTTTTT")
    #p = os.popen(cmd).readline()  # Changed from read to readline
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    for line in iter(p.stdout.readline, b''):
        print(">>> " + line.rstrip())

def get_frames_count(input_file):
    asd = os.popen('mediainfo --fullscan "{}"'.format(input_file)).readlines()
    for line in asd:
        if "Frame count" in line:
            print(line)
            line = line.split(": ")
            return line[1]

    time.sleep(99)
def convert_file(input_file):
    FFmpeg_rescale = " "

    input_file_path = os.getcwd() + "/VIDEOS/" + input_file

    file_name_split = input_file_path.split("/")
    file_name = file_name_split[len(file_name_split)-1]

    output_dir = '/WORKING_ON'
    output_file_name = '/HEVC_' + file_name[:-3] + 'mp4'
    output_file_path = os.getcwd() + output_dir + output_file_name

    #Getting video's width using mediainfo
    get_width = get_video_file_width(input_file_path)
    video_file_width = int(get_width)  # Getting width of video file
    logging.info('Width of video file / max width: {}/{}'.format(video_file_width, max_video_width))
    if int(video_file_width) > max_video_width:   #Setting output file's width
        logging.info("Resizing video to: {}".format(max_video_width))
        FFmpeg_rescale = " -vf scale={}:-1 ".format(max_video_width)
    else:
        logging.info("No resizing needed")
        FFmpeg_rescale = " "

    cmd = FFmpeg + " \"" + input_file_path + "\"" + FFmpeg_rescale + FFmpeg_preset + " " + FFmpeg_acodec + " " + FFmpeg_vcodec + " \"" + output_file_path + "\""
    #cmd_raw = "ffmpeg -i \"{}\" {} -threads 1 -c:v libx265 -preset veryslow -f mp4 -x265-params crf=32:numa-pools=none:threads=1 -strict -2 -c:a mp3 -q:a 8 \"{}\"".format(input_file_path, FFmpeg_rescale, output_file_path)
    logging.info('cmd: ', cmd)
    convert_function(cmd)
    time_1 = time.time()

    conv_time = time.time() - time_1

    if int(conv_time) > 10:
        logging.debug("Looks like converting finished successfully. conv_time > 10")
        logging.debug("Moving files as planned")
        #moving source file to ORIGINAL_FINISHED
        os.rename(input_file_path, os.getcwd() + "/Original_finished/" + file_name)

        #moving converted file to FINISHED
        os.rename(output_file_path, os.getcwd() + "/FINISHED/" + output_file_name)
    else:
        logging.info("Something went wrong. FFMpeg could not convert the file. Moving it to ERROR dir.")
        os.rename(input_file_path, os.getcwd() + "/ERROR/" + file_name)

def grab_video_file(dir):
    logging.info("Grabbing video file")
    multi_dir = "/VIDEOS_Multi/"
    files = os.listdir(os.getcwd() + multi_dir)
    logging.info(files[0])
    os.rename(os.getcwd() + multi_dir + files[0], os.getcwd() + dir + files[0])

def write_pid_to_file():
    running_process_name = os.path.basename(__file__)
    logging.info(running_process_name[:-3])
    with open(running_process_name[:-3] + ".pid", "w+") as f:
        f.write(str(os.getpid()))

def remove_unfinished_files():
    working_on_path = os.getcwd() + "/WORKING_ON/"
    remained_files = os.listdir(working_on_path)
    for file in remained_files: os.remove(working_on_path + file)  # Removing files from WORKING_ON folder