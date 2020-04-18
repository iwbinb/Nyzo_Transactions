# Nyzo_Transactions
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



