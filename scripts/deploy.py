#!/usr/bin/python3
# scripts/deploy.py

from brownie import Employment, Factory, accounts

def main():
    acct = accounts.load('testac2')

    employment = Employment.deploy({'from': acct})
    factory = Factory.deploy({'from': acct})

    factory.initializeFactory(employment, {'from': acct})

    return [factory, employment]