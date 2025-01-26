import flet as ft
import requests
from models import Products

api_address = 'http://192.168.52.80:12345'


def create_card(page: ft.Page, image, name, price):
    # Картинка
    product_image_1 = ft.Image(f'products/{image}', fit=ft.ImageFit.COVER)

    # Текстовые элементы
    product_name_1 = ft.Text(f'{name}', color='black', text_align=ft.TextAlign.CENTER,
                             width=page.width * 0.4)
    product_price_1 = ft.Text(f'{price}', color='black', text_align=ft.TextAlign.CENTER, width=page.width * 0.4)

    # Контейнер с изображением
    image_container = ft.Container(content=product_image_1)

    # Контейнер для текста с выравниванием по горизонтали и вертикали
    text_container = ft.Column(
        [product_name_1, product_price_1],
        alignment=ft.MainAxisAlignment.CENTER,  # Выравнивание по вертикали
        horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Выравнивание по горизонтали
    )

    btn_add = ft.IconButton(icon=ft.icons.ADD, icon_color='black')
    btn_remove = ft.IconButton(icon=ft.icons.REMOVE, icon_color='black')
    product_counter = ft.Text('0', color='black')
    btn_container = ft.Container(content=ft.Row([btn_remove, product_counter, btn_add],
                                                alignment=ft.MainAxisAlignment.CENTER))

    # Главный контейнер (карточка)
    card_container = ft.Container(
        content=ft.Column([image_container, text_container, btn_container], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor='#FFFFFF',
        border_radius=20,
        width=page.width * 0.4
    )
    return card_container


def gen_cards(page: ft.Page):
    response = requests.get(f'{api_address}/products/all')
    data = response.json()
    answer = Products.model_validate(data)

    i, counter = 0, len(answer.data)
    products_rows = []
    while counter != 0:
        if counter - 2 >= 0:
            products_rows.append(ft.Row([
                create_card(page, answer.data[i].image, answer.data[i].name, answer.data[i].price),
                create_card(page, answer.data[i + 1].image, answer.data[i + 1].name, answer.data[i + 1].price)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=page.width * 0.05))
            counter -= 2
            i += 2
        else:
            products_rows.append(ft.Row([
                create_card(page, answer.data[i].image, answer.data[i].name, answer.data[i].price)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=page.width * 0.05))
            counter -= 1
            i += 1
    return products_rows


def build_main(page: ft.Page, user_id: int, user_hash: str):
    print(user_id, user_hash)
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
    body = ft.Column(gen_cards(page), scroll="always", expand=True, spacing=page.height * 0.02)

    frame = ft.Column([
        header,
        body
    ],
        expand=True)
    return frame


def start(page: ft.Page):
    print(page.route)
    if page.route == "/basket":
        return ft.Text("basket")
    elif page.route.find("/login/") != -1:
        ip, data = page.route.split("/login/")
        user_id, user_hash = data.split("/")
        return build_main(page, user_id, user_hash)
    else:
        return build_main(page, 0, "2")


def card_generator(name: str, price: int, img: str) -> ft.Container:
    pass


def on_resize(e: ft.ControlEvent):
    e.page: ft.Page
    e.page.clean()
    data = start(e.page)
    e.page.add(data)


def on_route_change(e: ft.RouteChangeEvent):
    data = start(e.page)
    e.page.clean()
    e.page.add(data)
    e.page.update()


def main(page: ft.Page):
    data = start(page)
    page.add(data)

    page.on_resized = on_resize
    page.on_route_change = on_route_change


ft.app(target=main, assets_dir="src", view=ft.WEB_BROWSER, port=2222)
