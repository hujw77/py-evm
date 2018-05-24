#!/usr/bin/env python

import logging

from checks import (
    mine_empty_blocks_benchmark
)

from utils.shellart import (
    bold_green
)

HEADER = (
    "\n"
    "______                 _                          _     \n"
    "| ___ \               | |                        | |    \n"
    "| |_/ / ___ _ __   ___| |__  _ __ ___   __ _ _ __| | __ \n"
    "| ___ \/ _ \ '_ \ / __| '_ \| '_ ` _ \ / _` | '__| |/ / \n"
    "| |_/ /  __/ | | | (__| | | | | | | | | (_| | |  |   <  \n"
    "\____/ \___|_| |_|\___|_| |_|_| |_| |_|\__,_|_|  |_|\_\\\n"
)


def run() -> None:

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.info(bold_green(HEADER))

    mine_empty_blocks_benchmark()


if __name__ == '__main__':
    run()
