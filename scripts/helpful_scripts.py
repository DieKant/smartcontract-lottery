from brownie import network, accounts, config, MockV3Aggregator, LinkToken, VRFCoordinatorMock, interface

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

# usiamo questa funzione per scegliere tra account per il development
# con l'index posso poi decidere quale account usare usandolo come posizione
#
def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


# mappiamo il tipo di contratto al tipo di mock che ci serve per esso
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator, 
    "vrf_coordinator": VRFCoordinatorMock, 
    "link_token": LinkToken
}


def get_contract(contract_name):
    """questa funzione prende gli indirizzi dei contratti dalla config altrimenti deploya mocks
    args:
        contract_name(string)
    ritorna:
        brownie.network.contract.ProjectContract: alla sua versione più recente
    """
    # prendiamo il tipo di contratto che ci serve
    contract_type = contract_to_mock[contract_name]
    # controlliamo se siamo in dev perche non c'è bisogno di mockare se siamo in fork
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # guardiamo se questo tipo di contratto è gia stato deployato (len conta quante volte è stato deployato)
        if len(contract_type) <= 0:
            deploy_mocks()
        # se è gia su prendo quello più recente dall'array
        contract = contract_type[-1]
    # se non sono in locale vo a prendere quello sulla testnet(in questo caso con forking)
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, 
            contract_address, 
            contract_type.abi
        )
    return contract


DECIMALS = 8
STARTING_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, inital_value=STARTING_VALUE):
    account = get_account()
    # il to.wei aggiunge 18 decimali dopo il numero che gli diamo, also facciamo il deploy del mock solo una volta e prendiamo quello più recente
    MockV3Aggregator.deploy(decimals, inital_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})

""" 
ci serve il contratto a cui mandare il link, 
quale account manda link al contratto (None perche si può scegliere noi), 
quale link token usare (None di base perche possiamo sceglierne 1 specifico), 
quanto link mandare(in questo esempio 0.1 LINK) 
"""
def fund_wiht_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    # questa è magia nera di python, non ho capito come, ma funziona
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # invece di agire direttamente sul contratto possiamo usare un interfaccia
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("contratto caricato con 0,1 link")
    return tx