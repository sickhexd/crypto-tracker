import flet as ft
import pandas as pd
import func

def main(page: ft.Page):
    page.title = 'Crypto-Tracker'
    page.theme_mode = 'dark'
    page.window_width = 650
    page.window_height = 450

    
    
    user_output = ft.Text(value='')
    user_output_table = ft.Text(value='')
    input1 = ft.Dropdown(
        label='Enter first currency:',options=[
            ft.dropdown.Option("btc"),
            ft.dropdown.Option("eth"),
            ft.dropdown.Option("doge"),
            ft.dropdown.Option("usdt"),
            ft.dropdown.Option("trx"),
            ft.dropdown.Option("toncoin"),
            ft.dropdown.Option("ltc"),
            ], 
            on_change=lambda _: update_output()
            )
    input2 = ft.Dropdown(
        label='Enter second currency:',options=[
            ft.dropdown.Option("btc"),
            ft.dropdown.Option("eth"),
            ft.dropdown.Option("doge"),
            ft.dropdown.Option("usdt"),
            ft.dropdown.Option("trx"),
            ft.dropdown.Option("toncoin"),
            ft.dropdown.Option("ltc"),
            ], 
            on_change=lambda _: update_output()
            )

    row1 = ft.Row([input1, input2], alignment=ft.MainAxisAlignment.CENTER)
    row2 = ft.Row([user_output], alignment=ft.MainAxisAlignment.CENTER)
    row3 = ft.Row([user_output_table], alignment=ft.MainAxisAlignment.CENTER)

    rows_added = False

    def button_clicked(e):
        nonlocal rows_added
        if not rows_added:
            page.add(row1, row2, row3)
            rows_added = True
        else:
            page.remove(row1, row2, row3)
            rows_added = False
   
            

    trades_bottom = ft.TextButton('Trades', on_click= button_clicked, data=0)


    def update_output():
        nonlocal user_output, user_output_table
        if input1.value == input2.value:
            user_output.value = 'error'
            user_output_table.value = ''
        else:
            user_output.value = func.get_trades(input1.value, input2.value)
            user_output_table.value = func.data_framed(input1.value, input2.value)
        user_output.update()
        user_output_table.update()

    page.add(
        ft.Row([trades_bottom],alignment=ft.MainAxisAlignment.CENTER),
    )

ft.app(target=main)
