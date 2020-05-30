
from playsound import playsound
import sys

str = sys.path[0]
file = eval(repr(str).replace('\\', '/'))
file_name = file + ''
print(file_name)
playsound(file_name)