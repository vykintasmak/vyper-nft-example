# OpenSea compatible ERC721 (NFT) contract using Vyper
## Safety
This is experimental software that wasn't audited. Use it at your own risk.
## Environment
In order for errors or bugs to be reproducible on any environment, this example uses [Docker](https://docs.docker.com/get-docker/). Please install `docker` and `docker-compose` before the start.

Also if you are looking to deploy your contract to non-local testnet or mainnet, you'll need Infura Project ID. You can find a tutorial of how to obtain one [here](https://blog.infura.io/getting-started-with-infura-28e41844cc89/). Once you have one set it as environment variable:
```Bash
export INFURA_ID=your_infura_id
```
Or add it directly to `docker-compose.yml` file (not recommended).
## Quick Start
### Build
Clone repository, build and launch docker image:
```Bash
git clone https://github.com/vykintasmak/vyper-nft-example
cd vyper-nft-example
docker-compose build
docker-compose up -d
```
### Setup
To prepare contract for deployment you will need to edit contract variables found in `contracts/ERC721_OpenSea.vy`:
```python
self.name = "Another Lootbox"
self.symbol = "LOOTBOX"
self.baseURI = "https://opensea-creatures-api.herokuapp.com/api/creature/"
```
Name will be used as the OpenSea Collection name. URI is for accessing metadata of each individual NFTs.
### Usage
This example uses [brownie](https://github.com/eth-brownie/brownie) for smart contract development and testing. In order to interact with smart contracts we use brownie CLI:
#### Test
In order to run tests:
```Bash
docker-compose exec sandbox bash -c 'brownie test --network development'
```
#### Wallet setup
To deploy to either a test or main network you'll need a wallet and some ether on that network. 
To create new wallet for this specific purpose run:
```Bash
docker-compose exec sandbox bash -c 'brownie accounts generate your-account-id'
```
Please note that `your-account-id` will be needed for each interaction with the contract. You can also load and existing account using a private key using this command:
```Bash
docker-compose exec sandbox bash -c 'brownie accounts new your-account-id'
```
Read more on Brownie account management [here](https://eth-brownie.readthedocs.io/en/stable/account-management.html)

OpenSea uses Rinkeby testnet so we recommend testing your NFTs on this net as well. In order to get some Eth you'll need to request some from public faucets like [this](https://faucet.rinkeby.io/) or [that](https://faucet.paradigm.xyz/).
#### Deploy
Once you have enough Eth you can deploy your contract to testnet using a command:
```Bash
docker-compose exec sandbox bash -c 'brownie run deploy.py your-account-id --network rinkeby'
```
#### Mint
And mint your first NFT:
```Bash
docker-compose exec sandbox bash -c 'brownie run interact.py mint contract-address your-account-id your-account-address --network rinkeby'
```
In the command above `contract-address` should be replaced with the address of deployed contract, `your-account-id` with the ID you created previously and `your-account-address` is the ethereum address that should get the minted NFT.

Once it's done you can open this link: `https://testnets.opensea.io/assets/[contract-address]/1` after replacing `[contract-address]` with your contract address, to view NFT.
### Further interactions
To simplify interaction with the contract each external function is accessible through `interact.py`. In order to trigger some smart contract function run:
```Bash
docker-compose exec sandbox bash -c 'brownie run interact.py [functionName] [contract-address] [your-account-id] [additional-variables] --network rinkeby'
```
Here `functionName` corresponds to the same function name as in the contract, for example `balanceOf`. `contract-address` is the address of previously deployed contract. `your-account-id` is the brownie account you are using to interact with the blockchain. `additional-variables` can be one or more variables that are required for function execution, for example `balanceOf(_owner: address)` requires you to provide the address of the wallet.
### Acknowledgements
The ERC721_OpenSea.vy contract code was originally written by: Ryuya Nakamura (@nrryuya), Thiwakon Mezenen (@ThiwakonPB) and Anutorn Ravisitikiat(BeatMil).
