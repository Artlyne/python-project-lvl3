#!/usr/bin/env python3
from page_loader import page_loader


def main():
    args = page_loader.get_args().parse_args()
    result = page_loader.download(args.url, args.output)
    print(result)


if __name__ == '__main__':
    main()
