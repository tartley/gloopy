#! /usr/bin/env python

from gloopy import init
from gloopy.controller.eventloop import run


def main():
    options = init()
    run(options)


if __name__ == '__main__':
    main()

