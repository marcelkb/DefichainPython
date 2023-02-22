from defichain.transactions.rawtransactions import TxOutput, define_fee
from defichain.transactions.builder.rawtransactionbuilder import RawTransactionBuilder, Transaction


class UTXO:

    def __init__(self, builder):
        self._builder: RawTransactionBuilder = builder

    def send(self, value: int, addressTo: str, changeAddress: str = "fromAddress", inputs=[]) -> Transaction:
        if changeAddress == "fromAddress":
            changeAddress = self._builder.get_address()

        # If to_address is the same as account address
        if addressTo == self._builder.get_address() or addressTo == changeAddress:
            return self.sendall(addressTo)

        # If to_address is different from account address
        tx = self._builder.build_transactionInputs(inputs)
        input_value = tx.get_inputsValue()
        changeOutputValue = input_value - value
        sendingOutput = TxOutput(value, addressTo)
        changeOutput = TxOutput(changeOutputValue, changeAddress)
        tx.add_output(sendingOutput)
        tx.add_output(changeOutput)

        # Calculate fee
        fee = define_fee(tx, [self._builder.get_account().get_wif()], self._builder.get_feePerByte())

        # Subtract fee from output
        tx.get_outputs()[1].set_value(tx.get_outputs()[1].get_value() - fee)

        self._builder.sign(tx)
        return tx

    def sendall(self, addressTo: str, inputs=[]) -> Transaction:
        tx = self._builder.build_transactionInputs(inputs)
        inputValue = tx.get_inputsValue()
        output = TxOutput(inputValue, addressTo)
        tx.add_output(output)

        # Calculate fee
        fee = define_fee(tx, [self._builder.get_account().get_wif()], self._builder.get_feePerByte())

        # Subtract fee from output
        tx.get_outputs()[0].set_value(tx.get_outputs()[0].get_value() - fee)

        self._builder.sign(tx)
        return tx


