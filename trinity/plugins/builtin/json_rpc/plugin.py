from argparse import (
    ArgumentParser,
    _SubParsersAction,
)
import asyncio

from trinity.extensibility import (
    BaseIsolatedPlugin,
)
from trinity.rpc.main import (
    RPCServer,
)
from trinity.rpc.ipc import (
    IPCServer,
)
from trinity.utils.db_proxy import (
    create_db_manager
)


class JsonRpcServerPlugin(BaseIsolatedPlugin):

    @property
    def name(self) -> str:
        return "JSON-RPC Server"

    def should_start(self) -> bool:
        return not self.context.args.disable_rpc

    def configure_parser(self, arg_parser: ArgumentParser, subparser: _SubParsersAction) -> None:
        arg_parser.add_argument(
            "--disable-rpc",
            action="store_true",
            help="Disables the JSON-RPC Server",
        )

    def start(self) -> None:
        self.logger.info('JSON-RPC Server started')
        loop = asyncio.get_event_loop()
        self.context.event_bus.connect()

        db_manager = create_db_manager(self.context.chain_config.database_ipc_path)
        db_manager.connect()

        chain_class = self.context.chain_config.node_class.chain_class
        db = db_manager.get_db()  # type: ignore
        chain = chain_class(db)

        rpc = RPCServer(chain, self.context.event_bus)
        ipc = IPCServer(rpc, self.context.chain_config.jsonrpc_ipc_path)

        asyncio.ensure_future(ipc.run())
        loop.run_forever()
        loop.close()
