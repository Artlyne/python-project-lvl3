#!/usr/bin/env python3
import sys
from page_loader import app_logger, page_loader, cli

logger = app_logger.get_logger(__name__)


def main():
    try:
        args = cli.get_args().parse_args()
        result = page_loader.download(args.url, args.output)
        print(result)
    except page_loader.AppInternalError as e:
        print(e)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
