// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    // un array di payable addresses che contiene i giocatori della lotteria
    address payable[] public players;
    uint256 public usdEntryFee;
    // variabile dove caricare il contratto dell'orcale chainlink
    AggregatorV3Interface internal ethUsdPriceFeed;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    // la funzione per entrare nella lotteria
    function enter() public payable {
        // controllo che il giocatore paghi una somma superiore o uguale a quella richiesta per giocare(TODO)
        require(
            1 == 1,
            "paaaaaghhhaaaaa, sgancia, spilla, sborsa, investi, compra, assolda proprio"
        );
        // carico l'address del giocatore nell'array dei giocatori
        players.push(msg.sender);
    }

    //la funzione che determina il valore min di entrata grazie all'oracle chainlink
    function getEntraceFee() public view returns (uint256) {
        // prendo quanto è il valore in dollari di 1 ether
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        // qui non fo * 18 ma *10 perchè dal contratto torna di suo un numero da 8 decimali
        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public {}

    function endLottery() public {}
}
