import logging

from evm.chains.base import Chain

from chain_generator import (
    for_each_vm,
    FUNDED_ADDRESS,
    FUNDED_ADDRESS_PRIVATE_KEY
)
from utils.format import format_block
from utils.decorator import timecall
from utils.shellart import (
    bold_white,
    bold_yellow,
    bold_green
)

from utils.tx import new_transaction

TO_ADDRESS = b'\0' * 19 + b'\x02'


@timecall(formatter=bold_green)
def simple_value_transfer_benchmark() -> None:
    logging.info(bold_yellow('Starting simple value transfer benchmark\n'))

    for_each_vm(lambda chain: mine_blocks(chain, 10, 10))


@timecall(formatter=bold_white)
def mine_blocks(chain: Chain, num_blocks: int, num_tx: int) -> None:

    logging.info('Mining {} blocks with {} simple value transfers on Chain with {} VM'.format(
        num_blocks,
        num_tx,
        bold_white(chain.get_vm().fork)
    ))

    for i in range(1, num_blocks + 1):
        mine_block(chain, i, num_tx)


@timecall(log_level=logging.DEBUG)
def mine_block(chain: Chain, block_number: int, num_tx: int) -> None:
    logging.debug('Mining block #{0}'.format(block_number))

    apply_transactions(chain, num_tx)

    block = chain.mine_block()
    logging.debug(format_block(block))


@timecall(log_level=logging.DEBUG)
def apply_transactions(chain: Chain, number_tx: int) -> None:
    for i in range(1, number_tx + 1):
        apply_transaction(chain)


@timecall(log_level=logging.DEBUG)
def apply_transaction(chain: Chain) -> None:
    tx = new_transaction(
        vm=chain.get_vm(),
        private_key=FUNDED_ADDRESS_PRIVATE_KEY,
        from_=FUNDED_ADDRESS,
        to=TO_ADDRESS,
        amount=100,
        data=b''
    )

    logging.debug('Applying Transaction {}'.format(tx))

    block, receipt, computation = chain.apply_transaction(tx)

    logging.debug('Block {}'.format(block))
    logging.debug('Receipt {}'.format(receipt))
    logging.debug('Computation {}'.format(computation))
