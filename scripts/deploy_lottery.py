from scripts.helpful_scripts import get_account, get_contract
from brownie import Lottery, network, config

def deploy_lottery():
    # al get_account gli passo il mio indirizzo locale cosi che scelga il deploy su rete testnet oppure un index se volgio usare ganache
    account = get_account(id="codecamp-training")
    lottery = Lottery.deploy(
        # passo il nome del contratto che voglio usare(prendo solo l'address cosi punto quello invece di scaricami tutto)
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        # se non c'è verify nella conf allora mette false di default
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    print("deploy completato")

def main():
    deploy_lottery()
