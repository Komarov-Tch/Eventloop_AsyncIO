import aiohttp
import asyncio
from more_itertools import chunked
#from models import engine, SWPeople


async def films(data:str) -> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    return json_data["title"]


async def homeworld(data:str) -> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    return json_data["name"]


async def species(data:str) -> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    return json_data['name']


async def starships(data:str) -> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    return json_data['name']


async def vehicles(data:str)-> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    return json_data['name']


async def get_people(people_id):
    session = aiohttp.ClientSession()
    response = await session.get(f'https://swapi.dev/api/people/{people_id}')
    json_data = await response.json()
    await session.close()
    return json_data

async def hub(data, arg):
    r = []
    if arg == homeworld:
        data = [data]
    for i in data:
        r.append(arg(i))
    r = ', '.join(await asyncio.gather(*r))
    return r


async def create_dict(people_id):
    result = await get_people(people_id)
    if len(result) == 1:
        return None
    f =  await hub(result['films'], films)
    h = await hub(result['homeworld'], homeworld)
    sp = await hub(result['species'], species)
    st = await hub(result['starships'], starships)
    ve = await hub(result['vehicles'], vehicles)
    person_info = {
        "id" : people_id,
        'birth_year': result['birth_year'],
        'eye_color': result['eye_color'],
        'films': f,
        "gender": result['gender'],
        "hair_color": result['hair_color'],
        "height": result['height'],
        "homeworld": h,
        "mass": result['mass'],
        "name": result['name'],
        'skin_color': result['skin_color'],
        'species': sp,
        'starships': st,
        'vehicles': ve,
    }
    return person_info


async def main():
    person_coros = (create_dict(i) for i in range(1, 84))
    person_coros_ch = chunked(person_coros, 2)
    for p in person_coros_ch:
        persons = await asyncio.gather(*p)
        print(persons)

asyncio.run(main())