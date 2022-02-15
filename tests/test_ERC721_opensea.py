# tests/test_employment.py

import pytest

from brownie import ERC721_OpenSea, ERC721ReceiverMock, accounts, chain, Contract
from brownie.convert import to_bytes

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
RECEIVER_MAGIC_VALUE = '0x150b7a02'
GAS_MAGIC_VALUE = 2000000

@pytest.fixture
def erc721_contract(ERC721_OpenSea, accounts):
    # deploy the contract with the initial value as a constructor argument
    erc721 = ERC721_OpenSea.deploy(accounts[0], {'from': accounts[0]})
    yield erc721

def test_no_minted_tokens(erc721_contract, accounts):
    assert erc721_contract.totalSupply() == 0

def test_some_tokens_minted(erc721_contract, accounts):
    acc1 = accounts[1]
    acc2 = accounts[2]
    acc3 = accounts[3]

    # mint tokens to different accounts
    assert erc721_contract.mint(acc1)

    assert erc721_contract.mint(acc2)
    assert erc721_contract.mint(acc2)

    assert erc721_contract.mint(acc3)
    assert erc721_contract.mint(acc3)
    assert erc721_contract.mint(acc3)

    # verify the supply
    assert erc721_contract.totalSupply() == 6

    # verify balances of accounts
    assert erc721_contract.balanceOf(accounts[0]) == 0
    assert erc721_contract.balanceOf(acc1) == 1
    assert erc721_contract.balanceOf(acc2) == 2
    assert erc721_contract.balanceOf(acc3) == 3

    # verify ownership of tokens
    assert erc721_contract.ownerOf(1) == acc1

    assert erc721_contract.ownerOf(2) == acc2
    assert erc721_contract.ownerOf(3) == acc2

    assert erc721_contract.ownerOf(4) == acc3
    assert erc721_contract.ownerOf(5) == acc3
    assert erc721_contract.ownerOf(6) == acc3

    # verify throwing an error if token doesnt exist
    with pytest.raises(Exception) as e_info:
        assert erc721_contract.ownerOf(7) == acc3

    # verify throwing an error for balanceOf zero address
    with pytest.raises(Exception) as e_info:
        assert erc721_contract.balanceOf(ZERO_ADDRESS) == 0


    # verify approval
    tx = erc721_contract.approve(acc2, 1, {'from': acc1})
    assert erc721_contract.getApproved(1) == acc2

    # verify approval event emitted
    assert tx.events['Approval'][0] == dict(owner=acc1, approved=acc2, tokenId=1)


    # verify throwing an error if trying to approve by non-owner
    with pytest.raises(Exception) as e_info:
        erc721_contract.approve(acc2, 2, {'from': acc1})

    # verify throwing an error if trying to approve by unknown owner
    with pytest.raises(Exception) as e_info:
        erc721_contract.approve(acc2, 1)

    # verify throwing an error if trying to get approvals of non-existing token
    with pytest.raises(Exception) as e_info:
        assert erc721_contract.getApproved(7) == acc3

    # verify if approval for all sets properly
    erc721_contract.setApprovalForAll(acc1, True, {'from': accounts[0]})
    assert erc721_contract.isApprovedForAll(accounts[0], acc1)

    # verify that approval is rejected if sender approves himself
    with pytest.raises(Exception) as e_info:
        erc721_contract.setApprovalForAll(accounts[0], True, {'from': accounts[0]})

def test_succesful_transfers(erc721_contract, accounts):
    sender = accounts[1]
    receiver = ERC721ReceiverMock.deploy(to_bytes(RECEIVER_MAGIC_VALUE, 'bytes32'), False, {'from': accounts[0]})

    erc721_contract.mint(sender)
    erc721_contract.mint(sender)
    erc721_contract.mint(sender)
    erc721_contract.mint(sender)

    # verify if approval for all event emitted 
    tx = erc721_contract.setApprovalForAll(receiver, True, {'from': sender})
    assert tx.events['ApprovalForAll'][0] == dict(owner=sender, operator=receiver, approved=True)

    # verify if recerver can safeTransfer after approval
    tx = erc721_contract.safeTransferFrom(sender, receiver, 1, to_bytes('0xff', 'bytes'), {'from': receiver})
    assert erc721_contract.ownerOf(1) == receiver
    assert tx.events['Transfer'][0] == dict(sender=sender, receiver=receiver, tokenId=1)
    
    # verify if receiver emitted event is correct
    assert tx.events['Received'][0]['_operator'] == receiver
    assert tx.events['Received'][0]['_from'] == sender
    assert tx.events['Received'][0]['_tokenId'] == 1
    assert tx.events['Received'][0]['_data'] == '0xff'

    # verify if sender can safeTransfer after approval
    tx = erc721_contract.safeTransferFrom(sender, receiver, 2, to_bytes('0xff', 'bytes'), {'from': sender})
    assert erc721_contract.ownerOf(2) == receiver
    assert tx.events['Transfer'][0] == dict(sender=sender, receiver=receiver, tokenId=2)

    # verify if receiver emitted event is correct
    assert tx.events['Received'][0]['_operator'] == sender
    assert tx.events['Received'][0]['_from'] == sender
    assert tx.events['Received'][0]['_tokenId'] == 2
    assert tx.events['Received'][0]['_data'] == '0xff'

    # verify if recerver can transfer after approval
    tx = erc721_contract.transferFrom(sender, receiver, 3, {'from': receiver})
    assert erc721_contract.ownerOf(3) == receiver
    assert tx.events['Transfer'][0] == dict(sender=sender, receiver=receiver, tokenId=3)

    # verify if sender can transfer after approval
    tx = erc721_contract.transferFrom(sender, receiver, 4, {'from': sender})
    assert erc721_contract.ownerOf(4) == receiver
    assert tx.events['Transfer'][0] == dict(sender=sender, receiver=receiver, tokenId=4)

    # verify tokens aren't approved anymore
    assert erc721_contract.getApproved(1) == ZERO_ADDRESS
    assert erc721_contract.getApproved(2) == ZERO_ADDRESS

    # verify that balance was adjusted
    assert erc721_contract.balanceOf(sender) == 0

def test_unsuccesful_transfers(erc721_contract, accounts):
    acc1 = accounts[1]
    acc2 = accounts[2]
    acc3 = accounts[3]

    # mint tokens to different accounts
    assert erc721_contract.mint(acc1)
    assert erc721_contract.mint(acc2)

    # verify that sending without the approval reverts
    with pytest.raises(Exception) as e_info:
        tx = erc721_contract.safeTransferFrom(acc1, acc2, 1, to_bytes('0xff', 'bytes'), {'from': acc2})
    with pytest.raises(Exception) as e_info:
        tx = erc721_contract.transferFrom(acc1, acc2, 1, {'from': acc2})

    # verify the rejection of token transfer from incorrect owner
    with pytest.raises(Exception) as e_info:
        tx = erc721_contract.safeTransferFrom(acc2, acc3, 1, to_bytes('0xff', 'bytes'), {'from': acc2})
    with pytest.raises(Exception) as e_info:
        tx = erc721_contract.transferFrom(acc2, acc3, 1, {'from': acc2})

    # verify that sending to zero address reverts
    with pytest.raises(Exception) as e_info:
        tx = erc721_contract.safeTransferFrom(acc1, ZERO_ADDRESS, 1, to_bytes('0xff', 'bytes'), {'from': acc1})
    with pytest.raises(Exception) as e_info:
        tx = erc721_contract.transferFrom(acc1, ZERO_ADDRESS, 1, {'from': acc1})

def test_mint(erc721_contract, accounts):
    owner = accounts[0]
    acc1 = accounts[1]
    acc2 = accounts[2]
    receiver = ERC721ReceiverMock.deploy(to_bytes(RECEIVER_MAGIC_VALUE, 'bytes32'), False, {'from': accounts[3]})

    # verify minting a single token by owner for owner
    tx = erc721_contract.mint(owner, {'from': owner})
    assert erc721_contract.balanceOf(owner) == 1
    assert erc721_contract.ownerOf(1) == owner
    assert tx.events['Transfer'][0] == dict(sender=ZERO_ADDRESS, receiver=owner, tokenId=1)

    # verify minting a single token by owner for account 1
    tx = erc721_contract.mint(acc1, {'from': owner})
    assert erc721_contract.balanceOf(acc1) == 1
    assert erc721_contract.ownerOf(2) == acc1
    assert tx.events['Transfer'][0] == dict(sender=ZERO_ADDRESS, receiver=acc1, tokenId=2)

    # verify minting a single token by owner for receiver contract
    tx = erc721_contract.mint(receiver, {'from': owner})
    assert erc721_contract.balanceOf(receiver) == 1
    assert erc721_contract.ownerOf(3) == receiver
    assert tx.events['Transfer'][0] == dict(sender=ZERO_ADDRESS, receiver=receiver, tokenId=3)

    # verify miniting to zero address reverts
    with pytest.raises(Exception) as e_info:
        erc721_contract.mint(ZERO_ADDRESS, {'from': owner})

    # verify minting by non-owner reverts
    with pytest.raises(Exception) as e_info:
        erc721_contract.mint(acc1, {'from': acc1})

    erc721_contract.transferMinter(acc2, {'from': owner})

    # verify that owner can't mint after minter transfer
    with pytest.raises(Exception) as e_info:
        erc721_contract.mint(acc1, {'from': owner})

    # verify that new minter can mint 
    tx = erc721_contract.mint(acc1, {'from': acc2})
    assert erc721_contract.balanceOf(acc1) == 2
    assert erc721_contract.ownerOf(4) == acc1
    assert tx.events['Transfer'][0] == dict(sender=ZERO_ADDRESS, receiver=acc1, tokenId=4)

def test_burn(erc721_contract, accounts):
    owner = accounts[0]
    acc1 = accounts[1]
    acc2 = accounts[2]

    erc721_contract.mint(owner, {'from': owner})

    erc721_contract.mint(acc1, {'from': owner})
    erc721_contract.mint(acc1, {'from': owner})

    erc721_contract.mint(acc2, {'from': owner})
    erc721_contract.mint(acc2, {'from': owner})
    erc721_contract.mint(acc2, {'from': owner})


    # verify if token owner can burn token
    tx = erc721_contract.burn(3, {'from': acc1})
    
    assert erc721_contract.balanceOf(acc1) == 1
    assert tx.events['Transfer'][0] == dict(sender=acc1, receiver=ZERO_ADDRESS, tokenId=3)
    with pytest.raises(Exception) as e_info:
    	erc721_contract.ownerOf(3)

    # verify if token approved operator can burn token
    erc721_contract.approve(acc2, 2, {'from': acc1})
    tx = erc721_contract.burn(2, {'from': acc2})
    
    assert erc721_contract.balanceOf(acc1) == 0
    assert tx.events['Transfer'][0] == dict(sender=acc1, receiver=ZERO_ADDRESS, tokenId=2) # validate if sender in Transfer event should be previos owner of account who done the transaction
    
    with pytest.raises(Exception) as e_info:
    	erc721_contract.ownerOf(2)

    # verify if reverts when non-owner of token tries to burn token
    with pytest.raises(Exception) as e_info:
    	erc721_contract.burn(4, {'from': acc1})

    # verify if reverts if trying to burn non-existing token
    with pytest.raises(Exception) as e_info:
    	erc721_contract.burn(12, {'from': acc1})

def test_metadata(erc721_contract, accounts):
	owner = accounts[0]
	acc1 = accounts[1]
	new_base = "https://opensea-creatures-api-new.herokuapp.com/api/creature/"

	erc721_contract.mint(owner, {'from': owner})

	# verify if base url changed
	erc721_contract.setBaseURI(new_base, {'from': owner})
	assert erc721_contract.tokenURI(1) == new_base+str(1)

	# verify if reverts when non-minter tries to change base url
	with pytest.raises(Exception) as e_info:
		erc721_contract.setBaseURI(new_base, {'from': acc1})

	# verify if reverts for incorrect tokenId 
	with pytest.raises(Exception) as e_info:
		erc721_contract.tokenURI(2)


















    



