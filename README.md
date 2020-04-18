# Nyzo_Transactions - wip
 Can be used to confirm incoming transactions to a Nyzo address

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
- the configuration of several parameters pertaining to the network observer
- the storing of transactions and their sender data in MongoDB, with available filter mechanism as to only store transactions pertaining a particular set of addresses, thus saving on storage
- a historical api pertaining to the network observers and their states
- a historical api pertaining to address specific transaction history
 


