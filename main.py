import json
import os

import flet as ft
import requests

from models import Products, Product

api_address = 'http://localhost:12345'


def get_token(user_id: int):
    response = requests.get(f"{api_address}/get_token", data=json.dumps({"user_id": user_id}))
    return response.text.strip('"')


def check_activation(user_id: int):
    response = requests.get(f"{api_address}/check_activation", data=json.dumps({"user_id": user_id}))
    return int(response.text.strip('"'))


def add_btn_on_click(e, counter, btn, image):
    e.page: ft.Page
    btn.disabled = False
    basket = e.page.session.get('basket')
    file_name_without_extension = os.path.splitext(os.path.basename(image))[0]
    if basket is None:
        basket = {}
        dat = int(counter.value)
    else:
        dat = basket.get(file_name_without_extension)
        if dat is None:
            dat = 0
    dat += 1
    counter.value = dat
    basket[file_name_without_extension] = dat
    e.page.session.set("basket", basket)
    e.page.update()
    print(e.page.session.get("user_id"), e.page.session.get('basket'))


def remove_btn_on_click(e, counter, btn, image):
    e.page: ft.Page
    basket = e.page.session.get('basket')
    file_name_without_extension = os.path.splitext(os.path.basename(image))[0]
    if basket is None:
        basket = {}
        dat = int(counter.value)
    else:
        dat = basket.get(file_name_without_extension)
        if dat is None:
            dat = 0
    dat -= 1
    if dat <= 0:
        dat = 0
        btn.disabled = True
    counter.value = dat
    basket[file_name_without_extension] = dat
    e.page.session.set("basket", basket)
    e.page.update()
    print(e.page.session.get("user_id"), e.page.session.get('basket'))


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

    file_name_without_extension = os.path.splitext(os.path.basename(image))[0]

    value = "0"
    if page.session.get("basket"):
        value = str(page.session.get("basket").get(file_name_without_extension) or 0)

    product_counter = ft.Text(value, color='black')
    btn_add = ft.IconButton(icon=ft.Icons.ADD, icon_color='black',
                            on_click=lambda e: add_btn_on_click(e, product_counter, btn_remove, image))
    btn_remove = ft.IconButton(icon=ft.Icons.REMOVE, icon_color='black',
                               on_click=lambda e: remove_btn_on_click(e, product_counter, btn_remove, image))
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
    page.session.set("user_id", user_id)
    page.session.set("user_hash", user_hash)
    page.bgcolor = '#000000'
    logo_image = ft.Container(ft.Image(src="img/logo.svg", width=page.width * 0.3), on_click=lambda e: page.launch_url("https://neimark-it.ru"))
    free_container = ft.Container(expand=True)

    basket = ft.Container(
        content=ft.Image(src="img/basket.svg", width=50),
        border_radius=1000,
        on_click=lambda e: page.go("/basket")
    )

    account_icon = ft.Container(
        content=ft.Image(src="img/account_icon.svg", width=50)
    )

    buttons = ft.Row(
        [basket, account_icon], spacing=page.width * 0.01
    )

    response = requests.get(f'{api_address}/get_balance', data=json.dumps({'user_id': page.session.get('user_id')}))
    data = int(response.text.strip('"'))

    balance = ft.Row([ft.Text(f'ВАШ БАЛАНС: {data}', color='#FFFFFF')],
                     alignment=ft.MainAxisAlignment.CENTER)

    header = ft.Row([logo_image, free_container, buttons])
    body = ft.Column([balance, *gen_cards(page)], scroll="always", expand=True, spacing=page.height * 0.02)

    frame = ft.Column([
        header,
        body
    ],
        expand=True)
    return frame


def build_basket(page: ft.Page):
    page.bgcolor = '#000000'
    btn_back = ft.Container(ft.Image(src="img/arrow.svg", width=50), on_click=lambda e: page.go(f"/login/{page.session.get('user_id')}/{page.session.get('user_hash')}"))
    basket_text = ft.Container(ft.Image(src="img/basket_text.svg", width=page.width * 0.2))

    data_basket = page.session.get('basket')
    rows = []
    final_price = 0
    rows.append(ft.Row([
        ft.Text(f'ТОВАР', color='#FFFFFF', width=page.width * 0.5,
                text_align=ft.TextAlign.CENTER),
        ft.Text(f'КОЛ-ВО', color='#FFFFFF', width=page.width * 0.25,
                text_align=ft.TextAlign.CENTER),
        ft.Text(f'ЦЕНА', color='#FFFFFF', width=page.width * 0.25,
                text_align=ft.TextAlign.CENTER)
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY))
    if data_basket is None:
        data_basket = {}
    else:
        print(data_basket)
        for i in data_basket.keys():
            if data_basket[i] != 0:
                response = requests.get(f'{api_address}/products/get', data=json.dumps({"product_id": int(i)}))
                data = response.json()
                print(data)
                answer = Product.model_validate(data)

                rows.append(ft.Row([
                    ft.Text(f'{answer.name}', color='#FFFFFF', width=page.width * 0.5),
                    ft.Text(f'{data_basket[i]} шт.', color='#FFFFFF', width=page.width * 0.25,
                            text_align=ft.TextAlign.CENTER),
                    ft.Text(f'{answer.price * data_basket[i]}', color='#FFFFFF', width=page.width * 0.25,
                            text_align=ft.TextAlign.CENTER)
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY))
                final_price += answer.price * data_basket[i]

    final_price_row = ft.Row([
        ft.Text(f'ИТОГОВАЯ ЦЕНА: {final_price}', color='#FFFFFF')
    ], alignment=ft.MainAxisAlignment.CENTER)

    header = ft.Row([btn_back, basket_text], spacing=page.width * 0.02)
    body = ft.Column(controls=rows, scroll="always", expand=True, spacing=page.height * 0.02)

    order = ft.Container(ft.Image(src="img/btn_order.svg", width=page.width * 0.8),
                         alignment=ft.alignment.center)

    frame = ft.Column([
        header,
        body,
        final_price_row,
        order
    ],
        expand=True)
    return frame


def start(page: ft.Page):
    if page.route == "/basket":
        return build_basket(page)
    elif page.route.find("/login/") != -1:
        ip, data = page.route.split("/login/")
        user_id, user_hash = data.split("/")
        if user_hash != get_token(user_id):
            return ft.Text("Вы зашли не со своего аккаунта")
        elif bool(check_activation(user_id)) is False:
            return ft.Text("Ваша учетная запись не активирована")
        return build_main(page, user_id, user_hash)
    else:
        return ft.Text("Вы зашли не с телеграмма")


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
