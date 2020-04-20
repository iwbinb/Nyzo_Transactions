from Configurations import Configurations, NetworkObserverConfigurations
from helpers import getDateHuman
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

#

def showMenu_ViewNetworkObserversSaved():
    with open('stored_NetworkObservers', 'r') as f:
        dict_list = ast.literal_eval(f.readline())
        print(makePrettyUiLine(''))
        print(makePrettyUiLine('Total observers: '+str(len(dict_list))))
        for i in dict_list:
            print(makePrettyUiLine(''))
            print(makePrettyUiLine('[observer_identifier]: '+colorPrint.BOLD+str(i['observer_identifier'])+colorPrint.END))
            print(makePrettyUiLine('[ip_address]: '+colorPrint.BOLD+i['ip_address']+colorPrint.END))
            print(makePrettyUiLine('[consider_missing_blocks]: ' +colorPrint.BOLD+ str(i['consider_missing_blocks'])+colorPrint.END))
            print(makePrettyUiLine('[consider_frozen_edge_discrepancy]: ' +colorPrint.BOLD+ str(i['consider_frozen_edge_discrepancy'])+colorPrint.END))
            print(makePrettyUiLine('[consider_fetching_reliability]: ' +colorPrint.BOLD+ str(i['consider_fetching_reliability'])+colorPrint.END))
            print(makePrettyUiLine('[chunk_size_missing_blocks]: ' +colorPrint.BOLD+ str(i['chunk_size_missing_blocks'])+colorPrint.END))
            print(makePrettyUiLine('[failed_fetch_minimum_seconds_passed]: ' +colorPrint.BOLD+ str(i['failed_fetch_minimum_seconds_passed'])+colorPrint.END))
            print(makePrettyUiLine('[allowed_frozenEdge_sync_discrepancy]: ' +colorPrint.BOLD+ str(i['allowed_frozenEdge_sync_discrepancy'])+colorPrint.END))
            print(makePrettyUiLine('[url_prepend]: ' +colorPrint.BOLD+ i['url_prepend']+colorPrint.END))
            print(makePrettyUiLine('[url_append]: ' +colorPrint.BOLD+ i['url_append']+colorPrint.END))
            print(makePrettyUiLine(''))
            print(makePrettyUiLine('##########          ##########          ##########          ##########'))
    print(makePrettyUiLine('', enclosing=True))
#

def menuHandler_AddNetworkObserver(error_raised):
    global initialized_configurations
    if error_raised:
        print(makePrettyUiLine('', enclosing=True))
        print(makePrettyUiLine(''))
        print(makePrettyUiLine('A typing error was raised, please try again'))
        print(makePrettyUiLine('To view the main menu, use the "main" command'))
        print(makePrettyUiLine(''))

    print(makePrettyUiLine(''))
    print(makePrettyUiLine('Fill out the following parameters, press [ENTER] to use the default value'))
    print(makePrettyUiLine(''))

    input_ip_address = input('*    //string// IP address: ')
    input_consider_missing_blocks = input('*    //boolean// Consider missing blocks [default=True]: ')
    input_consider_frozen_edge_discrepancy = input('*    //boolean// Consider frozen edge discrepancy [default=True]: ')
    input_consider_fetching_reliability = input('*    //boolean// Consider fetching reliability [default=True]: ')
    input_chunk_size_missing_blocks = input('*    //int// Chunk size missing blocks [default=30]: ')
    input_failed_fetch_minimum_seconds_passed = input('*    //int// Failed fetch minimum seconds passed [default=350]: ')
    input_allowed_frozenEdge_sync_discrepancy = input('*    //int// Allowed frozenEdge sync discrepancy [default=5]: ')
    input_url_prepend = input('*    //string// URL prepend [default=http://]: ')
    input_url_append = input('*    //string// URL append [default=/api/]: ')

    try:
        if len(input_ip_address.split('.')) == 4:
            input_ip_address = str(input_ip_address)
        else:
            raise TypeError

        if len(input_consider_missing_blocks) > 0: input_consider_missing_blocks = bool(input_consider_missing_blocks)
        else: input_consider_missing_blocks = True
        if len(input_consider_frozen_edge_discrepancy) > 0: input_consider_frozen_edge_discrepancy = bool(input_consider_frozen_edge_discrepancy)
        else: input_consider_frozen_edge_discrepancy = True
        if len(input_consider_fetching_reliability) > 0: input_consider_fetching_reliability = bool(input_consider_fetching_reliability)
        else: input_consider_fetching_reliability = True
        if len(input_chunk_size_missing_blocks) > 0: input_chunk_size_missing_blocks = int(input_chunk_size_missing_blocks)
        else: input_chunk_size_missing_blocks = 30
        if len(input_failed_fetch_minimum_seconds_passed) > 0: input_failed_fetch_minimum_seconds_passed = int(input_failed_fetch_minimum_seconds_passed)
        else: input_failed_fetch_minimum_seconds_passed = 350
        if len(input_allowed_frozenEdge_sync_discrepancy) > 0: input_allowed_frozenEdge_sync_discrepancy = int(input_allowed_frozenEdge_sync_discrepancy)
        else: input_allowed_frozenEdge_sync_discrepancy = 5

        if len(input_url_prepend) > 0:
            if 'http' in input_url_prepend: input_url_prepend = str(input_url_prepend)
            else: raise TypeError
        else: input_url_prepend = 'http://'

        if len(input_url_append) > 0:
            if '/' in input_url_append: input_url_append = str(input_url_append)
            else: raise TypeError
        else: input_url_append = '/api/'

    except:
        menuHandler_AddNetworkObserver(error_raised=True)

    initialized_NetworkObserver_configurations.addNewNetworkObserver(
        ip_address=input_ip_address,
        save_permanently=True,
        consider_missing_blocks=input_consider_missing_blocks,
        consider_frozen_edge_discrepancy=input_consider_frozen_edge_discrepancy,
        consider_fetching_reliability=input_consider_fetching_reliability,
        chunk_size_missing_blocks=input_chunk_size_missing_blocks,
        failed_fetch_minimum_seconds_passed=input_failed_fetch_minimum_seconds_passed,
        allowed_frozenEdge_sync_discrepancy=input_allowed_frozenEdge_sync_discrepancy,
        url_prepend=input_url_prepend,
        url_append=input_url_append
    )


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
        makePrettyUiLine('[2] - Add Network Observer to disk'),
        makePrettyUiLine('[3] - Update Network Observer from disk'),
        makePrettyUiLine('[4] - Delete Network Observer from disk'),
        makePrettyUiLine('[5] - Start'),
        makePrettyUiLine(''),
        makePrettyUiLine('', enclosing=True)
    )
    print(main_menu)
    mainMenuHandler(error_raised=False)
    logPretty('main menu shown')

def showUiStart(version):
    print("""
********************************************************************************
*                             _ __  _   _ _______                              *
*                            |  _ \| | | |_  / _ \                             *     
*                            | | | | |_| |/ / (_) |                            *
*                            |_| |_|\__  /___\___/                             *
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
    initialized_configurations = Configurations()
    initialized_NetworkObserver_configurations = NetworkObserverConfigurations(amount_of_network_observers_compliant_minimum_percentage=initialized_configurations.amount_of_network_observers_compliant_minimum_percentage)
    if initialized_configurations.showGuiOnStartup:
        showUiStart(initialized_configurations.version)
    else:
        while True:
            initiate_MainLoop()
