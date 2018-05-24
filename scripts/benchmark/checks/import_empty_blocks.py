import logging

from evm.chains.base import Chain

from chain_generator import for_each_vm
from utils.format import format_block
from utils.decorator import timecall
from utils.shellart import (
    bold_white,
    bold_yellow,
    bold_green
)


@timecall(formatter=bold_green)
def import_empty_blocks_benchmark() -> None:
    logging.info(bold_yellow('Starting empty block import benchmark\n'))

    for_each_vm(lambda chain: import_empty_blocks(chain, 100))


@timecall(formatter=bold_white)
def import_empty_blocks(chain: Chain, number_blocks: int) -> None:

    logging.info('Mining {} empty blocks on Chain with {} VM'.format(
        number_blocks,
        bold_white(chain.get_vm().fork)
    ))

    for i in range(1, number_blocks + 1):
        import_block(chain, i)


@timecall(log_level=logging.DEBUG)
def import_block(chain: Chain, num: int) -> None:
    logging.debug('Importing block #{0}'.format(num))

    # TODO: Talk about validation
    block = chain.import_block(chain.get_vm().block, False)
    logging.debug(format_block(block))
