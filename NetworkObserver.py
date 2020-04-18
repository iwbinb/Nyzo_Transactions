
class NetworkObserver:
    def __init__(self, ip_address, consider_missing_blocks=True, consider_frozen_edge_discrepancy=True, consider_fetching_unreliability=True,
                 chunk_size_missing_blocks=20, failed_fetch_minimum_seconds_passed=350,
                 allowed_frozenEdge_sync_discrepancy=5,url_prepend='http://', url_append='/api/'):
        """
        In the documentation below, several mentions are made to processes which do not exist yet at the time of creating this
        class, to indicate where these non-existant processes come in, the relevant text has been surrounded by << >>

        :param 1 ip_address: the ip address of the node fetching information from the network
        :param 2 url_prepend: the prepend of the ip address through which requests can make a request
        :param 3 url_append: the append of the ip address, this is where the API endpoint is running

        :param 4 chunk_size_missing_blocks: this is a configurable chunk size, if a block is missing from the
                                          last [x=default=20], all data from this observer <<will be considered
                                          useless>> until the missing block is no longer part of the last x
        :param 5 failed_fetch_minimum_seconds_passed : a configurable seconds counter, <<if last_failed_fetch_timestamp_seconds
                                                       + failed_fetch_minimum_seconds_passed is bigger than the
                                                       last_successful_fetch_timestamp_seconds>>
                                                       the observer <<will be considered useless>> until this has resolved
        :param 6 allowed_frozenEdge_sync_discrepancy: all network observers have a frozenEdge, this allows the observer
                                                      to deviate, by default, 5 blocks from the highest frozenEdge observed,
                                                      and should be the leniency used <<when considering to update>>
                                                      missing_blocks_in_chunk and chunk_size_missing_blocks

        :returns 1 base_url: a concoction of param[1,2,3], this is never updated
        :returns 3 chunk_size_missing_blocks: sets the parameter, explanation above, this is never updated
        :returns 5 failed_fetch_minimum_seconds_passed: set at 350 by default, this is never updated

        :returns 2 last_seen_frozenEdge: set at 0 by default, <<this is populated every [] by the [] function>>
        :returns 4 last_failed_fetch_timestamp_seconds: set at 0 by default, <<every contact with the observer
                                                      updates this value>>
        :returns 6 missing_blocks_in_chunk: by default True, we haven't fetched anything yet during initialization,
                                            <<this is updated by the functions: []>>
        :returns 7 network_observer_live: by default False, we haven't fetched anything yet during initialization
                                        <<this should be auto-updated **BEFORE** an action>>, according to returns[3,4,5,6]
        """
        self.base_url = url_prepend + ip_address + url_append
        self.chunk_size_missing_blocks = chunk_size_missing_blocks
        self.allowed_frozenEdge_sync_discrepancy = allowed_frozenEdge_sync_discrepancy
        self.failed_fetch_minimum_seconds_passed = failed_fetch_minimum_seconds_passed

        self.last_seen_frozenEdgeHeight = 0
        self.last_failed_frozenEdge_fetch_timestamp_seconds = 0
        self.last_successful_frozenEdge_fetch_timestamp_seconds = 0

        self.last_seen_transaction_blocks = {}
        self.last_failed_transaction_fetch_timestamp_seconds = 0
        self.last_successful_transaction_fetch_timestamp_seconds = 0

        self.network_observer_live = False # meh

        self.block_fetching_reliable = False
        self.missing_blocks_in_chunk = True

        self.node_fetching_reliable = False
        self.frozenEdge_in_sync = False
