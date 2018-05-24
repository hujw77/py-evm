import logging

from evm.utils.spoof import (
    SpoofTransaction,
)

from utils.decorator import (
    timecall
)


@timecall(log_level=logging.DEBUG)
def new_transaction(
        vm,
        from_,
        to,
        amount=0,
        private_key=None,
        gas_price=10,
        gas=100000,
        data=b''):
    """
    Create and return a transaction sending amount from <from_> to <to>.

    The transaction will be signed with the given private key.
    """
    nonce = vm.state.account_db.get_nonce(from_)
    tx = vm.create_unsigned_transaction(
        nonce=nonce, gas_price=gas_price, gas=gas, to=to, value=amount, data=data)
    if private_key:
        return tx.as_signed_transaction(private_key)
    else:
        return SpoofTransaction(tx, from_=from_)
