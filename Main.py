from Configurations import Configurations, NetworkObserverConfigurations
import os
import ast

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
    for key in printColor.len_dict:
        if key in pre_line:
            line_length += printColor.len_dict[key]
    line_diff = line_length - len(pre_line)
    for i in range(line_diff):
        if i == line_diff-1:
            pre_line += '*'
        else:
            pre_line += ' '

    return pre_line

class printColor:
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

#

def showMenu_ViewNetworkObserversSaved():
    with open('stored_NetworkObservers', 'r') as f:
        dict_list = ast.literal_eval(f.readline())
        print(makePrettyUiLine(''))
        print(makePrettyUiLine('Total observers: '+str(len(dict_list))))
        for i in dict_list:
            print(makePrettyUiLine(''))
            print(makePrettyUiLine('[observer_identifier]: '+printColor.BOLD+str(i['observer_identifier'])+printColor.END))
            print(makePrettyUiLine('[ip_address]: '+printColor.BOLD+i['ip_address']+printColor.END))
            print(makePrettyUiLine('[consider_missing_blocks]: ' +printColor.BOLD+ str(i['consider_missing_blocks'])+printColor.END))
            print(makePrettyUiLine('[consider_frozen_edge_discrepancy]: ' +printColor.BOLD+ str(i['consider_frozen_edge_discrepancy'])+printColor.END))
            print(makePrettyUiLine('[consider_fetching_unreliability]: ' +printColor.BOLD+ str(i['consider_fetching_unreliability'])+printColor.END))
            print(makePrettyUiLine('[chunk_size_missing_blocks]: ' +printColor.BOLD+ str(i['chunk_size_missing_blocks'])+printColor.END))
            print(makePrettyUiLine('[failed_fetch_minimum_seconds_passed]: ' +printColor.BOLD+ str(i['failed_fetch_minimum_seconds_passed'])+printColor.END))
            print(makePrettyUiLine('[allowed_frozenEdge_sync_discrepancy]: ' +printColor.BOLD+ str(i['allowed_frozenEdge_sync_discrepancy'])+printColor.END))
            print(makePrettyUiLine('[url_prepend]: ' +printColor.BOLD+ i['url_prepend']+printColor.END))
            print(makePrettyUiLine('[url_append]: ' +printColor.BOLD+ i['url_append']+printColor.END))
            print(makePrettyUiLine(''))
            print(makePrettyUiLine('##########          ##########          ##########          ##########'))
    print(makePrettyUiLine('', enclosing=True))
#

def menuHandler_AddNetworkObserver():
    print('add')

def showMenu_AddNetworkObserver():
    print('add')

def menuHandler_UpdateNetworkObserver():
    print('add')

def showMenu_UpdateNetworkObserver():
    print('update')

def menuHandler_DeleteNetworkObserver():
    print('add')

def showMenu_DeleteNetworkObserver():
    print('del')

#

def mainMenuHandler(error_raised):
    if error_raised:
        print(makePrettyUiLine('', enclosing=True))
        print(makePrettyUiLine(''))
        print(makePrettyUiLine('Command invalid, please try again'))
        print(makePrettyUiLine('To view the main menu, use the "main" command'))
        print(makePrettyUiLine(''))
    input_result = input('*    // Select option: ')
    printEncloseInput()
    if input_result is '1':
        showMenu_ViewNetworkObserversSaved()
    elif input_result is '2':
        showMenu_AddNetworkObserver()
    elif input_result is '3':
        showMenu_UpdateNetworkObserver()
    elif input_result is '4':
        showMenu_DeleteNetworkObserver()
    elif input_result is '5':
        initiate_MainLoop()
    elif input_result == 'main':
        showMainMenu()
    else:
        print(makePrettyUiLine(''))
        print(makePrettyUiLine('Invalid command: '+input_result))
        print(makePrettyUiLine(''))
        mainMenuHandler(error_raised=True)

def showMainMenu():
    main_menu = """{}\n{}\n{}\n{}\n{}\n{}\n{}""".format(
        makePrettyUiLine(''),
        makePrettyUiLine('[1] - View Network Observers saved on disk'),
        makePrettyUiLine('[2] - Add Network Observer'),
        makePrettyUiLine('[3] - Update Network Observer from disk'),
        makePrettyUiLine('[4] - Delete Network Observer from disk'),
        makePrettyUiLine('[5] - Start'),
        makePrettyUiLine(''),
        makePrettyUiLine('', enclosing=True)
    )
    print(main_menu)
    mainMenuHandler(error_raised=False)

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

#

def initiate_MainLoop():
    print('main')

#

if __name__ == "__main__":
    configurations = Configurations()
    if configurations.showGuiOnStartup:
        showUiStart(configurations.version)
    else:
        while True:
            initiate_MainLoop()
