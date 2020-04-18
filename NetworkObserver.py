class NetworkObserver:
    def __init__(self, ip_address, consider_missing_blocks=True, consider_frozen_edge_discrepancy=True, consider_fetching_unreliability=True,
                 chunk_size_missing_blocks=20, failed_fetch_minimum_seconds_passed=350,
                 allowed_frozenEdge_sync_discrepancy=5,url_prepend='http://', url_append='/api/'):

        self.base_url = url_prepend + ip_address + url_append
        self.chunk_size_missing_blocks = chunk_size_missing_blocks
        self.allowed_frozenEdge_sync_discrepancy = allowed_frozenEdge_sync_discrepancy
        self.failed_fetch_minimum_seconds_passed = failed_fetch_minimum_seconds_passed
        self.rolling_run_ids = [['', 0], ['', 0], ['', 0], ['', 0], ['', 0]]

        self.last_seen_frozenEdgeHeight = 0
        self.last_failed_frozenEdge_fetch_timestamp_seconds = 0
        self.last_successful_frozenEdge_fetch_timestamp_seconds = 0

        self.last_seen_transaction_blocks = {}
        self.last_failed_transaction_fetch_timestamp_seconds = 0
        self.last_successful_transaction_fetch_timestamp_seconds = 0

        self.block_fetching_reliable = False
        self.missing_blocks_in_chunk = True

        self.frozenEdge_fetching_reliable = False
        self.frozenEdge_in_sync = False
