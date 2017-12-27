import os, time, subprocess, logging
from functions import get_video_file_width, convert_file, grab_video_file
from preferences import max_video_width
#from colorama import Fore, Back, Style

if __name__ == "__main__":
    logging.info('Converter started')
    logging.basicConfig(filename='converter.log', level=logging.DEBUG)

    #Writing the processes pid to a file
    running_process_name = os.path.basename(__file__)
    logging.info(running_process_name[:-3])
    with open(running_process_name[:-3] + ".pid", "w+") as f:
        f.write(str(os.getpid()))

    while True:
        failed_to_convert = False
        #grab_video_file('\VIDEOS\\')

        video_list = os.listdir('VIDEOS')  # Getting video file names to convert

        #Printing out video file list

        logging.info('Found', len(video_list), 'video files to convert')

        input_file = video_list[0]

        if input_file == 'no_video_file':
            logging.info('No file to convert')
        else:
            #video_file=input_file.replace(' ', '%20') # Replacing whitespaces with %20 for FFMpeg in a new variable
            video_file_path = os.getcwd() + '\VIDEOS\\' + input_file # Creating full path to video file
            logging.info('Selected file to convert: ', input_file)
            logging.info('Getting width of video file')

            output_dir = '\WORKING_ON'
            output_file_name = '\HEVC_' + input_file[:-3] + 'mp4'
            output_file_path = os.getcwd() + output_dir + output_file_name

            #Using FFMpeg to convert
            logging.info('Starting to convert')
            convert_start_time = time.time()
            convert_file(video_file_path) # Converting the file
            converting_time = time.time() - convert_start_time

            if int(converting_time) < 5:
                failed_to_convert = True

            try:
                conv_time = time.strftime("%H:%M:%S", time.gmtime(converting_time))
                logging.info('Converting time ' + conv_time)
            except Exception as e:
                logging.info('Failed to calculate converting time: ' + e)

            if not failed_to_convert:

                file_created = os.path.isfile(output_file_path)
                output_file_size = os.path.getsize(output_file_path)

                if file_created:
                    if output_file_size > 0:

                        logging.info('Moving finished file to finished folder')
                        finished_dir = '/FINISHED/'
                        finished_file_path = os.getcwd() + finished_dir + output_file_name
                        os.rename(output_file_path, finished_file_path)

                        logging.info('Moving original file to original_finished folder')
                        original_finished_dir = '/Original_finished/'
                        original_finished_file_path = os.getcwd() + original_finished_dir + input_file
                        os.rename(video_file_path, original_finished_file_path)

            else:
                logging.info('asd' + 123)
                logging.info('Moving original file to ERROR folder')
                original_finished_dir = '/ERROR/'
                original_finished_file_path = os.getcwd() + original_finished_dir + input_file
                os.rename(video_file_path, original_finished_file_path)

            logging.info('process finished, looking for new video file')
        time.sleep(10)
