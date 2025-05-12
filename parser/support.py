import re
import json
import aiofiles

from typing import Any


async def write_json(obj: Any, file_name: str) -> None:
    async with aiofiles.open(f'{file_name}.json', mode='w', encoding='UTF-8') as file:
        await file.write(json.dumps(obj, indent=4, ensure_ascii=False))


async def read_json(file_name: str) -> Any:
    async with aiofiles.open(f'{file_name}.json', mode='r', encoding='UTF-8') as file:
        content = await file.read()
        return json.loads(content)


async def transform_product_name(product_name: str) -> str:
    check = re.search(r'[\"/*]', product_name)
    if check is not None:
        result = product_name.replace('"', '').replace('/', '').replace('*', '')
        return result

    return product_name


async def transform_info_in_text(obj: dict) -> str:
    result = '! '.join([': '.join(item) for item in obj.items()])
    return result

