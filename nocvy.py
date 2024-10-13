#!/usr/bin/env python3
#NOCVY
#Copyright (C) 2022  Jaraslau
#Use of this source code is governed by a BSD-style license that can be found in the license file.

import argparse
import urllib3
import threading
import queue

def get_args():
    parser = argparse.ArgumentParser(description="nocvy - enumerate a url and write to standard output", epilog="This software is licensed under the BSD-3-Clause license.")
    parser.add_argument("-u", "--url", type=str, required=True, help="url of which the content will be enumerated")
    parser.add_argument("-w", "--wordlist", type=str, required=True, help="path to a wordlist")
    parser.add_argument("-t", "--threads", type=int, default=12, help="a number of threads to use")
    parser.add_argument("--head", action="store_true", help="use HEAD method instead of GET")
    return parser.parse_args()

def enumerate_content(http, method, target_queue, response_queue):
    while True:
        url = target_queue.get()
        response = http.request(method, url, redirect=False)
        response_queue.put((url, response.status))

def main():
    args = get_args()
    threads = 1 if args.threads < 1 else args.threads
    method = "HEAD" if args.head else "GET"
    url = args.url if args.url.endswith("/") else f"{args.url}/"
    target_queue = queue.Queue()
    with open(args.wordlist, "r", encoding="UTF-8") as wordlist:
        for line in wordlist:
            target_queue.put(f"{url}{line.strip()}")
    expected_responses = target_queue.qsize()
    response_queue = queue.Queue()
    with urllib3.PoolManager() as http:
        for i in range(threads):
            threading.Thread(target=enumerate_content, args=(http, method, target_queue, response_queue), daemon=True).start()
        for i in range(expected_responses):
            url, status = response_queue.get()
            print(url, status)

if __name__ == "__main__":
    main()
