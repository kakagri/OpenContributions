from address_book import AddressBook
from collections import namedtuple
from typing import List
from abis import ABIS
from web3 import Web3

class AaveV3Metrics:
    def __init__(
        self,
        client: Web3
    ):
        self.client = client
        self.pool_data_provider = client.eth.contract(address= AddressBook.ETH_AAVE_V3["POOL_DATA_PROVIDER"], abi = ABIS.ETH_AAVE_V3["POOL_DATA_PROVIDER"])
        self.pool = client.eth.contract(address= AddressBook.ETH_AAVE_V3["POOL"], abi = ABIS.ETH_AAVE_V3["POOL"])

    AllReserveTokensTuple = namedtuple("AllReserveTokensTuple", "token_name token_address")
    def get_all_reserve_tokens(
        self
    ) -> List[AllReserveTokensTuple]:
        """
        Returns: returns the list of all reserve tokens (underlying address)
        """
        res = self.pool_data_provider.functions.getAllReservesTokens().call()
        for i in range(len(res)):
            res[i] = AaveV3Metrics.AllReserveTokensTuple(*res[i])
        return res

    ReserveConfigurationData = namedtuple("ReserveConfigurationData", "decimals ltv liquidation_threshold liquidation_bonus reserve_factor usage_as_collateral_enabled borrowing_enabled stable_borrow_rate_enabled is_active is_frozen")
    def get_reserve_configuration_data(
        self,
        token_address: str,
    ) -> ReserveConfigurationData:
        """
        Parameter: token_address
        Returns: returns the configuration data of the reserve
        """
        token_address = Web3.to_checksum_address(token_address)
        return AaveV3Metrics.ReserveConfigurationData(*self.pool_data_provider.functions.getReserveConfigurationData(token_address).call())

    # Borrow and supply caps are in the underlying token without caring for decimals
    # meaning if cap = 338_000_00 -> that cap is 338M units of that token
    ReserveCaps = namedtuple("ReserveCaps", "borrow_cap supply_cap")
    def get_reserve_caps(
        self,
        token_address: str,
    ) -> ReserveCaps:
        """
        Parameter: token_address
        Returns: returns the borrow and supply caps of the reserve
        """
        token_address = Web3.to_checksum_address(token_address)
        return AaveV3Metrics.ReserveCaps(*self.pool_data_provider.functions.getReserveCaps(token_address).call())

    # TODO: add optionality to get it directly from the pool itself
    ReserveData = namedtuple("ReserveData", "unbacked accrued_to_treasury_scaled total_a_token total_stable_debt total_variable_debt liquidity_rate variable_borrow_rate stable_borrow_rate average_stable_borrow_rate liquidity_index variable_borrow_index last_update_timestamp")
    def get_reserve_data(
        self,
        token_address: str,
    ) -> ReserveData:
        """
        Parameter: token_address
        Returns: returns the reserve data 
        """
        token_address = Web3.to_checksum_address(token_address)
        return AaveV3Metrics.ReserveData(*self.pool_data_provider.functions.getReserveData(token_address).call())

    def get_reserve_emode_category(
        self,
        token_address: str,
    ) -> int:
        """
        Parameter: token_address
        Returns: returns the EMode category of the reserve
        """
        token_address = Web3.to_checksum_address(token_address)
        return self.pool_data_provider.functions.getReserveEModeCategory(token_address).call()


    ReserveTokensAddressesTuple = namedtuple("ReserveTokensAddressesTuple", "a_token_address stable_debt_token_address variable_debt_token_address")
    def get_reserve_tokens_addresses(
        self,
        token_address: str
    ) -> ReserveTokensAddressesTuple:
        '''
        Parameter: token_address
        Returns: returns the addresses of AToken, StableDebtToken and VariableDebtToken
        '''
        token_address = Web3.to_checksum_address(token_address)
        return AaveV3Metrics.ReserveTokensAddressesTuple(*self.pool_data_provider.functions.getReserveTokensAddresses(token_address).call())
    
    def get_siloed_borrowing(
        self,
        token_address: str
    ) -> bool:
        """
        Parameter: token_address
        Returns: returns whether asset is available for siloed borrowing
        """
        token_address = Web3.to_checksum_address(token_address)
        return self.pool_data_provider.functions.getSiloedBorrowing(token_address).call()

    def get_total_debt(
        self,
        token_address: str
    ) -> int:
        """
        Parameter: token_address
        Returns: returns the total debt of the reserve
        """
        token_address = Web3.to_checksum_address(token_address)
        return self.pool_data_provider.functions.getTotalDebt(token_address).call()

    def get_unbacked_mint_cap(
        self,
        token_address: str
    ) -> int:
        """
        Parameter: token_address
        Returns: returns the unbacked mint cap of the reserve
        """
        token_address = Web3.to_checksum_address(token_address)
        return self.pool_data_provider.functions.getUnbackedMintCap(token_address).call()

    UserReserveData = namedtuple("UserReserveData", "current_a_token_balance current_stable_debt current_variable_debt principal_stable_debt scaled_variable_debt stable_borrow_rate liquidity_rate stable_rate_last_updated usage_as_collateral_enabled")
    def get_user_reserve_data(
        self,
        token_address: str,
        user_address: str
    ) -> UserReserveData:
        """
        Parameters: token_address, user_address
        Returns: returns the user data of the reserve
        """
        token_address = Web3.to_checksum_address(token_address)
        user_address = Web3.to_checksum_address(user_address)
        return AaveV3Metrics.UserReserveData(*self.pool_data_provider.functions.getUserReserveData(token_address, user_address).call())

    def get_paused(
        self,
        token_address: str,
    ) -> bool:
        """
        Parameter: token_address
        Returns: returns whether the reserve is paused
        """
        token_address = Web3.to_checksum_address(token_address)
        return self.pool_data_provider.functions.getPaused(token_address).call()
    
    def get_liquidation_protocol_fee(
        self,
        token_address: str
    ) -> int:
        """
        Parameter: token_address
        Returns: returns the liquidation protocol fee
        """
        token_address = Web3.to_checksum_address(token_address)
        return self.pool_data_provider.functions.getLiquidationProtocolFee(token_address).call()

    def get_interest_rate_strategy_address(
        self,
        token_address: str
    ) -> str:
        """
        Parameter: token_address
        Returns: returns the address of the interest rate strategy of the reserve
        """
        token_address = Web3.to_checksum_address(token_address)
        return self.pool_data_provider.functions.getInterestRateStrategyAddress(token_address).call()

    def get_flash_loan_enabled(
        self,
        token_address: str
    ) -> bool:
        """
        Parameter: token_address
        Returns: returns whether flash loans are enabled for the reserve
        """
        token_address = Web3.to_checksum_address(token_address)
        return self.pool_data_provider.functions.getFlashLoanEnabled(token_address).call()

    def get_debt_ceiling(
        self,
        token_address: str
    ) -> int:
        """
        Parameter: token_address
        Returns: returns the debt ceiling of the reserve
        """
        token_address = Web3.to_checksum_address(token_address)
        return self.pool_data_provider.functions.getDebtCeiling(token_address).call()



if __name__ == "__main__":
    client = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/84fe9ded8e9646d2a73529faf5039a0a"))
    aave_v3_metrics = AaveV3Metrics(client)
    print(aave_v3_metrics.get_all_reserve_tokens())
    print(aave_v3_metrics.get_reserve_configuration_data(AddressBook.ETH_DAI))
    print(aave_v3_metrics.get_reserve_caps(AddressBook.ETH_DAI))
    print(aave_v3_metrics.get_reserve_data(AddressBook.ETH_DAI))