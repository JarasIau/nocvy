#!/usr/bin/env python3
#SWDET-MT v0.21 (This code needs better readability and optimization)
#Copyright (C) 2022  Jaraslau
#SWDET-MT is licensed under GPL v3. Details in section License in README.md file.

import argparse
import urllib3
import threading
import queue

class FileERR(Exception):
    '''Custom exception to be raised in form_queue()'''

def return_args():
    parser = argparse.ArgumentParser(description="Simple Website Directory Enumeration Tool - Multi Threaded.", epilog="Written by @Jaraslau")
    parser.add_argument("-u", "--url", type=str, required=True, help="url to begin bruteforcing process (NO PROTOCOL, e.g. \"url.com\")")
    parser.add_argument("-w", "--wordlist", type=str, required=True, help="point SWDET to a wordlist (Try wl.txt)")
    parser.add_argument("-t", "--threads", type=int, default=12, help="a number of threads to use")
    parser.add_argument("-m", "--head", action="store_true", help="use HEAD method instead of GET")
    return parser.parse_args()

def form_queue(path):
    target_queue = queue.Queue()
    try:
        with open(path, "r", encoding = "UTF-8") as raw_wordlist:
            for line in raw_wordlist:
                target_queue.put(f"/{line}".strip()) # This needs better readability and automatic url normalization
        return target_queue
    except FileNotFoundError:
        raise FileERR("No such file or directory. Try checking whether you gave the right path.") # I didn't want to print in a function so bad
    except PermissionError:
        raise FileERR("Insuficient permissions to manipulate the file. Try running as root.")
    except IsADirectoryError:
        raise FileERR("Given path leads to a directory. The path is supposed to lead to a file.")

def enumerate_dirs(connection_pool, method, target_queue, response_queue):
    while True:
        url = target_queue.get()
        try:
            response = connection_pool.request(method, url)
            status = response.status
        except urllib3.exceptions.NewConnectionError:
            status = ": Failed to establish a connection. Check your url format or internet connection."
        except urllib3.exceptions.ProtocolError:
            status = ": Protocol error. Try removing a protocol from your url."
        except urllib3.exceptions.TimeoutError:
            status = ": Timeout occured."
        except urllib3.exceptions.ConnectTimeoutError:
            status = ": Connection Timeout occured."
        finally:
            response_queue.put((url, status))
            target_queue.task_done()

def main():
    args = return_args()
    if args.threads < 1:
        raise ValueError("Number of threads can't be less than 1!")
    method = "HEAD" if args.head else "GET"
    target_queue = form_queue(args.wordlist)
    target_queue_size = target_queue.qsize()
    response_queue = queue.Queue()
    connection_pool = urllib3.HTTPConnectionPool(host=args.url, retries=False)

    for thread_number in range(args.threads):
        threading.Thread(target=enumerate_dirs, args=(connection_pool, method, target_queue, response_queue), daemon=True).start()

    for i in range(target_queue_size):
        url, status = response_queue.get()
        print(url, status)
    target_queue.join()

if __name__ == "__main__":
    main()
