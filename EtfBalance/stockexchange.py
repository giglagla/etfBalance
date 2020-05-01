#!/usr/bin/python
from urllib.parse import urlencode
import aiohttp
import asyncio
import json
import sys
import time


API_KEY = 'bqk1nffrh5r9t8htebpg'
BASE_URL = 'https://finnhub.io/api/v1'

async def fetchJson(url, params):
    """ Fetch a web page in json-encoded content """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json()


async def gatherResources(resources):
    """ Gather resources and schedule them concurrently  """
    coroutines = []
    for resource in resources:
        resource.get("params").update({'token': API_KEY})
        coroutines.append(fetchJson(resource.get("url"), resource.get("params")))

    return await asyncio.gather(*coroutines)

async def currentPrice(*symbols):
    """ Get stocks symboles current prices """
    resources = []
    for symbol in symbols:
        url = BASE_URL + "/quote"
        params = {'symbol': symbol}
        resources.append({"url":url, "params":params})

    # Get only the "c" field of each result
    results = map(lambda result: result["c"], await gatherResources(resources))
    return list(results)

async def stockExchanges():
    """ Get a list of all stock exchanges """
    url = BASE_URL + "/stock/exchange"
    return await gatherResources([{"url":url, "params":{}}])


if __name__ == '__main__':
    asyncio.run(currentPrice('ESE.PA','ESE.PA','ESE.PA','ESE.PA','ESE.PA'))
    asyncio.run(stockExchanges())

    sys.exit()
