from scripts.helpful_scripts import get_account, get_contract, fund_wiht_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    # al get_account gli passo il mio indirizzo locale cosi che scelga il deploy su rete testnet oppure un index se volgio usare ganache
    # id="codecamp-training" per mocks
    account = get_account()
    print(account)
    lottery = Lottery.deploy(
        # passo il nome del contratto che voglio usare(prendo solo l'address cosi punto quello invece di scaricami tutto)
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        # se non c'è verify nella conf allora mette false di default
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("deploy completato")
    # faccio il return per usarla nei test, questo non cambia il funzionamento
    return lottery


def start_lottery():
    account = get_account()
    # prendo l'ultimo contratto che ho deployato per eseguirci cose sopra
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    # aspetto l'ultima transazione da parte della funzione precedente
    starting_tx.wait(1)
    print("lotteria partita")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # ne mando un po di più nel caso smongolasse
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("ora sei un partecipante della lotteria")

# in questa funzione ci servirà del link nel contratto perche dobbiamo prendere il numero random dall'oracle che va pagato
def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # mettiamo del link nel contratto
    tx = fund_wiht_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    # metto questo anche col wait perche il nodo chainlink ci mette del tempo a mandare indietro il numero random
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()