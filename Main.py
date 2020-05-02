from Configurations import Configurations, NetworkObserverConfigurations
from helpers import getTimestampSeconds ,clearConsole, printEncloseInput, makePrettyUiLine, colorPrint, logPretty, getDateHuman
import ast
from Mongo import initializeMongo, checkIfTransactionInDatabase, addTransactionToDatabase

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
    showMainMenu()
#

def menuHandler_AddNetworkObserver(error_raised):
    global initialized_NetworkObserver_configurations
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

        if len(input_consider_missing_blocks) > 0: input_consider_missing_blocks = ast.literal_eval(input_consider_missing_blocks)
        else: input_consider_missing_blocks = True
        if len(input_consider_frozen_edge_discrepancy) > 0: input_consider_frozen_edge_discrepancy = ast.literal_eval(input_consider_frozen_edge_discrepancy)
        else: input_consider_frozen_edge_discrepancy = True
        if len(input_consider_fetching_reliability) > 0: input_consider_fetching_reliability = ast.literal_eval(input_consider_fetching_reliability)
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
        consider_missing_blocks=str(input_consider_missing_blocks).capitalize(),
        consider_frozen_edge_discrepancy=str(input_consider_frozen_edge_discrepancy).capitalize(),
        consider_fetching_reliability=str(input_consider_fetching_reliability).capitalize(),
        chunk_size_missing_blocks=input_chunk_size_missing_blocks,
        failed_fetch_minimum_seconds_passed=input_failed_fetch_minimum_seconds_passed,
        allowed_frozenEdge_sync_discrepancy=input_allowed_frozenEdge_sync_discrepancy,
        url_prepend=input_url_prepend,
        url_append=input_url_append
    )

    showMainMenu()


def menuHandler_UpdateNetworkObserver(error_raised=False):
    global initialized_NetworkObserver_configurations
    if error_raised:
        print(makePrettyUiLine('', enclosing=True))
        print(makePrettyUiLine(''))
        print(makePrettyUiLine('A typing error was raised, please try again'))
        print(makePrettyUiLine('To view the main menu, use the "main" command'))
        print(makePrettyUiLine(''))

    print(makePrettyUiLine(''))
    print(makePrettyUiLine('Fill out the following parameters, press [ENTER] to use the current value'))
    print(makePrettyUiLine(''))

    input_observer_identifier = input("*    //int// Observer identifier: ")
    observer_exists = False
    selected_observer = None

    for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
        if int(input_observer_identifier) == NetworkObserver.observer_identifier:
            observer_exists = True
            selected_observer = NetworkObserver

    if not observer_exists:
        logPretty('Observer does not exist on disk or has not been loaded into memory')
        menuHandler_UpdateNetworkObserver(error_raised=True)

    if observer_exists:
        logPretty('Confirmed that observer exists and is loaded into memory')
        input_ip_address = input('*    //string// IP address [{}]: '.format(selected_observer.ip_address))
        input_consider_missing_blocks = input('*    //boolean// Consider missing blocks [{}]: '.format(selected_observer.consider_missing_blocks))
        input_consider_frozen_edge_discrepancy = input('*    //boolean// Consider frozen edge discrepancy [{}]: '.format(selected_observer.consider_frozen_edge_discrepancy))
        input_consider_fetching_reliability = input('*    //boolean// Consider fetching reliability [{}]: '.format(selected_observer.consider_fetching_reliability))
        input_chunk_size_missing_blocks = input('*    //int// Chunk size missing blocks [{}]: '.format(selected_observer.chunk_size_missing_blocks))
        input_failed_fetch_minimum_seconds_passed = input('*    //int// Failed fetch minimum seconds passed [{}]: '.format(selected_observer.failed_fetch_minimum_seconds_passed))
        input_allowed_frozenEdge_sync_discrepancy = input('*    //int// Allowed frozenEdge sync discrepancy [{}]: '.format(selected_observer.allowed_frozenEdge_sync_discrepancy))
        input_url_prepend = input('*    //string// URL prepend [{}]: '.format(selected_observer.url_prepend))
        input_url_append = input('*    //string// URL append [{}]: '.format(selected_observer.url_append))

        try:
            if len(input_ip_address) > 0:
                if len(input_ip_address.split('.')) == 4:
                    input_ip_address = str(input_ip_address)
                else:
                    raise TypeError
            else: input_ip_address = selected_observer.ip_address

            if len(input_consider_missing_blocks) > 0: input_consider_missing_blocks = ast.literal_eval(input_consider_missing_blocks)
            else: input_consider_missing_blocks = selected_observer.consider_missing_blocks
            if len(input_consider_frozen_edge_discrepancy) > 0: input_consider_frozen_edge_discrepancy = ast.literal_eval(input_consider_frozen_edge_discrepancy)
            else: input_consider_frozen_edge_discrepancy = selected_observer.consider_frozen_edge_discrepancy
            if len(input_consider_fetching_reliability) > 0: input_consider_fetching_reliability = ast.literal_eval(input_consider_fetching_reliability)
            else: input_consider_fetching_reliability = selected_observer.consider_fetching_reliability
            if len(input_chunk_size_missing_blocks) > 0: input_chunk_size_missing_blocks = int(input_chunk_size_missing_blocks)
            else: input_chunk_size_missing_blocks = selected_observer.chunk_size_missing_blocks
            if len(input_failed_fetch_minimum_seconds_passed) > 0: input_failed_fetch_minimum_seconds_passed = int(input_failed_fetch_minimum_seconds_passed)
            else: input_failed_fetch_minimum_seconds_passed = selected_observer.failed_fetch_minimum_seconds_passed
            if len(input_allowed_frozenEdge_sync_discrepancy) > 0: input_allowed_frozenEdge_sync_discrepancy = int(input_allowed_frozenEdge_sync_discrepancy)
            else: input_allowed_frozenEdge_sync_discrepancy = selected_observer.allowed_frozenEdge_sync_discrepancy

            if len(input_url_prepend) > 0:
                if 'http' in input_url_prepend: input_url_prepend = str(input_url_prepend)
                else: raise TypeError
            else: input_url_prepend = selected_observer.url_prepend

            if len(input_url_append) > 0:
                if '/' in input_url_append: input_url_append = str(input_url_append)
                else: raise TypeError
            else: input_url_append = selected_observer.url_append

            logPretty('Successfully validated all new parameters for NetworkObserver')

            initialized_NetworkObserver_configurations.updateExistingNetworkObserver(int(selected_observer.observer_identifier),
                {
                    "observer_identifier": selected_observer.observer_identifier,
                    "ip_address": input_ip_address,
                    "consider_missing_blocks": str(input_consider_missing_blocks).capitalize(),
                    "consider_frozen_edge_discrepancy": str(input_consider_frozen_edge_discrepancy).capitalize(),
                    "consider_fetching_reliability": str(input_consider_fetching_reliability).capitalize(),
                    "chunk_size_missing_blocks": input_chunk_size_missing_blocks,
                    "failed_fetch_minimum_seconds_passed": input_failed_fetch_minimum_seconds_passed,
                    "allowed_frozenEdge_sync_discrepancy": input_allowed_frozenEdge_sync_discrepancy,
                    "url_prepend": input_url_prepend,
                    "url_append": input_url_append
                })

        except:
            menuHandler_UpdateNetworkObserver(error_raised=True)


def showMenu_UpdateNetworkObserver():
    menuHandler_UpdateNetworkObserver()
    showMainMenu()

def menuHandler_DeleteNetworkObserver(error_raised=False):
    global initialized_NetworkObserver_configurations
    if error_raised:
        print(makePrettyUiLine('', enclosing=True))
        print(makePrettyUiLine(''))
        print(makePrettyUiLine('A typing error was raised, please try again'))
        print(makePrettyUiLine(''))

    print(makePrettyUiLine(''))
    print(makePrettyUiLine('Fill out the following parameter'))
    print(makePrettyUiLine(''))
    input_observer_identifier = input("*    //int// Observer identifier: ")

    observer_exists = False
    selected_observer = None

    for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
        if int(input_observer_identifier) == NetworkObserver.observer_identifier:
            observer_exists = True
            selected_observer = NetworkObserver

    if not observer_exists:
        logPretty('Observer does not exist on disk or has not been loaded into memory')
        menuHandler_UpdateNetworkObserver(error_raised=True)

    if observer_exists:
        initialized_NetworkObserver_configurations.deleteExistingNetworkObserver(selected_observer.observer_identifier)


def showMenu_DeleteNetworkObserver():
    menuHandler_DeleteNetworkObserver()
    showMainMenu()

def disableMenuOnRun():
    global initialized_configurations
    initialized_configurations.disableMenu()

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
        menuHandler_AddNetworkObserver(error_raised=False)
    elif input_result is '3':
        showMenu_UpdateNetworkObserver()
    elif input_result is '4':
        showMenu_DeleteNetworkObserver()
    elif input_result is '5':
        disableMenuOnRun()
    elif input_result is '6':
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
        makePrettyUiLine('[5] - Disable this menu on run'),
        makePrettyUiLine('[6] - Start'),
        makePrettyUiLine(''),
        makePrettyUiLine('', enclosing=True)
    )
    print(main_menu)
    mainMenuHandler(error_raised=False)
    # logPretty('main menu shown')

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
    global amount_of_loops
    amount_of_loops +=1
    logPretty('Initiating loop {}'.format(str(amount_of_loops)))

    from time import sleep; sleep(7)

    #- used to temporarily store the frozen edge results
    frozenEdge_fetches = []
    #- generate a new run_id and timestamp
    #- query the frozen edge from each individual network observer
    for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
        NetworkObserver.discardPreviousRunTransactions()  # previous run's transactions are discarded to start fresh
        NetworkObserver.assignNewRunId()
        fetch_timestamp = getTimestampSeconds()
        NetworkObserver.fetchFrozenEdge()
        frozenEdge_fetches.append({
            'observer_identifier': NetworkObserver.observer_identifier,
            'ip_address': NetworkObserver.ip_address,
            'last_seen_frozenEdgeHeight': NetworkObserver.last_seen_frozenEdgeHeight,
            'last_failed_frozenEdge_fetch_timestamp_seconds': NetworkObserver.last_failed_frozenEdge_fetch_timestamp_seconds,
            'last_successful_frozenEdge_fetch_timestamp_seconds': NetworkObserver.last_successful_frozenEdge_fetch_timestamp_seconds,
            'failed_fetch_minimum_seconds_passed': NetworkObserver.failed_fetch_minimum_seconds_passed,
            'timestamp_problematic': False,
            'fetch_timestamp': fetch_timestamp,
            'deviation_from_highest_found': None,
            'deviation_problematic': False,
            'consider_frozen_edge_discrepancy': NetworkObserver.consider_frozen_edge_discrepancy,
            'allowed_frozenEdge_sync_discrepancy': NetworkObserver.allowed_frozenEdge_sync_discrepancy,
        })

    #- uses the temporary results to assert highest found frozenEdgeHeight
    highest_frozenEdgeHeight = 0

    for frozenEdge_fetch in frozenEdge_fetches:
        if frozenEdge_fetch['last_seen_frozenEdgeHeight'] > highest_frozenEdgeHeight:
            highest_frozenEdgeHeight = frozenEdge_fetch['last_seen_frozenEdgeHeight']

    #- assert problematic deviation in regards to frozenEdgeHeight
    for frozenEdge_fetch in frozenEdge_fetches:
        if frozenEdge_fetch['consider_frozen_edge_discrepancy']:
            logPretty('Checking if frozenEdgeHeight deviates per the configured allowed_frozenEdge_sync_discrepancy for NetworkObserver {}'.format(frozenEdge_fetch['ip_address']))
            if (highest_frozenEdgeHeight - frozenEdge_fetch['last_seen_frozenEdgeHeight']) > frozenEdge_fetch['allowed_frozenEdge_sync_discrepancy']:
                frozenEdge_fetch['deviation'] = (highest_frozenEdgeHeight - frozenEdge_fetch['last_seen_frozenEdgeHeight'])
                frozenEdge_fetch['deviation_problematic'] = True
                logPretty('frozenEdgeHeight out of boundaries with deviation={} for NetworkObserver {}'.format(frozenEdge_fetch['deviation'], frozenEdge_fetch['ip_address']), color=colorPrint.RED)
            else:
                frozenEdge_fetch['deviation'] = (highest_frozenEdgeHeight - frozenEdge_fetch['last_seen_frozenEdgeHeight'])
                logPretty('frozenEdgeHeight NOT out of boundaries with deviation={} for NetworkObserver {} '.format(frozenEdge_fetch['deviation'], frozenEdge_fetch['ip_address']))
        else:
            logPretty('Disregarding frozenEdgeHeight discrepancy check due to configuration of consider_frozen_edge_discrepancy for NetworkObserver {}'.format(frozenEdge_fetch['ip_address']), color=colorPrint.YELLOW)

    # assert if timestamp is problematic
    for frozenEdge_fetch in frozenEdge_fetches:
        logPretty('Checking if last failed frozenEdge fetch resides far enough in history per the configurations for NetworkObserver {}'.format(frozenEdge_fetch['ip_address']))
        if (frozenEdge_fetch['last_failed_frozenEdge_fetch_timestamp_seconds'] + frozenEdge_fetch['failed_fetch_minimum_seconds_passed']) > frozenEdge_fetch['fetch_timestamp']:
            logPretty('Last failed frozenEdge fetch NOT old enough per the configuration minimum for NetworkObserver {}'.format(frozenEdge_fetch['ip_address'], color=colorPrint.RED))
            frozenEdge_fetch['timestamp_problematic'] = True
        else:
            logPretty('Timestamp compliant for NetworkObserver {}'.format(frozenEdge_fetch['ip_address']))

    # push the first assertions to NetworkObserver
    for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
        for frozenEdge_fetch in frozenEdge_fetches:
            if NetworkObserver.observer_identifier == frozenEdge_fetch['observer_identifier']:
                NetworkObserver.frozenEdge_deviation = frozenEdge_fetch['deviation']
                if frozenEdge_fetch['deviation_problematic']:
                    NetworkObserver.frozenEdge_in_sync = False
                    logPretty('FrozenEdge considered not in sync for NetworkObserver {}'.format(NetworkObserver.ip_address), color=colorPrint.YELLOW)
                else:
                    NetworkObserver.frozenEdge_in_sync = True
                    logPretty('FrozenEdge considered in sync for NetworkObserver {}'.format(NetworkObserver.ip_address))

                if frozenEdge_fetch['timestamp_problematic']:
                    NetworkObserver.frozenEdge_fetching_reliable = False
                    logPretty('FrozenEdge fetching considered unreliable for NetworkObserver {}'.format(NetworkObserver.ip_address), color=colorPrint.YELLOW)
                else:
                    NetworkObserver.frozenEdge_fetching_reliable = True
                    logPretty('FrozenEdge fetching considered reliable for NetworkObserver {}'.format(NetworkObserver.ip_address))

    # temporary list used to store timestamp results of transaction fetches, used to determine problematic fetching behavior
    after_blockFetches = []

    # use these assertions to determine if we want to try and fetch transactions from the nodes
    for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
        if NetworkObserver.frozenEdge_in_sync and NetworkObserver.frozenEdge_fetching_reliable:
            # the heights for transaction fetching are determined according to a network observer's frozenEdgeHeight
            height_start = NetworkObserver.last_seen_frozenEdgeHeight - NetworkObserver.chunk_size_missing_blocks
            height_end = NetworkObserver.last_seen_frozenEdgeHeight
            logPretty('Starting fetching of transactions frozenEdge range({} - {}) - NetworkObserver {}'.format(height_start, height_end, NetworkObserver.ip_address))

            block_heights_fetch_initiated = []
            fetch_timestamp = getTimestampSeconds()
            for blockHeight in range(height_start, height_end+1):
                #logPretty('Fetching transactions for blockHeight {} - NetworkObserver {}'.format(blockHeight, NetworkObserver.ip_address))
                block_heights_fetch_initiated.append(blockHeight)
                NetworkObserver.fetchTransactionsForBlock(blockHeight)

            logPretty('Transaction fetching finished for NetworkObserver {}'.format(NetworkObserver.ip_address))
            after_blockFetches.append({
                'observer_identifier': NetworkObserver.observer_identifier,
                'ip_address': NetworkObserver.ip_address,
                'last_failed_transaction_fetch_timestamp_seconds': NetworkObserver.last_failed_transaction_fetch_timestamp_seconds,
                'last_successful_transaction_fetch_timestamp_seconds': NetworkObserver.last_successful_transaction_fetch_timestamp_seconds,
                'fetch_timestamp': fetch_timestamp,
                'failed_fetch_minimum_seconds_passed': NetworkObserver.failed_fetch_minimum_seconds_passed,
                'block_fetching_reliable': None,
                'missing_blocks_in_chunk': False #
            })

        else:
            logPretty('Skipping transaction fetching for NetworkObserver {}'.format(NetworkObserver.ip_address), color=colorPrint.YELLOW)

    # assert if timestamp is problematic
    for blockFetch in after_blockFetches:
        logPretty('Checking if last failed transaction fetch resides far enough in history per the configurations for NetworkObserver {}'.format(blockFetch['ip_address']))
        if (blockFetch['last_failed_transaction_fetch_timestamp_seconds'] + blockFetch['failed_fetch_minimum_seconds_passed']) > blockFetch['fetch_timestamp']:
            logPretty('Last failed transaction fetch NOT old enough per the configuration minimum for NetworkObserver {}'.format(blockFetch['ip_address'], color=colorPrint.RED))
            blockFetch['block_fetching_reliable'] = False
        else:
            logPretty('Timestamp compliant for NetworkObserver {}'.format(blockFetch['ip_address']))
            blockFetch['block_fetching_reliable'] = True

    # push states to NetworkObserver
    for blockFetch in after_blockFetches:
        for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
            if blockFetch['observer_identifier'] == NetworkObserver.observer_identifier:
                NetworkObserver.block_fetching_reliable = blockFetch['block_fetching_reliable']
                NetworkObserver.missing_blocks_in_chunk = blockFetch['missing_blocks_in_chunk'] # not assigned, could be used in future

    # depending on consider_ configurations, we filter nodes
    compliant_NetworkObserver_identifiers = []
    defiant_NetworkObserver_identifiers = []
    for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
        compliant = True

        if NetworkObserver.consider_missing_blocks:
            if NetworkObserver.missing_blocks_in_chunk:
                compliant = False

        if NetworkObserver.consider_frozen_edge_discrepancy:
            if not NetworkObserver.frozenEdge_in_sync:
                compliant = False

        if NetworkObserver.consider_fetching_reliability:
            if not NetworkObserver.frozenEdge_fetching_reliable:
                compliant = False
            if not NetworkObserver.block_fetching_reliable:
                compliant = False

        if not compliant:
            logPretty('NetworkObserver {} - NOT fully compliant'.format(NetworkObserver.ip_address), color=colorPrint.RED)
            defiant_NetworkObserver_identifiers.append(NetworkObserver.observer_identifier)

        if compliant:
            logPretty('NetworkObserver {} - fully compliant'.format(NetworkObserver.ip_address))
            compliant_NetworkObserver_identifiers.append(NetworkObserver.observer_identifier)

    # percentage comparison fully compliant nodes
    minimum_compliance_percentage = initialized_configurations.amount_of_network_observers_compliant_minimum_percentage
    actual_compliance_percentage = 100/(len(compliant_NetworkObserver_identifiers)+len(defiant_NetworkObserver_identifiers))*len(compliant_NetworkObserver_identifiers)
    tx_insertion_allowed = False

    if actual_compliance_percentage >= minimum_compliance_percentage:
        logPretty('Minimum percentage of compliant network observers ({}%) has been met = {}%'.format(minimum_compliance_percentage, actual_compliance_percentage))
        tx_insertion_allowed = True

    if not tx_insertion_allowed:
        logPretty('No transactions (from both compliant and defiant NetworkObservers) will be added to the database due to the minimum of compliant network observers not being met',color=colorPrint.RED)
        # insert this event too

    # insert the transactions into the database if the minimum amount of compliant network observers is met
    # only insert transactions from compliant nodes
    # transactions are inserted once into a temporary list and handled further down below
    transactionsForDatabase = []
    if tx_insertion_allowed:
        for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
            if NetworkObserver.observer_identifier in compliant_NetworkObserver_identifiers:
                relevant_transactions = NetworkObserver.last_seen_transaction_blocks
                for transaction in relevant_transactions:
                    transactionsForDatabase.append(transaction)
            else:
                logPretty('Transactions will not be processed for defiant NetworkObserver {}'.format(NetworkObserver.ip_address))
    else:
        logPretty('Transactions will not be processed for all NetworkObservers due to the minimum amount of compliant nodes not being met', color=colorPrint.RED)

    # only unique transactions will be added to the database
    logPretty('Amount of transactions before uniqueness filter: {}'.format(len(transactionsForDatabase)))
    transactionsUniqueForDatabase = []
    for transaction in transactionsForDatabase:
        if checkIfTransactionInDatabase(transaction['transactionNyzoString']) is False:
            transactionsUniqueForDatabase.append(transaction)

    #remove duplicates in transactionsUniqueForDatabase
    deduplication_txs = set()
    deduplicated_transactionForDatabase = []
    for tx in transactionsUniqueForDatabase:
        try:
            if tx['transactionNyzoString'] not in deduplication_txs:
                deduplication_txs.add(tx['transactionNyzoString'])
            else:
                raise KeyError
        except Exception as e:
            continue
        deduplicated_transactionForDatabase.append(tx)

    transactionsUniqueForDatabase = deduplicated_transactionForDatabase

    # some variables are fetched from NetworkObservers
    # this is custom data which will be added to the transaction dict below
    current_run_id = ''
    amt_compliant_nodes = len(compliant_NetworkObserver_identifiers)
    amt_defiant_nodes = len(defiant_NetworkObserver_identifiers)

    for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
        current_run_id = NetworkObserver.rolling_run_ids[4][0] # the last one we appended

    # the unique transactions are added to the database, some custom data is added to the transaction dict
    logPretty('Amount of transactions after uniqueness filter: {}'.format(len(transactionsUniqueForDatabase)))

    if initialized_configurations.storeSpecificAddressTransactions:
        logPretty('storeSpecificAddressTransactions is enabled, not all transactions will be saved!',color=colorPrint.YELLOW)

    #

    amount_of_irrelevant_transactions = 0  # this pertains to the storeSpecificAddressTransactions filtration
    highest_frozenEdge_deviation = 0
    blocks_with_deviations = []

    for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
        if NetworkObserver.frozenEdge_deviation > highest_frozenEdge_deviation:
            highest_frozenEdge_deviation = NetworkObserver.frozenEdge_deviation

    final_transactionsForDatabase = []

    for transaction in transactionsUniqueForDatabase:
        # consider data homogeneity in terms of transactions, this uses the amount of compliant nodes
        seen_by_networkobservers = 0
        for NetworkObserver in initialized_NetworkObserver_configurations.loadedNetworkObservers:
            curr_txs = NetworkObserver.last_seen_transaction_blocks
            for tx in curr_txs:
                if tx['transactionNyzoString'] in transaction['transactionNyzoString']:
                    seen_by_networkobservers +=1

        if seen_by_networkobservers < amt_compliant_nodes:
            if transaction['height'] not in blocks_with_deviations:
                blocks_with_deviations.append(transaction['height'])

        ship_to_database = False
        if initialized_configurations.storeSpecificAddressTransactions:
            if transaction['receiverIdentifier'] in initialized_configurations.specificAddressListRaw or transaction['senderIdentifier'] in initialized_configurations.specificAddressListRaw:
                logPretty('receiverIdentifier or senderIdentifier matches an address specified in specificAddressListRaw')
                ship_to_database = True
            else:
                amount_of_irrelevant_transactions += 1
        else:
            ship_to_database = True

        if ship_to_database:
            transaction['run_id'] = current_run_id
            transaction['amt_compliant_nodes'] = amt_compliant_nodes
            transaction['amt_defiant_nodes'] = amt_defiant_nodes
            final_transactionsForDatabase.append(transaction)

    if amount_of_irrelevant_transactions > 0:
        logPretty('Amount of transactions skipped due to storeSpecificAddressTransactions: {}'.format(amount_of_irrelevant_transactions))

    logPretty('Total block deviations from highest frozenEdgeHeight: {}'.format(highest_frozenEdge_deviation))
    logPretty('Total of adjusted blocks with transaction deviations: {}'.format(len(blocks_with_deviations)/2))

    if (len(blocks_with_deviations)/2) > highest_frozenEdge_deviation:
        logPretty('The amount of blocks for which the transaction content differs shouldn\'t exceed {} but {} was found!'.format(highest_frozenEdge_deviation, (len(blocks_with_deviations)/2)), color=colorPrint.RED)

    for tx in final_transactionsForDatabase:
        tx['total_deviations_from_highest_FrozenEdge'] = highest_frozenEdge_deviation
        tx['total_blocks_with_deviations'] = len(blocks_with_deviations)
        tx['adjusted_blocks_with_deviations'] = len(blocks_with_deviations)/2
        tx['transactions_skipped'] = amount_of_irrelevant_transactions
        addTransactionToDatabase(tx)

    # the events for the network observers are added to the database



if __name__ == "__main__":
    amount_of_loops = 0
    initializeMongo()
    initialized_configurations = Configurations()
    initialized_NetworkObserver_configurations = NetworkObserverConfigurations(amount_of_network_observers_compliant_minimum_percentage=initialized_configurations.amount_of_network_observers_compliant_minimum_percentage)
    if initialized_configurations.showGuiOnStartup:
        showUiStart(initialized_configurations.version)
    else:
        logPretty('showGuiOnStartup has been disabled, initiating main loop')
        while True:
            initiate_MainLoop()
