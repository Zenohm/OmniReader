import asyncio

"""
    def afetch(stories):
        full_text = []
        async def fetch(url):
            print("Task %s: Fetching..." % (url.text))
            url.initialize()
            await asyncio.sleep(.1)
            full_text.append(url.text)
            print("%s Complete." % (url.url))
        
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(fetch(url)) for url in stories]
        loop.run_until_complete(asyncio.wait(tasks))
        return full_text
"""

print("No worries, this hasn't been added yet.")

"""
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
"""
