import flet as ft


def build(page: ft.Page):
    logo_image = ft.Image(src="img/neimark_logo.png", height=50, width=300)
    free_container = ft.Container(expand=True)

    header = ft.Row([logo_image, free_container, logo_image])
    return header


def main(page: ft.Page):
    data = build(page)
    page.add(data)


ft.app(target=main, assets_dir="src", port=80, view=ft.WEB_BROWSER)
