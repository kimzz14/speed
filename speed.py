from optparse import OptionParser
import os, time, sys
import subprocess
#option parser
parser = OptionParser(usage="""Run annotation.py \n Usage: %prog [options]""")
parser.add_option("-i","--interval",action = 'store',type = 'int',dest = 'INTERVAL',help = "")
parser.add_option("-t","--target",action = 'store',type = 'string',dest = 'TARGET',help = "")
(opt, args) = parser.parse_args()

if opt.INTERVAL == None:
    interval = 10
else:
    interval = opt.INTERVAL

if opt.TARGET == None:
    target = '*'
else:
    target = opt.TARGET

def get_fileFormat(fiseSize):
    fiseSize = float(fiseSize)

    if fiseSize < 1024 : #Byte
        return "%8.2f  B" % (fiseSize)
    elif fiseSize < 1024*1024 : #KiloByte
        return "%8.2f KB" % (fiseSize/1024)
    elif fiseSize < 1024*1024*1024 : #MegaByte
        return "%8.2f MB" % (fiseSize/1024/1024)
    else :
        return "%8.2f GB" % (fiseSize/1024/1024/1024)

def get_fileList(target):
    command = f'du -bsc {target}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    file_DICT = {}
    file_LIST = []
    for line in stdout.decode('utf-8').rstrip('\n').split('\n'):
        size, file = line.split('\t')
        file_LIST += [file]
        file_DICT[file] = int(size)

    return file_DICT, file_LIST

bFile_DICT, bFile_LIST = get_fileList(target)

while True:
    time.sleep(interval)
    cFile_DICT, cFile_LIST = get_fileList(target)

    print("===============================================================")
    for cFile in cFile_LIST:
        diffSize = cFile_DICT[cFile] - bFile_DICT.get(cFile, 0)
        if diffSize == 0:
            continue

        speed = diffSize / (interval)

        print(('[{0}/s]  {1} {2}').format(get_fileFormat(speed), get_fileFormat(cFile_DICT[cFile]), cFile))
    print('')
    bFile_DICT, bFile_LIST = cFile_DICT, cFile_LIST