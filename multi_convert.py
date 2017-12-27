import os, multiprocessing, logging, time
from functions import convert_file, write_pid_to_file, create_local_folders, remove_unfinished_files

if __name__ == '__main__':
    logging.info('Converter started')
    logging.basicConfig(filename='converter.log', level=logging.DEBUG)

    remove_unfinished_files()

    write_pid_to_file()
    create_local_folders()
    files_list = os.listdir(os.getcwd() + "/VIDEOS/")

    p = multiprocessing.Pool()
    p.map(convert_file, files_list)

    p.join()
    p.start()