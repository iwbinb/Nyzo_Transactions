# Nyzo_Transactions - wip
 Can be used to confirm incoming transactions to a Nyzo address and aims to be ultra-redundant out of the box.
 
 Consider it your ultra-paranoid blockchain watchdog.
 
 This repository is not production ready. Do not use it, it will not work at this time.

# Goal
What this repository aims to be is Nyzo transaction witnesser.
It aims to provide assurance to an application developer that:
- balance of a given address is accurate
- a transaction has been witnessed by multiple nodes whom are actively tracking the blockchain
- and thus that, a transaction exists and is incorporated into the blockchain

It does not:
- track the network in the first degree
- stand in contact with any of the network's peers, other than
those provided, and preferably in control by the integrator

To be able to use a Nyzo network node for this purpose:
- API endpoints must be live and reachable on port 80
- always_track_blockchain has to be enabled

It is not necessary for a Nyzo network node to:
- be part of the cycle
- store all blocks permanently (the retention edge gap is large enough for regular querying and storage of data by a third-party application such as this one to suffice)

This application facilitates:
- the adding and removing of Network Observers (Nyzo nodes) from which data will be queried
- the configuration of several parameters pertaining to each specific network observer
- the storing of transactions and their sender data in MongoDB, with available filter mechanism as to only store transactions pertaining a particular set of addresses, thus saving on storage
- a historical api pertaining to the network observers and their states
- a historical api pertaining to address specific transaction history

# Loop
This application performs the same set of actions regularly, in chronological order.
The start of the loop pertains to all network observers, as comparing the frozenEdge is necessary
- generate a new run_id and timestamp, pop the oldest run_id+ts from the *rolling_run_ids* list (0), append the newly generated run_id+ts
- query the frozen edge from each individual network observer
- depending on if the query is successful, update either *last_failed_frozenEdge_fetch_timestamp_seconds* or *last_successful_frozenEdge_fetch_timestamp_seconds*
- update the last_seen_frozenEdgeHeight parameter of an observer's class instance if the fetch was successful, otherwise leave the last successful run's frozenEdge enact


- compare the frozen edge of all network observers against each other
- consider the *allowed_frozenEdge_sync_discrepancy* per individual Network Observer to assert whether the observer is to be considered in sync relative to its equal peers
- if a node's frozenedge deviates more than allowed, *frozenEdge_in_sync* = False
- if a node's (*last_failed_frozenEdge_fetch_timestamp* - *last_successful_frozenEdge_fetch_timestamp*) < *failed_fetch_minimum_seconds_passed*,
*frozenEdge_fetching_reliable* is set to False


The next bit of the loop will fetch the blocks from every observer:
- from the observer's class instance, the *last_seen_frozenEdgeHeight* is used in combination with
the *chunk_size_missing_blocks*, to determine for which heights the transactionSearch command from the api
needs to be utilized *(last_seen_frozenEdgeHeight-n)*range(chunk_size_missing_blocks)*
- depending on if ALL the queries for a single network observer are successful, update either *last_failed_transaction_fetch_timestamp_seconds* or *last_successful_transaction_fetch_timestamp_seconds*
- the results are stored in *last_seen_transaction_blocks*
- depending on the results now stored in *last_seen_transaction_blocks*, the *block_fetching_reliable* param is either set to True or False:
it considers the *failed_fetch_minimum_seconds_passed* for comparing *last_failed_transaction_fetch_timestamp_seconds* and *last_successful_transaction_fetch_timestamp_seconds* (similar principle as with frozenedge, but for blocks)
- depending on whether the *last_seen_transaction_blocks* contains (successful fetch communication + block available on node) all blocks, 
the *missing_blocks_in_chunk* param is either set to True or False


The next bit of the loop will make use of 3 configurable parameters:
- if *consider_missing_blocks* is enabled/True, the *missing_blocks_in_chunk* parameter which contains
the result from this loop's previous operations, is taken into regard
- if *consider_frozen_edge_discrepancy* is enabled/True, the *frozenEdge_in_sync* parameter which contains
the result from this loop's previous operations, is taken into regard
- if *consider_fetching_unreliability* is enabled/True, the *frozenEdge_fetching_reliable* and *block_fetching_reliable* parameters which contains
the result from this loop's previous operations, are taken into regard
- the results of these consideration checks are stored in a temporary list
- if the results, after determining whether to take them into consideration or not,
indicate that the node is unreliable, has missing blocks, or is out of sync compared to its peers, all transactions reported
by the node will be disregarded
- in the configurations class, the *amount_of_network_observers_compliant_minimum* parameter is used to check if the total amount of nodes for which
its individual transaction have been disregarded does not exceed (*amount_of_network_observers* - *amount_of_network_observers_compliant_minimum*)
If the minimum amount of nodes, for which transaction data has not been disregarded, is not met, the data from nodes for which
transaction data has not been disregarded, will be disregarded as well
This means that at this point, there are no transactions to process, as there are too little nodes which are working properly according to the demanded minimum
- if the *amount_of_network_observers_compliant_minimum* is however met, the transaction data from the nodes from which transaction data has not been disregarded
will be stored in a temporary list with dicts
- this temporary list will be used to insert the transactions into the mongodb database, this insertion always takes place,
even if all data has been disregarded, this makes any omissions due to data disregarding visible from the transactions api

(note to self: storing the amount of nodes which originally had their data disregarded vs nodes which originally wouldn't have their data disregarded along with the insert is probably a good idea)
- of all nodes, all parameters are inserted as events into the mongodb database

# Beyond the loop
- the api can be used, which in turns grabs results out of the mongodb, this is the primary source for knowing about confirmed transactions
and for extracting historical information about node observer behavior and states

(note to self: node events should be extractable by timestamp buckets ?from_ts= &until_ts=)

(note to self: transactions should be extractable by timestamp buckets ?from_ts= &until_ts=)

(note to self: transactions should be extractable by block buckets ?from_block= &until_block=)

To consider:
- When nodes are producing bad results within their preset parametered limitations and their transaction data is disregarded on a 
continuous basis, there's a likelihood that there will be an extended period where no transaction data is processed by the application. While giving your parameters more leniency may seem like an attractive solution at this point, the problem rests with your nodes and not with the application.









 


