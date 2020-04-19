from NetworkObserver import NetworkObserver
import json,ast

class Configurations:
    def __init__(self):
        with open('stored_Configurations','r') as f:
            dict_config = ast.literal_eval(f.readline())

        self.showGuiOnStartup = dict_config['showGuiOnStartup']
        self.version = dict_config['version']

class NetworkObserverConfigurations:
    def __init__(self, amount_of_network_observers, amount_of_network_observers_compliant_minimum):
        self.amount_of_network_observers = amount_of_network_observers
        self.amount_of_network_observers_compliant_minimum = amount_of_network_observers_compliant_minimum
        self.loadedNetworkObservers = []
        self.loadStoredNetworkObserversFromDisk()

    def saveNewNetworkObserver(self, configuration_dict):
        with open('stored_NetworkObservers','r') as f: existing = ast.literal_eval(f.readline())
        existing.append(configuration_dict); new = existing
        with open('stored_NetworkObservers', 'w') as f: ast.literal_eval(json.dumps(new))

    def updateExistingNetworkObserver(self, observer_identifier, new_configuration_dict):
        with open('stored_NetworkObservers', 'r') as f: existing = ast.literal_eval(f.readline())
        for i in existing:
            if i['observer_identifier'] == observer_identifier:
                existing.pop(existing.index(i))
        existing.append(new_configuration_dict); new = existing
        with open('stored_NetworkObservers', 'w') as f: f.write(json.dumps(new))
        self.loadStoredNetworkObserversFromDisk()

    def deleteExistingNetworkObserver(self, observer_identifier):
        with open('stored_NetworkObservers', 'r') as f: existing = ast.literal_eval(f.readline())
        for i in existing:
            if i['observer_identifier'] == observer_identifier:
                existing.pop(existing.index(i))
        new = existing
        with open('stored_NetworkObservers', 'w') as f: f.write(json.dumps(new))
        self.loadStoredNetworkObserversFromDisk()

    def addNewNetworkObserver(self, observer_identifier, ip_address, save_permanently=True, consider_missing_blocks=True, consider_frozen_edge_discrepancy=True, consider_fetching_unreliability=True,
                 chunk_size_missing_blocks=20, failed_fetch_minimum_seconds_passed=350,
                 allowed_frozenEdge_sync_discrepancy=5,url_prepend='http://', url_append='/api/'):

        new_observer = NetworkObserver(observer_identifier, ip_address, consider_missing_blocks, consider_frozen_edge_discrepancy, consider_fetching_unreliability, chunk_size_missing_blocks, failed_fetch_minimum_seconds_passed, allowed_frozenEdge_sync_discrepancy, url_prepend, url_append)
        self.loadedNetworkObservers.append(new_observer)
        if save_permanently:
            IdForNetworkObserver = self.getAmountOfStoredNetworkObserversFromDisk() #0-index
            self.saveNewNetworkObserver({
                'observer_identifier': IdForNetworkObserver,
                'ip_address': ip_address,
                'consider_missing_blocks': consider_missing_blocks,
                'consider_frozen_edge_discrepancy': consider_frozen_edge_discrepancy,
                'consider_fetching_unreliability': consider_fetching_unreliability,
                'chunk_size_missing_blocks': chunk_size_missing_blocks,
                'failed_fetch_minimum_seconds_passed': failed_fetch_minimum_seconds_passed,
                'allowed_frozenEdge_sync_discrepancy': allowed_frozenEdge_sync_discrepancy,
                'url_prepend': url_prepend,
                'url_append': url_append
            })

    def loadStoredNetworkObserversFromDisk(self):
        with open('stored_NetworkObservers', 'r') as f:
            dict_list = ast.literal_eval(f.readline())
            for i in dict_list:
                self.addNewNetworkObserver(i['observer_identifier'], i['ip_address'], False, i['consider_missing_blocks'], i['consider_frozen_edge_discrepancy'], i['consider_fetching_reliability'], i['chunk_size_missing_blocks'], i['failed_fetch_minimum_seconds_passed'], i['allowed_frozenEdge_sync_discrepancy'], i['url_prepend'], i['url_append'])

    def getAmountOfStoredNetworkObserversFromDisk(self):
        with open('stored_NetworkObservers', 'r') as f:
            return len(ast.literal_eval(f.readline()))



