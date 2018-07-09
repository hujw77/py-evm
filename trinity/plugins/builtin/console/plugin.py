from argparse import (
    Action,
    ArgumentParser,
)
import sys

from trinity.config import (
    ChainConfig
)
from trinity.extensibility import (
    BaseEvent,
    BasePlugin,
    PluginContext,
    PluginProcess,
)
from trinity.extensibility.events import (
    NetworkProcessReadyEvent,
    TrinityStartupEvent,
)

from trinity.plugins.builtin.console.console import (
    console
)


class ConsolePlugin(BasePlugin):

    def __init__(self) -> None:
        self.is_attach = False
        self.is_console = False
        self.is_vanilla = False
        self.network_process_ready = False
        self.chain_config: ChainConfig = None

    @property
    def name(self) -> str:
        return "Console"

    @property
    def process(self) -> PluginProcess:
        return PluginProcess.MAIN

    def configure_parser(self, arg_parser: ArgumentParser, sub_parser: Action) -> None:
        console_parser = sub_parser.add_parser(
            'console', help='run the chain and start the trinity REPL')
        console_parser.add_argument(
            '--vanilla-shell',
            action='store_true',
            default=False,
            help='start a native Python shell'
        )

        attach_parser = sub_parser.add_parser(
            'attach',
            help='open an REPL attached to a currently running chain',
        )
        attach_parser.add_argument(
            '--vanilla-shell',
            action='store_true',
            default=False,
            help='start a native Python shell'
        )

    def handle_event(self, event: BaseEvent) -> None:
        if isinstance(event, NetworkProcessReadyEvent):
            self.network_process_ready = True

        if isinstance(event, TrinityStartupEvent):
            self.is_console = event.args.subcommand == 'console'
            self.is_attach = event.args.subcommand == 'attach'
            self.is_vanilla = (hasattr(event.args, "vanilla_shell") and
                               event.args.vanilla_shell)
            self.chain_config = event.chain_config

    def should_start(self):
        return (self.is_console and self.network_process_ready) or self.is_attach

    def start(self, context: PluginContext) -> None:
        self.run_console(self.chain_config, not self.is_vanilla)

        # If we run `attach` the console will block the node from booting and we want
        # to shut it down to not continue booting when the user leaves the console
        if self.is_attach:
            sys.exit(0)

    def run_console(self, chain_config: ChainConfig, use_ipython: bool) -> None:
        try:
            console(chain_config.jsonrpc_ipc_path, use_ipython=use_ipython)
        except FileNotFoundError as err:
            self.logger.error(str(err))
            sys.exit(1)
