# -*- coding: utf-8 -*-
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

import json

DEFAULT_CONF = {
    'chainId': 3,
    'url': 'https://ropsten.infura.io/4gmRz0RyQUqgK0Q1jdu5',
    #'privatekey_path': 'keystore/UTC--2018-01-14T18-46-20.321874736Z--da83aee0f49802a331d455f503341a5fdcbde923',
    #'password': 'a',
    'privatekey_path': '',
    'password': '',
    'address': '0xda83aee0f49802a331d455f503341a5fdcbde923',
    'needKey': False,
}

class Web3Wrapper(object):

    def __init__(self, conf = DEFAULT_CONF):
        new_conf = DEFAULT_CONF.copy()
        new_conf.update(conf)

        self.contract = None
        self.chainId = new_conf['chainId']
        self.w3 = Web3(HTTPProvider(new_conf['url']))
        pk_path = new_conf['privatekey_path']
        password = new_conf['password']
        self.w3.eth.defaultAccount = new_conf['address']
        if self.w3.eth.defaultAccount == '':
            self.w3.eth.defaultAccount = self.w3.eth.coinbase
            
        self.needKey = new_conf['needKey']
        if self.needKey and pk_path != '':
            with open(pk_path, "r") as keyfile:
                encrypted_key = keyfile.read()
                self.privateKey = self.w3.eth.account.decrypt(encrypted_key, password)

    def blockNumber(self):
        return self.w3.eth.blockNumber

    def getBlock(self):
        return self.w3.eth.getBlock('latest')

    def signAndSend(self, raw_txn) :

        #print('signAndSend raw_txn:', raw_txn)

        signed_txn = self.w3.eth.account.signTransaction(raw_txn, private_key = self.privateKey)
        tx = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return tx

    def getTxParam(self, **kwargs):

        gas = 3 * 10 ** 6
        gasPrice = Web3.toWei(1, 'gwei')
        account = self.w3.eth.defaultAccount
        value = 0

        if 'account' in kwargs.keys():
            account = kwargs['account']

        nonce = self.w3.eth.getTransactionCount(account)

        if 'nonce' in kwargs.keys():
            nonce = kwargs['nonce']

        if 'gas' in kwargs.keys():
            gas = kwargs['gas']

        if 'gasPrice' in kwargs.keys():
            gasPrice = kwargs['gasPrice']

        if 'value' in kwargs.keys():
            value = kwargs['value']
            
        return { 'nonce' : nonce, 'account' : account, 'gas' : gas, 'gasPrice' : gasPrice, 'value' : value }

    def deployContractLocal(self, bin_content, **kwargs):

        param = self.getTxParam(**kwargs)

        raw_txn = {
            'chainId': self.chainId,
            'nonce': param['nonce'],
            'from': param['account'],
            'to': '',
            'value': param['value'],
            'gas': param['gas'],
            'gasPrice': param['gasPrice'],
            'data': bin_content
            }

        return self.signAndSend(raw_txn)

    def deployContract(self, contract_interface, acc = None, gasPrice = Web3.toWei(1, 'gwei'), gas = 3 * 10 ** 6):
        contract = self.w3.eth.contract(abi = contract_interface['abi'], bytecode = contract_interface['bin'])
        if acc == None:
            acc = self.w3.eth.defaultAccount

        print('balance:', self.w3.eth.getBalance(acc))
        print('acc:', acc, ' gasPrice:', gasPrice)
        tx_hash = contract.deploy(transaction={'from': acc, 'to': '', 'gas': gas, 'gasPrice': gasPrice, 'value': 0})
        return tx_hash

    def initContract(self, crowdsale_addr, _abi):
        self.contract = self.w3.eth.contract(address = crowdsale_addr, abi = _abi)
        self.concise = ConciseContract(self.contract)

    def getCount(self):
        if self.contract != None:
            return self.contract.functions.count().call()
        return -1

    def getTimestamp(self, _datetime) :
        if self.contract != None:
            return self.contract.functions.getTimestamp(_datetime).call()
        return ''

    def getHash(self, _datetime) :
        if self.contract != None:
            return self.contract.functions.getHash(_datetime).call()
        return ''

    def getDateTime(self, count) :
        if self.contract != None:
            return self.contract.functions.getDateTime(count).call()
        return ''

    def putHash(self, _datetime, _hashVal, **kwargs) :
        
        if self.contract != None:

            param = self.getTxParam(**kwargs)

            raw_txn = self.contract.functions.storeHash(_datetime, _hashVal).buildTransaction({
                'chainId': self.chainId,
                'gas': param['gas'],
                'gasPrice': param['gasPrice'],
                'nonce': param['nonce'],
            })

            return self.signAndSend(raw_txn)

        return None

if __name__ == "__main__":

    w3 = Web3Wrapper()

    print(w3.blockNumber())

    print(w3.getBlock())
