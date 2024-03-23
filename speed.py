from optparse import OptionParser
import os, time, sys

#option parser
parser = OptionParser(usage="""Run annotation.py \n Usage: %prog [options]""")
parser.add_option("-i","--interval",action = 'store',type = 'string',dest = 'INTERVAL',help = "")
(opt, args) = parser.parse_args()

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
    file_LIST = os.listdir(target)
    file_DICT = {}
    for file in file_LIST:
        file_DICT[file] = os.path.getsize(file)

    return file_DICT, file_LIST

if opt.INTERVAL == None:
    interval = 10
else:
    interval = opt.INTERVAL

target = '.'

bTime = time.time()
bFile_DICT, bFile_LIST = get_fileList(target)

while True:
    time.sleep(interval)
    cTime = time.time()
    cFile_DICT, cFile_LIST = get_fileList(target)

    print("===============================================================")
    totalDiffSize = 0
    totalSize = 0
    for cFile in cFile_LIST:
        diffSize = cFile_DICT[cFile] - bFile_DICT.get(cFile, 0)
        totalSize += cFile_DICT[cFile]
        if diffSize == 0:
            continue

        totalDiffSize += diffSize
        speed = diffSize / (cTime - bTime)

        print(('[{0}/s]  {1} {2}').format(get_fileFormat(speed), get_fileFormat(cFile_DICT[cFile]), cFile))
    print('')
    speed = totalDiffSize / (cTime - bTime)
    print(('Total {0}/s      {1}').format(get_fileFormat(speed), get_fileFormat(totalSize)))