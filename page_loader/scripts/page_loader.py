#!/usr/bin/env python3
from page_loader import page_loader, cli


def main():
    args = cli.get_args().parse_args()
    result = page_loader.download(args.url, args.output)
    print(result)


if __name__ == '__main__':
    main()
