from brownie import network
import pytest, time
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_wiht_link
from scripts.deploy_lottery import deploy_lottery

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # aggiungo 1000 per sicurezza e fee a caso se ho voglia
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_wiht_link(lottery)
    lottery.endLottery({"from": account})
    # ora dobbiamo chaimare il chain-link node vero
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
