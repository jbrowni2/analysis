import os
import hcdataprocessdef


hcdataprocessdef.addruns("/research/raw/data")

que = hcdataprocessdef.get_query()

os.system("rm fileDB.h5")

os.system("./setup.py --init")

command = 'python3 -W ignore processing.py -q "run == ' + str(que) + '" --d2r -o'

os.system(command)

command = 'python3 -W ignore processing.py -q "run == ' + str(que) + '" --r2d -o'

os.system(command)
