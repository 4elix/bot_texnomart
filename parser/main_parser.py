import os
import asyncio
import aiofiles
import aiohttp

from tqdm import tqdm
from bs4 import BeautifulSoup

from config import HOST, start_link, headers
from support import write_json, read_json, transform_product_name


async def get_html_code(session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
    async with session.get(url=url) as response:
        html_code = BeautifulSoup(await response.text(), 'html.parser')
        return html_code


async def get_data_categories(session: aiohttp.ClientSession) -> dict:
    html_code = await get_html_code(session, start_link)
    object_categories = {}
    main_block = html_code.find('div', class_='category__wrap')
    blocks = main_block.find_all('div', class_='category__item')

    for block in blocks:
        list_sub_categories = block.find('div', class_='content__wrap').find_all('div', class_='content__item')
        for sub_category in tqdm(list_sub_categories, desc='Парсинг под категорий', unit='под категория'):
            name_category = sub_category.find('a', class_='content__link').get_text(strip=True)
            link_category = HOST + sub_category.find('a', class_='content__link')['href']
            object_categories[name_category] = link_category

    return object_categories


async def get_info_product(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> dict:
    info = {}
    async with semaphore:
        html_code = await get_html_code(session, url)
    try:
        main_list = html_code.find('ul', class_='characteristic__wrap').find_all('li', class_='characteristic__item')
        for item in main_list:
            info_name = item.find('h2', class_='characteristic__name').find('span').get_text(strip=True)
            info_value = item.find('span', class_='characteristic__value').get_text(strip=True)
            info[info_name] = info_value
    except Exception as error:
        print(error)
        print(error.__class__)
        print(error.__class__.__name__)
    return info


async def save_product_image(session: aiohttp.ClientSession, url_image: str, product_name: str, product_category: str) -> str:
    async with session.get(url=url_image) as response:
        bytes_image = await response.read()

    new_name_product = await transform_product_name(product_name)
    path_dirs = f'images/{product_category}'
    path_image = f'{path_dirs}/{new_name_product}.jpg'

    if not os.path.exists(path_dirs):
        os.makedirs(path_dirs)

    async with aiofiles.open(path_image, mode='wb') as img:
        await img.write(bytes_image)

    return path_image


async def get_product_data_from_card(card, session, name_category, semaphore):
    try:
        title = card.find('h2').get_text(strip=True)
        current_price = card.find('div', class_='product-price__current').get_text(strip=True)
        link_detail = HOST + card.find('a', class_='product-name')['href']
        link_image = card.find('img', class_='product-image')['data-src']

        info = await get_info_product(session, link_detail, semaphore)
        path_image = await save_product_image(session, link_image, title, name_category)

        return {
            'title': title,
            'current_price': current_price,
            'info': info,
            'path_image': path_image
        }

    except Exception as error:
        print(f"Ошибка при обработке товара: {error}")
        return None


async def get_data_products(session: aiohttp.ClientSession) -> dict:
    links_categories = await read_json('categories')
    object_products = {}
    # Semaphore(10) -> не больше 10 задач могут выполняться одновременно в этом месте кода.
    semaphore = asyncio.Semaphore(10)

    for name_category, link_category in tqdm(links_categories.items(), desc='Парсинг категорий', unit='категория'):
        html_page_category = await get_html_code(session, link_category)
        try:
            cards = html_page_category.find('div', class_='products-box').find_all('div', class_='col-3')
            tasks = [
                get_product_data_from_card(card, session, name_category, semaphore)
                for card in cards
            ]
            # asyncio.gather(*tasks) -> запуск всех асинхронных задачи параллельно и пока все они не завершатся дольше код не идет
            products = await asyncio.gather(*tasks)
            products = [p for p in products if p is not None]
            object_products[name_category] = products if products else 'Нет товаров'

        except Exception as error:
            object_products[name_category] = 'Ошибка при парсинге'
            print(error)

    return object_products


async def main():
    async with aiohttp.ClientSession(headers=headers) as session:
        data_categories = await get_data_categories(session)
        await write_json(data_categories, 'categories')

        data_products = await get_data_products(session)
        await write_json(data_products, 'products')


if __name__ == "__main__":
    asyncio.run(main())