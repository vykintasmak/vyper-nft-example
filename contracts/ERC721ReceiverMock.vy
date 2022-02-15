# @version 0.3.1
# @dev Implementation of ERC-721Receiver mock.

from interfaces import ERC721Receiver

implements: ERC721Receiver


event Received:
    _operator: indexed(address)
    _from: indexed(address)
    _tokenId: uint256
    _data: Bytes[1024]
    _gas: uint256


retval: bytes32
reverts: bool

@external
def __init__(_retval: bytes32, _reverts: bool):
    """
    @dev Contract constructor.
    """
    self.retval = _retval
    self.reverts = _reverts

@external
def onERC721Received(_operator: address, _from: address, _tokenId: uint256, _data: Bytes[1024]) -> bytes32:
    assert self.reverts == False

    someInt: uint256 = 2
    log Received(_operator, _from, _tokenId, _data, msg.gas)

    return self.retval
    
