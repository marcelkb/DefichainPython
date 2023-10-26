import json
import logging
import traceback

import requests
import time
from defichain.logger import Logger
from defichain.node.RPCErrorHandler import RPCErrorHandler
from defichain.exceptions.http.ServiceUnavailable import ServiceUnavailable
from defichain.exceptions.http.InternalServerError import InternalServerError

RPC_TIMEOUT = 60

class RPC(object):
    def __init__(self, url, logger: Logger):
        self._session = requests.Session()
        self._url = url
        self._headers = {'content-type': 'application/json'}
        self._logger = logger

    def call(self, rpc_method, *params):
        filtered_params = []
        for param in params:
            if param is not None:
                filtered_params.append(param)

        payload = json.dumps({"method": rpc_method, "params": list(filtered_params), "jsonrpc": "2.0"})
        if rpc_method == "walletpassphrase" or rpc_method == "signrawtransactionwithkey":
            logging.debug(json.dumps({"method": rpc_method, "params": '***', "jsonrpc": "2.0"}))
        else:
            logging.debug(payload)
        tries = 3
        hadConnectionFailures = False

        # Logging of Node get request url
        if self._logger:
            if self._logger.log_level == "input" or self._logger.log_level == "all":
                if rpc_method == "walletpassphrase" or rpc_method == "signrawtransactionwithkey":
                    self._logger.input("NodeInput",
                                       f"Node request URL: {self._url} | Headers: {self._headers} | Payload: {json.dumps({'method': rpc_method, 'params': '***', 'jsonrpc': '2.0'})}")
                else:
                    self._logger.input("NodeInput",
                                       f"Node request URL: {self._url} | Headers: {self._headers} | Payload: {payload}")

        while True:
            try:
                response = self._session.post(self._url, headers=self._headers, data=payload, timeout=RPC_TIMEOUT)
            except requests.exceptions.ConnectionError as e:
                tries -= 1
                if tries == 0:
                    raise ServiceUnavailable("The service you are trying to connect to is not available")
                hadConnectionFailures = True
                print(
                    f"Couldn't connect for remote procedure call, will sleep for five seconds and then try again ({tries} more tries)")
                if self._logger:
                    self._logger.error("ConnectionError", f"Could not connect to the Node, trying again")
                logging.debug(traceback.format_exc())
                time.sleep(5)
            except requests.exceptions.ReadTimeout as timeout:
                print(
                    f"Read timeout for remote procedure call, will sleep for five seconds and then try again ({tries} more tries)")
                logging.debug(traceback.format_exc())
                if self._logger:
                    self._logger.error("ConnectionError", f"The connection timed out: {timeout}")
                time.sleep(5)
            except Exception as e2:
                print(f"other exception occurred: {e2}")
                logging.debug(traceback.format_exc())
                raise InternalServerError(e2)
            else:
                if hadConnectionFailures:
                    print('Connected for remote procedure call after retry.')
                #logging.debug("rpc call success")
                break

        RPCErrorHandler(response, self._logger)  # Check for Exceptions

        try:
            result = response.json()['result']
            #logging.debug(f"got result: {result}")
        except Exception as e3:
            raise InternalServerError(f"json error: {e3}")

        # Logging of Ocean get request result
        if self._logger:
            if self._logger.log_level == "output" or self._logger.log_level == "all":
                self._logger.output("NodeOutput", f"Node requests result: {result}")

        return result

    def update_url(self, url: str) -> None:
        self._url = url
