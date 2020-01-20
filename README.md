LastFM API (Python wrapper)
========
Feature important queries to the lastfm api, translating the responses to python specific terminology

## Installing

```
python3 -m pip install -U git+https://gitlab.com/midnight-society/lastfm
```

## Requirements
- Python 3.6
- asyncio
- aiohttp

## Start Process
```
from lastfm import LastFM_API
import asyncio


api = LastFM_API(api_key=api_key)


async def lotus_info():
    lotus = api.get_user('awhitelotus')
    info = await lotus.fetch_info()
    print(info)
    return info


loop = asyncio.get_event_loop()
loop.run_until_complete(lotus_info())
```