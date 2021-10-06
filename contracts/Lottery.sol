// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    // un array di payable addresses che contiene i giocatori della lotteria
    address payable[] public players;
    uint256 public usdEntryFee;
    // variabile dove caricare il contratto dell'orcale chainlink
    AggregatorV3Interface internal ethUsdPriceFeed;
    // definisco gli stati della lotteria, anche se li scrivo a lettere è come se stessi scrivendo stato 0,1,2
    enum LOTTERY_STATE {
        OPEN,
        CLOSE,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        // quando deployo il contratto la lotteria è chiusa
        lottery_state = LOTTERY_STATE.CLOSE;
    }

    // la funzione per entrare nella lotteria
    function enter() public payable {
        // controllo che la lotteria sia aperta
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "La lotteria non è aperta"
        );
        // controllo che il giocatore paghi una somma superiore o uguale a quella richiesta per giocare(TODO)
        require(
            msg.value >= getEntraceFee(),
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
    
    //solo l'autore può far partire o chiudere la lotteria
    function startLottery() public onlyOwner {
        // non avvio la lotteria se non è chiusa in primo luogo
        require(
            lottery_state == LOTTERY_STATE.CLOSE,
            "La lotteria è gia aperta/sta calcolando il vincitore"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        
    }
}
