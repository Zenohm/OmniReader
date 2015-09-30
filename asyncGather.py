import asyncio

full_text = []


async def fetch(url):
    print("Task %s: Fetching..." % (url.text))
    url.initialize()
    await asyncio.sleep(1)
    full_text.append(url.text)
    print("%s completed" % (url.url))

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(fetch(url)) for url in full_frontal_storytime]
loop.run_until_complete(asyncio.wait(tasks))
