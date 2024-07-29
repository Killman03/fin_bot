import re


async def resolve(data):
    pattern = re.compile(r'\d+|[\+\-\*/]')
    if pattern.search(data):
        try:
            return eval(data)
        except:
            return data
