import json
import aiohttp


async def req(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.text()
            data = data.encode().decode('unicode-escape')
            jsonDump = json.dumps(data)
            jsonResult = json.load(jsonDump)
            return jsonResult
