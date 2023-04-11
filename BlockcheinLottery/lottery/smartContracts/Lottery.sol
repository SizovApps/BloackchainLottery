// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery {
    address payable[] public players;
    address payable public recentWinner;
    uint256 public gweiEnterFee;
    uint256 public maxPlayers;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    constructor(
        uint256 _gweiEnterFee,
        uint256 _maxPlayers
    ) public {
        gweiEnterFee = _gweiEnterFee;
        maxPlayers = _maxPlayers;
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN, "Not started yet!");
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        require(players.length < maxPlayers, "Too many players");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {
        return gweiEnterFee;
    }

    function getLotteryState() public returns (LOTTERY_STATE) {
        return lottery_state;
    }

    function isParticipating(address playerAddress) public returns (uint256) {
        for (uint i=0; i < players.length; i++) {
            if (keccak256(abi.encodePacked(playerAddress)) == keccak256(abi.encodePacked(players[i]))) {
                return 1;
            }
        }
        return 0;
    }

    function startLottery() public {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery yet"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function getPlayersSize() public returns (uint256) {
        return players.length;
    }

    function getRecentWinner() public returns (address) {
        return recentWinner;
    }

    function endLottery() public {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        uint256 indexOfWinner = uint256(
            keccak256(
                abi.encodePacked(
                    "",
                    msg.sender,
                    block.prevrandao,
                    block.timestamp
                )
            )
        ) % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);

        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

}
