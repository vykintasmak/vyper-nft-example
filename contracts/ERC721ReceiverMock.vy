# @version 0.3.1
# @dev Implementation of ERC-721Receiver for mocking/testing purposes.
# @author Vykintas Maknickas (@vykintasm)

from interfaces import ERC721Receiver

implements: ERC721Receiver

# @dev Emits the retrieval of NFT sent to this contract. This event emits when NFTs are
#      sent to this contract and sender requests for the confirmation of retreival.
# @param _operator The address which called `safeTransferFrom` function
# @param _from The address which previously owned the token.
# @param _tokenId The NFT that got transfered.
# @param _data Data payload sent by the operator.
# @param _gas Number of gas that left after the transaction.

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
    """
    @dev Handle the receipt of an NFT.
         The ERC721 smart contract calls this function on the recipient
         after a `transfer`. This function MAY throw to revert and reject the
         transfer. Return of other than the magic value MUST result in the
         transaction being reverted.
    @param _operator The address which called `safeTransferFrom` function
    @param _from The address which previously owned the token.
    @param _tokenId The NFT that got transfered.
    @param _data Data payload sent by the operator.
    """
    assert self.reverts == False
    log Received(_operator, _from, _tokenId, _data, msg.gas)
    return self.retval
    
