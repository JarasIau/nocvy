#!/usr/bin/env python3
#SWDET v0.3
#Copyright (C) 2022  Jaraslau
#SWDET is licensed under GPL v3. Details in section License in README.md file.
import argparse
import aiohttp
import asyncio

class FileERR(Exception):
    '''Custom exception to be raised in form_wordlist()'''
class URLERR(Exception):
    '''Custom exception to be raised in enumerate_dirs()'''

def return_args():
    parser = argparse.ArgumentParser(description="Simple Website Directory Enumeration Tool.", epilog="Written by @Jaraslau")
    parser.add_argument("-u", "--url", type=str, required=True, help="url to begin the searching process (FULL URL, e.g. \"https://url.com/\")")
    parser.add_argument("-w", "--wordlist", type=str, required=True, help="point SWDET to a wordlist (Try wl.txt')")
    parser.add_argument("-m", "--head", action="store_true", help="use HEAD method instead of GET")
    parser.add_argument("-r", "--redirects", action="store_true", help="allow redirects")
    return parser.parse_args()

def form_wordlist(path, url):
    try:
        with open(path, "r", encoding = "UTF-8") as raw_wordlist:
            return ["".join((url, line)) for line in raw_wordlist]
    except FileNotFoundError:
        raise FileERR("No such file or directory. Try checking whether you gave the right path.")
    except PermissionError:
        raise FileERR("Insuficient permissions to manipulate the file. Try running as root.")
    except IsADirectoryError:
        raise FileERR("Given path leads to a directory. The path is supposed to lead to a file.")

async def enumerate_dirs(wordlist, head, redirects):
    try:
        async with aiohttp.ClientSession() as session:
            if head:
                tasks = [session.head(url, allow_redirects=redirects) for url in wordlist]
            else:
                tasks = [session.get(url, allow_redirects=redirects) for url in wordlist]
            return await asyncio.gather(*tasks)
    except aiohttp.client_exceptions.InvalidURL:
        raise URLERR("Try correcting your URL (e.g. append a protocol or a slash at the end) and relaunching the program.")
    except aiohttp.client_exceptions.ClientConnectorError:
        raise URLERR("Failed to establish a connection. Try checking your internet connection.")

async def main():
    args = return_args()
    wordlist = form_wordlist(args.wordlist, args.url)
    gathered = await enumerate_dirs(wordlist, args.head, args.redirects)
    for response in gathered:
        print(response.url, response.status)

if __name__ == "__main__":
    asyncio.run(main())
