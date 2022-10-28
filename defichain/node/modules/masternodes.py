from ..util import BuildJson


class Masternodes:
    def __init__(self, node):
        self._node = node

    def createmasternode(self, ownerAddress: str, operatorAddress: str = None, inputs: [{}] = [], timelock: str = None) -> str:  # 01
        """
        Creates (and submits to local node and network) a masternode creation transaction with given owner and operator
        addresses, spending the given inputs..
        The last optional argument (may be empty array) is an array of specific UTXOs to spend.

        :param ownerAddress: (required) Any valid address for keeping collateral amount (any P2PKH or P2WKH address) - used as owner key
        :type ownerAddress: str
        :param operatorAddress: (optional) Optional (== ownerAddress) masternode operator auth address (P2PKH only, unique)
        :type operatorAddress:
        :param inputs: (optional) :ref:`Node Inputs`
        :type inputs: json array
        :param timelock: (optional) Defaults to no timelock period so masternode can be resigned once active. To set a timelock period
            specify either FIVEYEARTIMELOCK or TENYEARTIMELOCK to create a masternode that cannot be resigned for
            five or ten years and will have 1.5x or 2.0 the staking power respectively. Be aware that this means
            that you cannot spend the collateral used to create a masternode for whatever period is specified.
        :type timelock: str
        :return: "hash" (string) -- The hex-encoded hash of broadcasted transaction

        :example:

            >>> node.masternodes.createmasternode("ownerAddress", "operatorAddress")
        """
        operatorAddress = ownerAddress if operatorAddress is None else operatorAddress
        return self._node._rpc.call("createmasternode", ownerAddress, operatorAddress, inputs, timelock)

    def getactivemasternodecount(self, blockCount: int = 20160) -> int:  # 02
        """
        Return number of unique masternodes in the last specified number of blocks

        :param blockCount: (optional) The number of blocks to check for unique masternodes
        :type blockCount: int
        :return: n (numeric) -- Number of unique masternodes seen

        :example:

            >>> node.masternodes.getactivemasternodecount()
        """
        return self._node._rpc.call("getactivemasternodecount", blockCount)

    def getanchorteams(self, blockHeight: int = None) -> {}:  # 03
        """
        Returns the auth and confirm anchor masternode teams at current or specified height

        :param blockHeight: (optional) The height of block which contain tx
        :type blockHeight: int
        :return: {"auth":[Address,...],"confirm":[Address,...]} (json) -- Two sets of masternode operator addresses

        :example:

            >>> node.masternodes.getanchorteams()
        """
        return self._node._rpc.call("getanchorteams", blockHeight)

    def getmasternode(self, mn_id: str) -> {}:  # 04
        """
        Returns information about specified masternode

        :param mn_id: (required)  Masternode's id
        :type mn_id: str
        :return: {id:{...}} (json) -- Json object with masternode information

        :example:

            >>> node.masternodes.getmasternode("095d2bfb5d05ba73fa96502df85aca818ee79810b9ababa71a9dc97e2c360100")
        """
        return self._node._rpc.call("getmasternode", mn_id)

    def getmasternodeblocks(self, id: str = None, ownerAddress: str = None, operatorAddress: str = None, depth: int = None) -> {}:  # 08
        """
        Returns blocks generated by the specified masternode

        Needs one of the three identifier: id, ownerAddress, operatorAddress

        :param id: (optional) Masternode's id
        :type id: str
        :param ownerAddress: (optional) Masternode owner address
        :type ownerAddress: str
        :param operatorAddress: (optional) Masternode operator address
        :type operatorAddress: str
        :param depth: (optional) Maximum depth, from the genesis block is the default
        :type depth: int
        :return: {...} (json) -- Json object with block hash and height information

        :example:

            >>> node.masternodes.getmasternodeblocks(id="095d2bfb5d05ba73fa96502df85aca818ee79810b9ababa71a9dc97e2c360100")
        """
        depth = self._node.blockchain.getblockcount() if depth is None else depth
        identifier = BuildJson()
        identifier.append("id", id)
        identifier.append("ownerAddress", ownerAddress)
        identifier.append("operatorAddress", operatorAddress)
        return self._node._rpc.call("getmasternodeblocks", identifier.build(), depth)

    def listanchors(self) -> []:  # 06
        """
        List anchors (if any)

        :return: [...] (array) -- Returns array of anchors

        :example:

            >>> node.masternodes.listanchors()
        """
        return self._node._rpc.call("listanchors")

    def listmasternodes(self, start: str = None, including_start: bool = None, limit: int = 1000000, verbose: bool = True) -> {}:  # 07
        """
        Returns information about specified masternodes (or all, if list of ids is empty).

        :param start: (optional) Optional first key to iterate from, in lexicographical order. Typically, it's set to last ID from previous request
        :type start: str
        :param including_start: (optional) If true, then iterate including starting position. False by default
        :type including_start: bool
        :param limit: (optional) Maximum number of orders to return, 1000000 by default
        :type limit: int
        :param verbose: (optional) Flag for verbose list (default = true), otherwise only ids are listed
        :type verbose: bool
        :return: {id:{...},...} (json) -- Json object with masternodes information

        :example:

            >>> node.masternodes.listmasternodes()
        """
        pagination = BuildJson()
        pagination.append("start", start)
        pagination.append("including_start", including_start)
        pagination.append("limit", limit)
        return self._node._rpc.call("listmasternodes", pagination.build(), verbose)

    def resignmasternode(self, mn_id: str, inputs: [{}] = None) -> str:  # 08
        """
        Creates (and submits to local node and network) a transaction resigning your masternode.
        Collateral will be unlocked after 2016 blocks.

        The last optional argument (may be empty array) is an array of specific UTXOs to spend. One of UTXO's must
        belong to the MN's owner (collateral) address

        :param mn_id: (required) The Masternode's ID
        :type mn_id: str
        :param inputs: (optional) :ref:`Node Inputs`
        :type inputs: json array
        :return: "hash" (string) -- The hex-encoded hash of broadcasted transaction

        :example:

            >>> node.masternodes.resignmasternode("095d2bfb5d05ba73fa96502df85aca818ee79810b9ababa71a9dc97e2c360100")
        """
        return self._node._rpc.call("resignmasternode", mn_id, inputs)
