import flet as ft
import requests
from models import Products

api_address = 'http://192.168.52.80'


def gen_cards(page: ft.Page):
    response = requests.get(f'{api_address}/products/all')
    data = response.json()
    answer = Products.model_validate(data)

    i, counter = 0, len(answer.data)
    products_rows = []
    while counter != 0:
        if counter - 2 >= 0:
            product_image_1 = ft.Image(f'products/{answer.data[i].image}', fit=ft.ImageFit.FILL, height=0.5 * page.height, width=0.4 * page.width
                                       )
            product_name_1 = ft.Text(f'{answer.data[i].name}')
            product_price_1 = ft.Text(f'{answer.data[i].price}')
            card_1 = ft.Container(
                content=ft.Column([product_image_1, product_name_1, product_price_1]),
                bgcolor='#262626',
                border_radius=20,
                width=page.width * 0.4,
                height=page.height * 0.6
            )
            product_image_2 = ft.Image(f'products/{answer.data[i + 1].image}', fit=ft.ImageFit.FILL, height=0.5 * page.height, width=0.4 * page.width)
            product_name_2 = ft.Text(f'{answer.data[i + 1].name}')
            product_price_2 = ft.Text(f'{answer.data[i + 1].price}')
            card_2 = ft.Container(
                content=ft.Column([product_image_2, product_name_2, product_price_2]),
                bgcolor='#262626',
                border_radius=20,
                width=page.width * 0.4,
                height=page.height * 0.6
            )
            products_rows.append(ft.Row([card_1, card_2],
                                        spacing=page.width * 0.07,
                                        alignment=ft.MainAxisAlignment.CENTER))
            counter -= 2
            i += 2
        else:
            product_image_1 = ft.Image(f'products/{answer.data[i].image}')
            product_name_1 = ft.Text(f'{answer.data[i].name}')
            product_price_1 = ft.Text(f'{answer.data[i].price}')
            card_1 = ft.Container(
                content=ft.Column([product_image_1, product_name_1, product_price_1]),
                bgcolor='#262626',
                border_radius=20,
                width=page.width * 0.4,
                height=page.height * 0.6
            )
            products_rows.append(ft.Row([card_1],
                                        spacing=page.width * 0.07,
                                        alignment=ft.MainAxisAlignment.CENTER))
            counter -= 1
            i += 1
    return products_rows


def build_main(page: ft.Page):
    page.bgcolor = '#000000'
    logo_image = ft.Container(ft.Image(src="img/logo.svg", width=page.width * 0.3))
    free_container = ft.Container(expand=True)

    basket = ft.Container(
        content=ft.Image(src="img/basket.svg", width=50),
        border_radius=1000,
    )

    account_icon = ft.Container(
        content=ft.Image(src="img/account_icon.svg", width=50)
    )

    buttons = ft.Row(
        [basket, account_icon], spacing=page.width * 0.01
    )

    header = ft.Row([logo_image, free_container, buttons])
    body = ft.Column(gen_cards(page), scroll="always", expand=True)

    frame = ft.Column([
        header,
        body
    ],
        expand=True)
    return frame


def card_generator(name: str, price: int, img: str) -> ft.Container:
    pass


def on_resize(e: ft.ControlEvent):
    e.page: ft.Page
    e.page.clean()
    data = build_main(e.page)
    e.page.add(data)
    e.page.update()


def main(page: ft.Page):
    data = build_main(page)
    page.add(data)

    page.on_resized = on_resize


ft.app(target=main, assets_dir="src", view=ft.WEB_BROWSER),  # port=8000)
