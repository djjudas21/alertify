#!/usr/bin/python3
"""
Main entrypoint to run Alertify
"""

import argparse
import logging
import os
import sys

from src import Alertify

if __name__ == '__main__':

    def parse_cli() -> argparse.ArgumentParser:
        """
        Function to parse the CLI
        """
        maxlen = max([len(key) for key in Alertify.Config.defaults()])
        defaults = [
            f'  * {key.upper().ljust(maxlen)} (default: {val if val != "" else "None"})'
            for key, val in Alertify.Config.defaults().items()
        ]

        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='Bridge between Prometheus Alertmanager and Gotify\n',
            epilog='The following environment variables will override any config or default:\n'
            + '\n'.join(defaults),
        )

        parser.add_argument(
            '-c',
            '--config',
            default=f'{os.path.splitext(__file__)[0]}.yaml',
            help=f'path to config YAML.  (default: {os.path.splitext(__file__)[0]}.yaml)',
        )

        parser.add_argument(
            '-H',
            '--healthcheck',
            action='store_true',
            help='simply exit with 0 for healthy or 1 when unhealthy',
        )

        return parser.parse_args()

    def main() -> int:
        """
        Main program logic
        """
        logging.basicConfig(
            format='%(levelname)s: %(message)s',
            level=logging.INFO,
        )

        args = parse_cli()

        alertify = Alertify.Alertify()
        alertify.configure(args.config)

        # -----------------------------
        # Calculate logging level
        # -----------------------------
        # Config  :: Verbose:   0 = WARNING,  1 = INFO,  2 = DEBUG
        # Logging :: Loglevel: 30 = WARNING, 20 = INFO, 10 = DEBUG
        logger = logging.getLogger()
        logger.setLevel(max(logging.WARNING - (alertify.config.verbose * 10), 10))
        # -----------------------------

        if args.healthcheck:
            _, status = alertify.healthcheck()
            # Invert the sense of 'healthy' for Unix CLI usage
            return not status == 200

        logging.info('Version: %s', Alertify.__version__)

        if alertify.config.verbose:
            logging.debug('Parsed config:')
            for key, val in alertify.config.items():
                logging.debug('%s: %s', key, val)

        alertify.run()

        return 0

    sys.exit(main())
