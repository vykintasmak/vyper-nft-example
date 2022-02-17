# Interface for the contract called by safeTransferFrom()
# @dev Note: the ERC-165 identifier for this interface is 0x150b7a02.

# Events

event Received:
    _operator: indexed(address)
    _from: indexed(address)
    _tokenId: uint256
    _data: Bytes[1024]
    _gas: uint256

# Functions

@external
def onERC721Received(_operator: address, _from: address, _tokenId: uint256, _data: Bytes[1024]) -> bytes32:
    pass