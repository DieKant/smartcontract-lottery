# 0.015 -> conversione di 50 usd in eth, data 02/08/2021
from brownie import Lottery, accounts, network, config, exceptions
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_wiht_link,
    get_contract
)
import pytest

# testo se la comversione che sto facendo nella funzione getEntranceFee è giusta
def test_get_entrace_fee():
    # uso questo solo in locale quindi lo skippo con pytest quando sono su testnet
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # imposta
    lottery = deploy_lottery()

    # prendi la roba da controllare
    entrance_fee = lottery.getEntranceFee()
    # deployamo mocks che hanno come valore 2000 usd = 1 eth
    # la entrance fee è di 50 usd quindi 0.025 ether
    # guardiamo se effettivamente è cosi
    expected_entrance_fee = Web3.toWei(0.025, "ether")

    # controlla
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # imposta
    lottery = deploy_lottery()

    # prendi la roba da controllare/controlla
    # settiamo l'exception perche ci aspettiamo un errore se entriamo in una lotteria non avviata
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # imposta
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})

    # prendi la roba da controllare
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})

    # controlla
    # cotrolliamo che dopo che la lotteria è partita
    # il nostro account è riuscito a entrare
    assert lottery.players(0) == account


def test_can_and_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_wiht_link(lottery)
    lottery.endLottery({"from": account})
    # guardo il 2 perche nell'enum lo stato di calcolo del vincitore è 2
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # prendo 2 account diversi per avere più partecipanti
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_wiht_link(lottery)
    # dobbiamo adesso fingerci un nodo chain-link che chiama il vrf cosi che chiama fullfillrandomnes
    # per questo useremo un evento, che sono come dei printf ma fanno anche cose
    transaction = lottery.endLottery({"from": account})
    # ho creato un evento che prende il requestId e lo vado a prendere
    # dopo l'esecuzione dell'endLottery cosi mi fingo un nodo chain-link
    # che manda la requestId al vrf e mi da un numero a caso in cambio
    requestId = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    # mi fingo un chainlink node e mando il requestId, un numero scelto da noi e il contratto al quale mandare il numero random
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 
        STATIC_RNG, 
        lottery.address, 
        {"from": account}
    )
    # 777 % 3 = 0, l'account nell'array players alla posizione 0 sarà il vincitore
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    # controllo che abbia vinto l'account 0
    # che i fondi siano trasferiti
    # che il vincitore abbia ricevuto i fondi
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery