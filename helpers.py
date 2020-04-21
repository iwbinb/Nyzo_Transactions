import datetime
import string, random
import os

def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')

def printEncloseInput():
    print(makePrettyUiLine(''))
    print(makePrettyUiLine('', enclosing=True))

def makePrettyUiLine(line, enclosing=False):
    if enclosing:
        return '********************************************************************************'
    line_length = 80
    pre = '*    '
    pre_line = pre+line
    for key in colorPrint.len_dict:
        if key in pre_line:
            line_length += colorPrint.len_dict[key]
    line_diff = line_length - len(pre_line)
    for i in range(line_diff):
        if i == line_diff-1:
            pre_line += '*'
        else:
            pre_line += ' '

    return pre_line

class colorPrint:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   len_dict = {"\033[95m":len(PURPLE), "\033[96m":len(CYAN),
               "\033[36m":len(DARKCYAN), "\033[94m":len(BLUE),
               "\033[92m":len(GREEN), "\033[93m":len(YELLOW), "\033[91m":len(RED),
               "\033[1m":len(BOLD), "\033[4m":len(UNDERLINE), "\033[0m":len(END)}

def logPretty(to_log, color=colorPrint.GREEN):
    print(makePrettyUiLine('[{}]: '.format(getDateHuman())+color+to_log+colorPrint.END))

def getTimestampSeconds():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))

def getDateHuman():
    return datetime.datetime.fromtimestamp(getTimestampSeconds()).isoformat()

def generateRunId(length=24):
    set = string.ascii_lowercase
    return ''.join(random.choice(set) for i in range(length))