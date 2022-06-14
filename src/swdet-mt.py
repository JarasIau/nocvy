#!/usr/bin/env python3
#SWDET-MT v0.1 (This code needs better readability and optimization)
#Copyright (C) 2022  Jaraslau
#SWDET-MT is licensed under GPL v3. Details in section License in README.md file.

import argparse
import urllib3
import threading
import queue

def return_args():
    parser = argparse.ArgumentParser(description="Simple Website Directory Enumeration Tool - Multi Threaded.", epilog="Written by @Jaraslau")
    parser.add_argument("-u", "--url", type=str, required=True, help="url to begin bruteforcing process (NO PROTOCOL, e.g. \"url.com\")")
    parser.add_argument("-w", "--wordlist", type=str, required=True, help="point SWDET to a wordlist (Try wl.txt)")
    parser.add_argument("-t", "--threads", type=int, default=12, help="a number of threads to use")
    parser.add_argument("-m", "--head", action="store_true", help="use HEAD method instead of GET")
    return parser.parse_args()

def form_queue(path):
    target_queue = queue.Queue()
    with open(path, "r", encoding = "UTF-8") as file:
        for line in file:
            target_queue.put(f"/{line}".strip()) # This needs better readability and automatic url normalization
    return target_queue

def guess(connection_pool, method, target_queue, response_queue):
    while True:
        url = target_queue.get()
        response = connection_pool.request(method, url)
        response_queue.put((url, response.status))
        target_queue.task_done()

def main():
    args = return_args()
    if args.head:
        method = "HEAD"
    else:
        method = "GET"
    target_queue = form_queue(args.wordlist)
    target_queue_size = target_queue.qsize()
    response_queue = queue.Queue()
    connection_pool = urllib3.HTTPConnectionPool(host=args.url, retries=False)

    for thread_number in range(args.threads):
        threading.Thread(target=guess, args=(connection_pool, method, target_queue, response_queue), daemon=True).start()

    for i in range(target_queue_size):
        url, status = response_queue.get()
        print(url, status)
    target_queue.join()

if __name__ == "__main__":
    main()
