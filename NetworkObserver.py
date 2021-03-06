import requests
import json
from helpers import logPretty, colorPrint

class NetworkObserver:
    def __init__(self, observer_identifier, ip_address, consider_missing_blocks=True, consider_frozen_edge_discrepancy=True, consider_fetching_reliability=True,
                 chunk_size_missing_blocks=20, failed_fetch_minimum_seconds_passed=350,
                 allowed_frozenEdge_sync_discrepancy=5,url_prepend='http://', url_append='/api/'):

        self.observer_identifier = observer_identifier
        self.ip_address = ip_address
        self.consider_missing_blocks = consider_missing_blocks
        self.consider_frozen_edge_discrepancy = consider_frozen_edge_discrepancy
        self.consider_fetching_reliability = consider_fetching_reliability
        self.chunk_size_missing_blocks = chunk_size_missing_blocks
        self.failed_fetch_minimum_seconds_passed = failed_fetch_minimum_seconds_passed
        self.allowed_frozenEdge_sync_discrepancy = allowed_frozenEdge_sync_discrepancy
        self.url_prepend = url_prepend
        self.url_append = url_append
        self.frozenEdge_deviation = 0

        self.base_url = url_prepend + ip_address + url_append
        self.rolling_run_ids = [['', 0], ['', 0], ['', 0], ['', 0], ['', 0]]

        self.last_seen_frozenEdgeHeight = 0
        self.last_failed_frozenEdge_fetch_timestamp_seconds = 0
        self.last_successful_frozenEdge_fetch_timestamp_seconds = 0

        self.last_seen_transaction_blocks = []
        self.last_failed_transaction_fetch_timestamp_seconds = 0
        self.last_successful_transaction_fetch_timestamp_seconds = 0

        self.block_fetching_reliable = False
        self.missing_blocks_in_chunk = True

        self.frozenEdge_fetching_reliable = False
        self.frozenEdge_in_sync = False

    def assignNewRunId(self):
        from helpers import getTimestampSeconds, generateRunId
        self.rolling_run_ids.pop(0)
        self.rolling_run_ids.append([generateRunId(), getTimestampSeconds()])
        logPretty('Generating new run id and timestamp for NetworkObserver {}'.format(self.ip_address))

    def fetchFrozenEdge(self):
        from helpers import getTimestampSeconds
        logPretty('Attempting to fetch frozenEdgeHeight for NetworkObserver {}'.format(self.ip_address))
        temp_res = requests.get(self.base_url+'frozenEdge')
        if temp_res.status_code == 200:
            try:
                logPretty('frozenEdgeHeight fetch successful - NetworkObserver {}'.format(self.ip_address))
                self.last_seen_frozenEdgeHeight = json.loads(temp_res.content.decode('utf-8'))['result'][0]['height']
                self.last_successful_frozenEdge_fetch_timestamp_seconds = getTimestampSeconds()
            except:
                logPretty('Failed to decode JSON from successful frozenEdgeHeight fetch', color=colorPrint.RED)
                self.last_failed_frozenEdge_fetch_timestamp_seconds = getTimestampSeconds()
        else:
            logPretty('Failed to fetch frozenEdgeHeight from NetworkObserver {}'.format(self.ip_address), color=colorPrint.RED)
            self.last_failed_frozenEdge_fetch_timestamp_seconds = getTimestampSeconds()

    def discardPreviousRunTransactions(self):
        self.last_seen_transaction_blocks = []
        self.frozenEdge_deviation = 0

    def fetchTransactionsForBlock(self, block_height):
        from helpers import getTimestampSeconds
        # logPretty('Attempting to fetch transactions for blockHeight {} from NetworkObserver {}'.format(block_height, self.ip_address))
        temp_res = requests.get(self.base_url+'transactionSearch?blockHeight='+str(block_height))
        if temp_res.status_code == 200:
            try:
                # logPretty('transactionSearch fetch successful for blockHeight {} from NetworkObserver {}'.format(block_height, self.ip_address))
                self.last_successful_transaction_fetch_timestamp_seconds = getTimestampSeconds()
                response_decoded = json.loads(temp_res.content.decode('utf-8'))
                if len(response_decoded['errors']) == 0:
                    for transaction in response_decoded['result']:
                        self.last_seen_transaction_blocks.append(transaction)
                else:
                    self.last_seen_transaction_blocks = []
                    raise ValueError
            except Exception as e:
                logPretty('{} - Failed to decode JSON from successful transactionSearch fetch'.format(e), color=colorPrint.RED)
                self.last_failed_transaction_fetch_timestamp_seconds = getTimestampSeconds()
        else:
            logPretty('Failed to fetch transactionSearch from NetworkObserver {}'.format(self.ip_address), color=colorPrint.RED)
            self.last_failed_transaction_fetch_timestamp_seconds = getTimestampSeconds()


