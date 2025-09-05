#!/usr/bin/env python3
# NOCVY
# Copyright (C) 2022  Jaraslau
# Use of this source code is governed by a BSD-style license that can be found in the license file.

import argparse
import urllib3
import queue
from concurrent.futures import ThreadPoolExecutor

def get_args():
    parser = argparse.ArgumentParser(
        description="nocvy - enumerate a url and write to standard output",
        epilog="This software is licensed under the BSD-3-Clause license.",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="url of which the content will be enumerated",
    )
    parser.add_argument(
        "-w", "--wordlist", type=str, required=True, help="path to a wordlist"
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=12, help="a number of threads to use"
    )
    parser.add_argument(
        "--head", action="store_true", help="use HEAD method instead of GET"
    )
    return parser.parse_args()

def enumerate_content(http, method, targets):
    while not targets.empty():
        url = targets.get()
        response = http.request(method, url, redirect=False)
        print(url, response.status)

def main(args):
    threads = 1 if args.threads < 1 else args.threads
    method = "HEAD" if args.head else "GET"
    url = args.url if args.url.endswith("/") else f"{args.url}/"
    targets = queue.Queue()
    with open(args.wordlist, "r", encoding="UTF-8") as wordlist:
        for line in wordlist:
            targets.put(f"{url}{line.strip()}")
    with urllib3.PoolManager() as http:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for i in range(threads):
                executor.submit(enumerate_content, http, method, targets)

if __name__ == "__main__":
    args = get_args()
    main(args)
