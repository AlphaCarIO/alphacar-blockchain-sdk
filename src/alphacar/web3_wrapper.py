# -*- coding: utf-8 -*-
from web3 import Web3, HTTPProvider

import json

DEFAULT_CONF = {
    'chainId': 3,
    'url': 'https://ropsten.infura.io/4gmRz0RyQUqgK0Q1jdu5',
    'db_name': 'alphacar',
    'privatekey_path': 'keystore/UTC--2018-01-14T18-46-20.321874736Z--da83aee0f49802a331d455f503341a5fdcbde923',
    'password': 'a',
    'address': '0xda83aee0f49802a331d455f503341a5fdcbde923',
    'needKey': True,
}

class Web3Wrapper(object):

    def __init__(self, conf = DEFAULT_CONF):
    
        self.chainId = conf['chainId']
        self.w3 = Web3(HTTPProvider(conf['url']))
        pk_path = conf['privatekey_path']
        password = conf['password']
        self.w3.eth.defaultAccount = conf['address']
        if self.w3.eth.defaultAccount == '':
            self.w3.eth.defaultAccount = self.w3.eth.coinbase
            
        self.needKey = conf['needKey']
        if self.needKey and pk_path != '':
            with open(pk_path, "r") as keyfile:
                encrypted_key = keyfile.read()
                self.privateKey = self.w3.eth.account.decrypt(encrypted_key, password)

    def blockNumber(self):
        return self.w3.eth.blockNumber

    def getBlock(self):
        return self.w3.eth.getBlock('latest')

    def signAndSend(self, raw_txn) :
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
            'nonce': param['nonce'],
            'from': param['account'],
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
        tx_hash = contract.deploy(transaction={'from': acc, 'gas': gas, 'gasPrice': gasPrice, 'value': 0})
        return tx_hash

    def storeHash(self, _datetime, _hashVal, contract_addr, abi_content, **kwargs) :

        param = self.getTxParam(**kwargs)
        
        cc = self.w3.eth.contract(address=contract_addr, abi=abi_content)

        raw_txn = cc.functions.storeHash(_datetime, _hashVal).buildTransaction({
            'chainId': self.chainId,
            'gas': param['gas'],
            'gasPrice': param['gasPrice'],
            'nonce': param['nonce'],
        })

        return self.signAndSend(raw_txn)

if __name__ == "__main__":

    w3 = Web3Wrapper()

    print(w3.blockNumber())

    print(w3.getBlock())
