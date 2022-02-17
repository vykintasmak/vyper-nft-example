#!/usr/bin/python3
# scripts/deploy.py

from brownie import ERC721_OpenSea, accounts

def main(signed_acc):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.deploy(acc, {'from': acc})
    return erc721_contract
