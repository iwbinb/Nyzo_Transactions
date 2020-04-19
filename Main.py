from Configurations import Configurations, NetworkObserverConfigurations
import os

def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')

def makePrettyUiLine(line, enclosing=False):
    if enclosing:
        return '********************************************************************************'
    line_length = 80
    pre = '*    '
    pre_line = pre+line
    line_diff = line_length - len(pre_line)
    for i in range(line_diff):
        if i == line_diff-1:
            pre_line += '*'
        else:
            pre_line += ' '

    return pre_line

def showMainMenu():
    main_menu = """{}\n{}\n{}\n{}\n{}\n{}\n{}""".format(
        makePrettyUiLine(''),
        makePrettyUiLine('[1] - View Network Observers saved on disk'),
        makePrettyUiLine('[2] - Add Network Observer'),
        makePrettyUiLine('[3] - Update Network Observer from disk'),
        makePrettyUiLine('[4] - Delete Network Observer from disk'),
        makePrettyUiLine(''),
        makePrettyUiLine('', True)
    )
    print(main_menu)

def showUiStart(version):
    print("""
********************************************************************************
*                             _ __  _   _ _______                              *
*                            | '_ \| | | |_  / _ \                             *     
*                            | | | | |_| |/ / (_) |                            *
*                            |_| |_|\__, /___\___/                             *
*                                   |___/                                      *
*                                                                              *
*                            Nyzo_Transactions v{}                            *
*                                by x00x0x00x                                  *
*                                                                              *
********************************************************************************""".format(version))
    showMainMenu()

# def processingLoop

if __name__ == "__main__":
    configurations = Configurations()
    if configurations.showGuiOnStartup:
        showUiStart(configurations.version)
