from pybvb.util import *
import datetime
import time, os


def timer(timepoints):
    hr = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    now_time = [hr, min]
    return (now_time in timepoints)


autolog = open('automator_log.txt', 'w+', encoding='utf-8')


if __name__ == '__main__':

    while(True):
        timepoints = [[4, 0], [10, 0], [16, 0], [22, 0]]
        if timer(timepoints):
            try:
                import main
                autolog.write('Successfully executed spider: {:s}\n'.format(GetNowTimeTx()))
            except:
                autolog.write('Encountered error when executing spider: {:s}\n'.format(GetNowTimeTx()))
        time.sleep(30)
