from defichain.networks import DefichainMainnet, DefichainTestnet, DefichainRegtest
from .basedefitx import BaseDefiTx
from ..defitx import DefiTx

from defichain.exceptions.transactions import DefiTxError
from defichain.transactions.address import Address
from defichain.transactions.utils import Converter, Verify, Token
from defichain.transactions.constants import DefiTxType


class Poolswap(BaseDefiTx):
    """
    Builds the defi transaction for a poolswap

    :param addressFrom: (required) the address where the tokens are located
    :param tokenFrom: (required) the token that should be exchanged
    :param amountFrom: (required) the amount that should be exchanged
    :param addressTo: (required) the address where the exchanged tokens are sent to
    :param tokenTo: (required) the token to change into
    :param maxPrice: (required) maximum acceptable price
    :return: "hex" (string) -- returns the finished defi transaction
    """

    @staticmethod
    def deserialize(network: DefichainMainnet or DefichainTestnet or DefichainRegtest, hex: str) -> "Poolswap":
        """TODO: Deserialize Poolswap"""

    def __init__(self, addressFrom: str, tokenFrom: int, amountFrom: int, addressTo: str, tokenTo: int,
                 maxPrice: int):

        self._addressFrom, self._tokenFrom, self._amountFrom, self._addressTo, self._tokenTo, self._maxPrice = None, \
            None, None, None, None, None
        self.set_addressFrom(addressFrom)
        self.set_tokenFrom(tokenFrom)
        self.set_amountFrom(amountFrom)
        self.set_addressTo(addressTo)
        self.set_tokenTo(tokenTo)
        self.set_maxPrice(maxPrice)

    def __bytes__(self) -> bytes:
        # Convert to Bytes
        defiTxType = Converter.hex_to_bytes(DefiTxType.OP_DEFI_TX_POOL_SWAP)
        addressFrom = Converter.hex_to_bytes(Address.from_address(self.get_addressFrom()).get_scriptPublicKey())
        tokenFrom = Converter.int_to_bytes(self.get_tokenFrom(), 1)
        amountFrom = Converter.int_to_bytes(self.get_amountFrom(), 8)
        addressTo = Converter.hex_to_bytes(Address.from_address(self.get_addressTo()).get_scriptPublicKey())
        tokenTo = Converter.int_to_bytes(self.get_tokenTo(), 1)
        maxPrice = Converter.int_to_bytes(self.get_maxPrice(), 8)

        length_addressFrom = Converter.int_to_bytes(len(addressFrom), 1)
        length_addressTo = Converter.int_to_bytes(len(addressTo), 1)
        null = Converter.int_to_bytes(0, 8)

        # Build PoolSwapDefiTx
        result = defiTxType
        result += length_addressFrom
        result += addressFrom
        result += tokenFrom
        result += amountFrom
        result += length_addressTo
        result += addressTo
        result += tokenTo
        result += null
        result += maxPrice

        return DefiTx.build_defiTx(result)

    def __str__(self) -> str:
        result = f"""
                Poolswap
                -------
                Address From: {self.get_addressFrom()}
                Token From: {self.get_tokenFrom()}
                Amount From: {self.get_amountFrom()}
                Address To: {self.get_addressTo()}
                Token To: {self.get_tokenTo()}
                Max Price: {self.get_maxPrice()}

                """
        return result

    def to_json(self) -> {}:
        result = {
            "addressFrom": self.get_addressFrom(),
            "tokenFrom": self.get_tokenFrom(),
            "amountFrom": self.get_amountFrom(),
            "addressTo": self.get_addressTo(),
            "tokenTo": self.get_tokenTo(),
            "maxPrice": self.get_maxPrice()
        }
        return result

    def verify(self) -> bool:
        Address.verify_address(self.get_addressFrom())
        Token.verify_tokenId(self.get_tokenFrom())
        Verify.is_int(self.get_amountFrom())
        Address.verify_address(self.get_addressTo())
        Token.verify_tokenId(self.get_tokenTo())
        Verify.is_int(self.get_maxPrice())
        return True

    # Get information
    def get_defiTxType(self) -> str:
        return DefiTxType.OP_DEFI_TX_POOL_SWAP

    def get_addressFrom(self) -> str:
        return self._addressFrom

    def get_tokenFrom(self) -> int:
        return self._tokenFrom

    def get_amountFrom(self) -> int:
        return self._amountFrom

    def get_addressTo(self) -> str:
        return self._addressTo

    def get_tokenTo(self) -> int:
        return self._tokenTo

    def get_maxPrice(self) -> int:
        return self._maxPrice

    # Set Information

    def set_addressFrom(self, addressFrom: str) -> None:
        self._addressFrom = addressFrom

    def set_tokenFrom(self, tokenFrom: int) -> None:
        self._tokenFrom = tokenFrom

    def set_amountFrom(self, amountFrom: int) -> None:
        self._amountFrom = amountFrom

    def set_addressTo(self, addressTo: str) -> None:
        self._addressTo = addressTo

    def set_tokenTo(self, tokenTo: int) -> None:
        self._tokenTo = tokenTo

    def set_maxPrice(self, maxPrice: int) -> None:
        self._maxPrice = maxPrice


class AddPoolLiquidity(BaseDefiTx):
    """
        Builds the defi transaction for addpoolliquidity

        :param addressAmount: (required) :ref:`Node Address Amount`
        :param shareAddress: (required) the address where the pool shares are placed
        :return: "hex" (string) -- returns the finished defi transaction


        number_of_entries = Converter.int_to_bytes(len(addressAmount), 1)

        result = Converter.hex_to_bytes(DefiTxType.OP_DEFI_TX_POOL_ADD_LIQUIDITY)
        result += number_of_entries

        for address in addressAmount:
            address_script = Converter.hex_to_bytes(Address.from_address(address).get_scriptPublicKey())
            length_of_script = Converter.int_to_bytes(len(address_script), 1)
            result += length_of_script + address_script

            number_of_tokens = Converter.int_to_bytes(len(addressAmount[address]), 1)
            result += number_of_tokens
            for amount in addressAmount[address]:
                split = amount.split('@')
                value = Converter.int_to_bytes(int(split[0]), 8)
                token = Converter.int_to_bytes(int(split[1]), 4)
                result += token + value

        share_address_script = Converter.hex_to_bytes(Address.from_address(shareAddress).get_scriptPublicKey())
        length_of_share_script = Converter.int_to_bytes(len(share_address_script), 1)
        result += length_of_share_script + share_address_script

        return self._defitx.package_defiTx(result)
    """


class RemovePoolLiquidity(BaseDefiTx):
    pass


class CreatePoolPair(BaseDefiTx):
    pass


class UpdatePoolPair(BaseDefiTx):
    pass
