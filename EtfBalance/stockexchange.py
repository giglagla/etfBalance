#!/usr/bin/env python3.7

from urllib.parse import urlencode
import aiohttp
import asyncio
import json
import sys
import time


RAPIDAPI_KEY = '7ce7f37e24msh5cd3c0ae48bc6cep1e367djsneddc64324900'
RAPIDAPI_HOST = 'apidojo-yahoo-finance-v1.p.rapidapi.com'
RAPIDAPI_URL = 'https://' + RAPIDAPI_HOST


async def fetchJson(url, params):
    """ Fetch a web page in json-encoded content """
    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params) as response:
            return await response.json()


async def gatherResources(resources):
    """ Gather resources and schedule them concurrently  """
    coroutines = []
    for resource in resources:
        resource.get("params").update({'region': 'FR', 'lang': 'fr'})
        coroutines.append(fetchJson(resource.get("url"), resource.get("params")))

    return await asyncio.gather(*coroutines)


async def currentPrice(*symbols):
    """ Get stocks symboles current prices """
    url = RAPIDAPI_URL + "/market/v2/get-quotes"
    params = {'symbols': ','.join(symbols)}
    resources = [{"url": url, "params": params}]

    results = map(lambda result: result['regularMarketPrice'],
                  (await gatherResources(resources))[0]['quoteResponse']['result'])
    return list(results)


async def stockExchanges():
    """ Get a list of all stock exchanges """
    url = RAPIDAPI_URL + "/market/v2/get-summary"
    return await gatherResources([{"url": url, "params": {}}])


if __name__ == '__main__':
    prices = asyncio.run(currentPrice('ESE.PA', 'VEUR.AS', 'PAEEM.PA', 'PTPXE.PA'))
    stocks = asyncio.run(stockExchanges())
    print(prices)
    print(stocks)
    sys.exit()
