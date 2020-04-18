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
- query the frozen edge from each individual network observer
- depending on if the query is successful, update either *last_failed_frozenEdge_fetch_timestamp_seconds* or *last_successful_frozenEdge_fetch_timestamp_seconds*
- update the last_seen_frozenEdgeHeight parameter of an observer's class instance
- compare the frozen edge of all network observers against each other
- consider the *allowed_frozenEdge_sync_discrepancy* per individual Network Observer to assert whether the observer is to be considered in sync relative to its equal peers
- if a node's frozenedge deviates more than allowed, *frozenEdge_in_sync* = False
- if a node's (*last_failed_frozenEdge_fetch_timestamp* - *last_successful_frozenEdge_fetch_timestamp*) < *failed_fetch_minimum_seconds_passed*,
*node_fetching_reliable* is set to False


The next bit of the loop will fetch the blocks from every observer:
- from the observer's class instance, the *last_seen_frozenEdgeHeight* is used in combination with
the *chunk_size_missing_blocks*, to determine for which heights the transactionSearch command from the api
needs to be utilized *(last_seen_frozenEdgeHeight-n)*range(chunk_size_missing_blocks)*
- depending on if ALL the queries for a single network observer are successful, update either *last_failed_transaction_fetch_timestamp_seconds* or *last_successful_transaction_fetch_timestamp_seconds*
- the results are stored in last_seen_transaction_blocks
- depending on the results now stored in *last_seen_transaction_blocks*, the *block_fetching_reliable* param is either set to True or False:
it considers the *failed_fetch_minimum_seconds_passed* for comparing *last_failed_transaction_fetch_timestamp_seconds* and *last_successful_transaction_fetch_timestamp_seconds* (similar principle as with frozenedge, but for blocks)
- depending on whether the *last_seen_transaction_blocks* contains (successful fetch communication + block available on node) all blocks, 
the *missing_blocks_in_chunk* param is either set to True or False




 


