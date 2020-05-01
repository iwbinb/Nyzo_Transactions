import pymongo
from helpers import colorPrint, logPretty, getTimestampSeconds

def initializeMongo():
    global mongoClient
    global mongoDatabase
    global mongoCollectionEvents
    global mongoCollectionTransactions
    mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
    mongoDatabase = mongoClient["Nyzo_Transactions"]
    mongoCollectionEvents = mongoDatabase["Events"]
    mongoCollectionTransactions = mongoDatabase["Transactions"]

def checkIfTransactionInDatabase(transactionNyzoString):
    global mongoClient
    global mongoDatabase
    global mongoCollectionTransactions

    res = getTransactionsFromDatabase(transactionNyzoString, filter_type='transactionNyzoString')

    if len(res) > 0:
        return True
    return False

def addTransactionToDatabase(transaction_dict):
    global mongoClient
    global mongoDatabase
    global mongoCollectionTransactions
    try:
        # omitted insertion values = typeValue dict
        logPretty('Adding transaction to database tx_id: {}'.format(transaction_dict['transactionNyzoString']))
        return mongoCollectionTransactions.insert_one({
            'run_id': transaction_dict['run_id'],
            'amt_compliant_nodes': transaction_dict['amt_compliant_nodes'],
            'amt_defiant_nodes': transaction_dict['amt_defiant_nodes'],
            'total_deviations_from_highest_FrozenEdge': transaction_dict['total_deviations_from_highest_FrozenEdge'],
            'total_blocks_with_deviations': transaction_dict['total_blocks_with_deviations'],
            'transactions_skipped': transaction_dict['transactions_skipped'],
            'adjusted_blocks_with_deviations': transaction_dict['adjusted_blocks_with_deviations'],
            'height': transaction_dict['height'],
            'timestampMilliseconds': transaction_dict['timestampMilliseconds'],
            'type': transaction_dict['type'],
            'amount': float(transaction_dict['amount'][1:]),  # the first character returned by the api is n
            'receiverIdentifier': transaction_dict['receiverIdentifier'],
            'senderIdentifier': transaction_dict['senderIdentifier'],
            'previousHashHeight': transaction_dict['previousHashHeight'],
            'senderData': transaction_dict['senderData'],
            'senderDataBytes': transaction_dict['senderDataBytes'],
            'transactionNyzoString': transaction_dict['transactionNyzoString'],
        })
    except KeyError as e:
        logPretty('{} - addTransactionToDatabase failed to get value of transaction dict item'.format(e), color=colorPrint.RED)

def getTransactionsFromDatabase(filter_value, filter_type='blockHeight'):
    global mongoClient
    global mongoDatabase
    global mongoCollectionTransactions
    transaction_list = []

    if filter_type == 'blockHeight':
        query = {'height': filter_value}
    elif filter_type == 'transactionNyzoString':
        query = {'transactionNyzoString': filter_value}
    elif filter_type == 'timestampMilliseconds':  # TODO ideally this should be AROUND a timestamp with leniency
        query = {'timestampMilliseconds': filter_value}
    else:
        logPretty('Invalid filter_type, returning empty list - Mongo.getTransactionFromDatabase', color=colorPrint.RED)
        return []

    res = mongoCollectionTransactions.find(query).sort([('height', -1)])
    for transaction in res:
        transaction_list.append(transaction)

    return transaction_list

def getLastSavedTransactionsFromDatabase(limit):
    global mongoClient
    global mongoDatabase
    global mongoCollectionTransactions
    transaction_list = []

    res = mongoCollectionTransactions.find().sort([('height', -1)]).limit(limit)
    for transaction in res:
        transaction_list.append(transaction)

    return transaction_list

def addEventToDatabase(event_dict):
    global mongoClient
    global mongoDatabase
    global mongoCollectionEvents
    try:
        logPretty('Adding event to database run_id: {}'.format(event_dict['run_id']))
        return mongoCollectionEvents.insert_one({
            'timestamp': getTimestampSeconds(),
            'run_id': event_dict['run_id'],
            'compliant_nodes_ids': event_dict['compliant_nodes_ids'],
            'defiant_nodes_ids': event_dict['defiant_nodes_ids'],
            'amt_transactions_processed': event_dict['amt_transactions_added']
        })
    except KeyError as e:
        logPretty('{} - addEventToDatabase failed to get value of event dict item'.format(e), color=colorPrint.RED)
