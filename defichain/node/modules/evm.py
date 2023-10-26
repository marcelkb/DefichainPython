from ..util import BuildJson


class Evm:

    def __init__(self, node):
        self._node = node

    def vmmap(self, hash, type):
        """
        Give the equivalent of an address, blockhash or transaction from EVM to DVM\n
        "vmmap", R"('"<hash>"' 1)")
         0 - Auto \n\
                            1 - Block Number: DFI -> EVM (Unsupported yet) \n\
                            2 - Block Number: EVM -> DFI (Unsupported yet) \n\
                            3 - Block Hash: DFI -> EVM \n\
                            4 - Block Hash: EVM -> DFI \n\
                            5 - Tx Hash: DFI -> EVM \n\
                            6 - Tx Hash: EVM -> DFI \n"}},
        :param hash:
        :param type:
        :return:
        """
        return self._node._rpc.call("vmmap", hash, type)

    def logvmmaps(self, type: int) -> {}:
        """
        Logs all block or tx indexes for debugging.
        0 - DVMToEVM Blocks
        1 - EVMToDVM Blocks
        2 - DVMToEVM TXs
        3 - EVMToDVM TXs
        :param type: (required) Type of logs
        :type type: int
        :return: json - (array) Json object with account balances if rpcresult is enabled.This is for debugging purposes only.
        :example:
            >>> node.evm.logvmmaps(0)
        """

        return self._node._rpc.call("logvmmaps", type)


    def evmtx(self, fromAcc, nonce, gasPrice, gasLimit, to, value, data):
        """
              "Creates (and submits to local node and network) a tx to send DFI token to EVM address.\n" +
                        {"from", RPCArg::Type::STR, RPCArg::Optional::NO, "From ERC55 address"},
                          {"nonce", RPCArg::Type::NUM, RPCArg::Optional::NO, "Transaction nonce"},
                          {"gasPrice", RPCArg::Type::NUM, RPCArg::Optional::NO, "Gas Price in Gwei"},
                          {"gasLimit", RPCArg::Type::NUM, RPCArg::Optional::NO, "Gas limit"},
                          {"to", RPCArg::Type::STR, RPCArg::Optional::NO, "To address. Can be empty"},
                          {"value", RPCArg::Type::NUM, RPCArg::Optional::NO, "Amount to send in DFI"},
                          {"data", RPCArg::Type::STR, RPCArg::Optional::OMITTED, "Hex encoded data. Can be blank."},
                          },
        RPCResult{"\"hash\"                  (string) The hex-encoded hash of broadcasted transaction\n"},
        """

        json = BuildJson()
        json.append("from", fromAcc)
        json.append("nonce", nonce)
        json.append("gasPrice", gasPrice)
        json.append("gasLimit", gasLimit)
        json.append("to", to)
        json.append("value", value)
        json.append("data", data)

        return self._node._rpc.call("evmtx", json.build())
