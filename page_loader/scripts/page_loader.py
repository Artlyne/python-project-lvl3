#!/usr/bin/env python3
import requests
import sys
from page_loader import app_logger, page_loader, cli

logger = app_logger.get_logger(__name__)


def main():
    args = cli.get_args().parse_args()
    try:
        result = page_loader.download(args.url, args.output)
        print(result)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        sys.exit(1)
    except OSError as e:
        logger.error(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
