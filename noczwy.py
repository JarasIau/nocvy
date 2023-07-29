#!/usr/bin/env python3
#NOCZWY
#Copyright (C) 2022  Jaraslau
#Use of this source code is governed by a BSD-style license that can be found in the license file.

import argparse
import urllib3
import threading
import queue

def get_args():
    parser = argparse.ArgumentParser(description="noczwy - enumerate a url and write to standard output", epilog="This software is licensed under the BSD-3-Clause license.")
    parser.add_argument("-u", "--url", type=str, required=True, help="url to enumerate")
    parser.add_argument("-w", "--wordlist", type=str, required=True, help="path to a wordlist")
    parser.add_argument("-t", "--threads", type=int, default=12, help="a number of threads to use")
    parser.add_argument("--head", action="store_true", help="use HEAD method instead of GET")
    return parser.parse_args()

def form_queue(path):
    target_queue = queue.Queue()
    with open(path, "r", encoding = "UTF-8") as wordlist:
        for line in wordlist:
            line = line if line.startswith("/") else f"/{line}"
            target_queue.put(line.strip())
    return target_queue

def enumerate_dirs(connection_pool, method, target_queue, response_queue):
    while True:
        url = target_queue.get()
        response = connection_pool.request(method, url)
        response_queue.put((url, response.status))
        target_queue.task_done()

def main():
    args = get_args()
    args.threads = 1 if args.threads < 1 else args.threads
    method = "HEAD" if args.head else "GET"
    args.url = args.url if not "://" in args.url else args.url.partition("://")[-1]
    target_queue = form_queue(args.wordlist)
    target_queue_size = target_queue.qsize()
    response_queue = queue.Queue()
    connection_pool = urllib3.HTTPConnectionPool(host=args.url, retries=False)

    for i in range(args.threads):
        threading.Thread(target=enumerate_dirs, args=(connection_pool, method, target_queue, response_queue), daemon=True).start()

    for i in range(target_queue_size):
        url, status = response_queue.get()
        print(url, status)
    target_queue.join()

if __name__ == "__main__":
    main()
