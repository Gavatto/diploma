// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SolarEnergyMonitor {
    struct EnergyData {
        uint256 producedEnergy;
        uint256 consumedEnergy;
        uint256 timestamp;
        string panelId;
    }
    
    mapping(uint256 => EnergyData) public energyRecords;
    uint256 public recordCount = 0;

    event EnergyDataRecorded(
        uint256 recordId,
        uint256 producedEnergy,
        uint256 consumedEnergy,
        uint256 timestamp,
        string panelId
    );

    function recordEnergyData(
        uint256 _producedEnergy,
        uint256 _consumedEnergy,
        uint256 _timestamp,
        string memory _panelId
    ) public {
        energyRecords[recordCount] = EnergyData(
            _producedEnergy,
            _consumedEnergy,
            _timestamp,
            _panelId
        );
        emit EnergyDataRecorded(recordCount, _producedEnergy, _consumedEnergy, _timestamp, _panelId);
        recordCount++;
    }

    function getEnergyData(uint256 _recordId) public view returns (EnergyData memory) {
        return energyRecords[_recordId];
    }
}
