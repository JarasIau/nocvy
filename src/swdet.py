#!/usr/bin/env python3
#SWDET v0.2
#Copyright (C) 2022  Jaraslau
#SWDET is licensed under GPL v3. Details in section License in README.md file.
import argparse
import aiohttp
import asyncio

def return_args():
    parser = argparse.ArgumentParser(description="Simple Website Directory Enumeration Tool.", epilog="Written by @Jaraslau")
    parser.add_argument("-u", "--url", type=str, required=True, help="url to begin the searching process (FULL URL, e.g. \"https://url.com/\")")
    parser.add_argument("-w", "--wordlist", type=str, required=True, help="point SWDET to a wordlist (Try wl.txt')")
    parser.add_argument("-m", "--head", action="store_true", help="use HEAD method instead of GET")
    parser.add_argument("-r", "--redirects", action="store_true", help="allow redirects")
    return parser.parse_args()

def form_wordlist(path, url):
    with open(path, "r", encoding = "UTF-8") as raw_wordlist:
        return ["".join((url, line)) for line in raw_wordlist]

async def enumerate_dirs(wordlist, head, redirects):
    async with aiohttp.ClientSession() as session:
        if head:
            tasks = [session.head(url, allow_redirects=redirects) for url in wordlist]
        else:
            tasks = [session.get(url, allow_redirects=redirects) for url in wordlist]
        return await asyncio.gather(*tasks)

async def main():
    args = return_args()
    wordlist = form_wordlist(args.wordlist, args.url)
    gathered = await enumerate_dirs(wordlist, args.head, args.redirects)
    for response in gathered:
        print(response.url, response.status)

if __name__ == "__main__":
    asyncio.run(main())
