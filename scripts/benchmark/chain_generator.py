from typing import (
    Any,
    Callable,
    Type
)

from eth_keys import (
    datatypes,
    keys
)

from eth_utils import (
    decode_hex,
    to_canonical_address,
    to_wei,
)

from eth_typing import (
    Address
)

from evm import constants, Chain
from evm.vm.base import BaseVM
from evm.vm.forks import ALL_VM
from evm.db.backends.memory import MemoryDB

FUNDED_ADDRESS_PRIVATE_KEY = keys.PrivateKey(
    decode_hex('0x45a915e4d060149eb4365960e6a7a45f334393093061116b197e3240065ff2d8')
)

FUNDED_ADDRESS_INITIAL_BALANCE = to_wei(1000, 'ether')

GENESIS_PARAMS = {
      'parent_hash': constants.GENESIS_PARENT_HASH,
      'uncles_hash': constants.EMPTY_UNCLE_HASH,
      'coinbase': constants.ZERO_ADDRESS,
      'transaction_root': constants.BLANK_ROOT_HASH,
      'receipt_root': constants.BLANK_ROOT_HASH,
      'difficulty': 1,
      'block_number': constants.GENESIS_BLOCK_NUMBER,
      'gas_limit': constants.GENESIS_GAS_LIMIT,
      'extra_data': constants.GENESIS_EXTRA_DATA,
      'nonce': constants.GENESIS_NONCE
  }


def genesis_state(funded_address: Address, funded_address_initial_balance: int) -> Any:
    return {
        funded_address: {
            "balance": funded_address_initial_balance,
            "nonce": 0,
            "code": b"",
            "storage": {}
        }
    }


def private_key_to_address(privateKey: datatypes.PrivateKey) -> Address:
    return Address(privateKey.public_key.to_canonical_address())


def chain_without_pow(
        base_db: MemoryDB,
        vm: Type[BaseVM],
        genesis_params: Any,
        genesis_state: Any) -> Chain:

    vm_without_pow = vm.configure(validate_seal=lambda self, block: None)

    klass = Chain.configure(
        __name__='TestChain',
        vm_configuration=(
            (constants.GENESIS_BLOCK_NUMBER, vm_without_pow),
        ))
    chain = klass.from_genesis(base_db, genesis_params, genesis_state)
    return chain


def get_chain(vm: Type[BaseVM]) -> Chain:
    return chain_without_pow(
        MemoryDB(),
        vm,
        GENESIS_PARAMS,
        genesis_state(
            private_key_to_address(FUNDED_ADDRESS_PRIVATE_KEY),
            FUNDED_ADDRESS_INITIAL_BALANCE)
    )


def for_each_vm(handler: Callable[[Chain], None]) -> None:
    for vm in ALL_VM:
        chain = get_chain(vm)
        handler(chain)
