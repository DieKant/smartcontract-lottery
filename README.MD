1. per partecipare un utente deve entrare con ether basato su conversione in una quantità fissa di di dollari (50)
2. un admin deciderà quando far finire la lotteria
3. la lotteria avrà solo un vincitore

Tipiologie di test in questo contratto

1. mainnet fork
eliminare quello di base con: brownie networks delete mainnet-fork
ed riaggiungerlo con alchemy (con infura m'ha dato un monte di problemi, questo no)

brownie networks add development mainnet-fork cmd= ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/HeNtmW3wEVVHUWxseRwoevoNa_DXJVeF accounts=10 mnemonic=brownie port=8545





2. testnet rinkeby
3. ganache mocks