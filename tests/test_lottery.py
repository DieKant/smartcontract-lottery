# 0.015 -> conversione di 50 usd in eth, data 02/08/2021 
from brownie import Lottery, accounts, network, config
from web3 import Web3

# testo se la comversione che sto facendo nella funzione getEntranceFee è giusta
def test_get_entrace_fee():
    # l'account che uso per pagare il deploy
    account = accounts[0]

    # deployio il contratto
    lottery = Lottery.deploy(
        # seleziono il network sul quale deployare
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    # effettuo il controllo
    assert lottery.getEntraceFee() > Web3.toWei(0.014, "ether")
    assert lottery.getEntraceFee() < Web3.toWei(0.018, "ether")

    # output del 02/08/2021 testando quanto scritto
    """
        ======================================= test session starts =======================================
        platform win32 -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
        rootdir: D:\SolidityProjects\SmartContractLottery
        plugins: eth-brownie-1.16.4, hypothesis-6.21.6, forked-1.3.0, xdist-1.34.0, web3-5.23.1
        collected 1 item

        Launching 'ganache-cli.cmd --accounts 10 --fork https://eth-mainnet.alchemyapi.io/v2/HeNtmW3wEVVHUWxseRwoevoNa_DXJVeF --mnemonic brownie --port 8545 --hardfork istanbul'...

        tests\test_lottery.py .                                                                      [100%]

        ======================================= 1 passed in 11.72s ======================================== 

    """
