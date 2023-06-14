import aiohttp
import asyncio
from more_itertools import chunked
from models import engine, SWPeople, Base, Session


async def films(data: str) -> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    await session.close()
    return json_data["title"]


async def homeworld(data: str) -> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    await session.close()
    return json_data["name"]


async def species(data: str) -> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    await session.close()
    return json_data['name']


async def starships(data: str) -> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    await session.close()
    return json_data['name']


async def vehicles(data: str) -> str:
    session = aiohttp.ClientSession()
    response = await session.get(data)
    json_data = await response.json()
    await session.close()
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
    person_info = {
        "id": people_id,
        'birth_year': result['birth_year'],
        'eye_color': result['eye_color'],
        'films': await hub(result['films'], films),
        "gender": result['gender'],
        "hair_color": result['hair_color'],
        "height": result['height'],
        "homeworld": await hub(result['homeworld'], homeworld),
        "mass": result['mass'],
        "name": result['name'],
        'skin_color': result['skin_color'],
        'species': await hub(result['species'], species),
        'starships': await hub(result['starships'], starships),
        'vehicles': await hub(result['vehicles'], vehicles),
    }
    return person_info


async def paste_to_db(persons_json):
    async with Session() as session:
        orm_objects = [SWPeople(**item) for item in persons_json if item]
        session.add_all(orm_objects)
        await session.commit()


async def main():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    person_coros = (create_dict(i) for i in range(1, 84))
    person_coros_ch = chunked(person_coros, 5)
    for p in person_coros_ch:
        persons = await asyncio.gather(*p)
        asyncio.create_task(paste_to_db(persons))
    tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks)


asyncio.run(main())
