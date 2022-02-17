#!/usr/bin/python3
# scripts/interact.py

from brownie import ERC721_OpenSea, accounts


### VIEW FUNCTIONS ###

def supportsInterface(contract, signed_acc, interface_id):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    is_supported = erc721_contract.supportsInterface(interface_id, {'from': acc})
    print("Supports interface "+interface_id+": "+str(is_supported))

def balanceOf(contract, signed_acc, owner):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    balance = erc721_contract.balanceOf(owner, {'from': acc})
    print("Balance of "+owner+": "+str(balance))

def ownerOf(contract, signed_acc, token_id):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    owner = erc721_contract.ownerOf(token_id, {'from': acc})
    print("Owner of "+token_id+": "+owner)

def getApproved(contract, signed_acc, token_id):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    approved = erc721_contract.getApproved(token_id, {'from': acc})
    print("Token "+token_id+" is approved for: "+approved)

def isApprovedForAll(contract, signed_acc, owner, operator):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    is_approved = erc721_contract.isApprovedForAll(owner, operator, {'from': acc})
    print("Is "+operator+" approved for all "+owner+" token operations: "+str(is_approved))


### TRANSFER FUNCTIONS ###

def transferFrom(contract, signed_acc, _from, _to, token_id):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    erc721_contract.transferFrom(_from, _to, token_id, {'from': acc})
    print("Transfer complete!")

def safeTransferFrom(contract, signed_acc, _from, _to, token_id, data):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    erc721_contract.safeTransferFrom(_from, _to, token_id, data, {'from': acc})
    print("Safe transfer complete!")

def approve(contract, signed_acc, approved, token_id):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    erc721_contract.approve(approved, token_id, {'from': acc})
    print("Approval is done!")

def setApprovalForAll(contract, signed_acc, operator, approved):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    approved = approved.lower() == 'true'
    erc721_contract.setApprovalForAll(operator, approved, {'from': acc})
    got_approved = "approved" if approved else "disapproved"
    print(operator+" was "+got_approved+" for all "+acc.address+" token operations")


### MINT & BURN FUNCTIONS ###

def mint(contract, signed_acc, _to):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    erc721_contract.mint(_to, {'from': acc})
    print("New token minted to "+_to)

def burn(contract, signed_acc, token_id):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    erc721_contract.burn(token_id, {'from': acc})
    print("Token "+token_id+" burned")

def transferMinter(contract, signed_acc, new_address):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    erc721_contract.transferMinter(new_address, {'from': acc})
    print("New minter set: "+new_address)



### METADATA FUNCTIONS ###

def setBaseURI(contract, signed_acc, uri):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    erc721_contract.setBaseURI(uri, {'from': acc})
    print("New base URI set to "+uri)

def tokenURI(contract, signed_acc, token_id):
    acc = accounts.load(signed_acc)
    erc721_contract = ERC721_OpenSea.at(contract)
    token_uri = erc721_contract.tokenURI(token_id, {'from': acc})
    print("Token URI: "+token_uri)
