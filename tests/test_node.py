import pytest
from config_node import USER, PASSWORD, IP, PORT, WALLET_PATH
from defichain import Node, BuildToJson


def test_createNode():
    assert Node(USER, PASSWORD, IP, PORT)


node = Node(USER, PASSWORD, IP, PORT, wallet_path=WALLET_PATH)


""" Accounts """


@pytest.mark.parametrize("no_rewards, token", [
    (True, "DFI"),
    (False, "TSLA"),
])
@pytest.mark.query
def test_accounthistorycount(no_rewards, token):  # 01
    assert node.accounts.accounthistorycount("df1q26wlgkdxghw8jgs6puqj3t86v84nu48mspgst3", no_rewards=no_rewards,
                                             token=token, txtype="")


@pytest.mark.transaction
def test_accounttoaccount():  # 02
    # The first Address has to have a little of UTXO
    address = node.wallet.listaddressgroupings()
    _from = address[0][0][0]
    to = BuildToJson()
    to.add(_from, "DFI", 0.00000001)
    utxo = address[0][0][1]
    txid = node.accounts.accounttoaccount(_from, to.build(), [])
    assert txid


@pytest.mark.transaction
def test_accounttoutxos():  # 03
    # The first Address has to have a little of DFI Token
    address = node.wallet.listaddressgroupings()
    _from = address[0][0][0]
    to = BuildToJson()
    to.add(_from, "DFI", 0.00001000)
    utxo = address[0][0][1]
    assert node.accounts.accounttoutxos(_from, to.build(), [])


@pytest.mark.developer
def test_executesmartcontract():  # 04
    assert True  # not testable


@pytest.mark.transaction
def test_futureswap():  # 05
    # The first Address has to have a little of PDBC Token
    addresses = node.wallet.listaddressgroupings()
    address = addresses[0][0][0]
    token = "PDBC"
    amount = "0.00000001"
    destination = ""
    txid = node.accounts.futureswap(address=address, token=token, amount=amount, destination=destination, inputs=[])
    assert txid
