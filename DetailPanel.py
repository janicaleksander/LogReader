import flet as ft
from typing import List, Dict, Any, Tuple, Optional, Callable
from enums import *
from log_reader import LogReader

class DetailPanel:
    def __init__(self):
        self.text_remote_host = ft.Text("", color=ft.Colors.BLACK,size=15)
        self.text_date = ft.Text("", color=ft.Colors.BLACK,size=15)
        self.text_time = ft.Text("", color=ft.Colors.BLACK,size=15)
        self.text_method = ft.Text("", color=ft.Colors.BLACK,size=15)
        self.text_code = ft.Text("", color=ft.Colors.BLACK,size=15)
        self.text_resource = ft.Text("", color=ft.Colors.BLACK,size=15)
        self.text_size = ft.Text("", color=ft.Colors.BLACK,size=15)

    def color_code(self, code):
        if code == "200":
            return ft.Colors.GREEN
        elif code == "404":
            return ft.Colors.RED
        else:
            return ft.Colors.BLACK

    def set_code(self, code):
        self.text_code.value = code
        self.text_code.color = self.color_code(code)

    def get_container(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([ft.Text("HOST:", width=100, weight="bold", color=ft.Colors.BLACK), self.text_remote_host],
                           expand=True),
                    ft.Row([ft.Text("DATE:", width=100, weight="bold", color=ft.Colors.BLACK), self.text_date],
                           expand=True),
                    ft.Row([ft.Text("TIME:", width=100, weight="bold", color=ft.Colors.BLACK), self.text_time],
                           expand=True),
                    ft.Row([ft.Text("METHOD", width=100, weight="bold", color=ft.Colors.BLACK), self.text_method],
                           expand=True),
                    ft.Row([ft.Text("CODE:", width=100, weight="bold", color=ft.Colors.BLACK), self.text_code],
                           expand=True),
                    ft.Row([ft.Text("RESOURCE:", width=100, weight="bold", color=ft.Colors.BLACK), self.text_resource],
                           expand=True),
                    ft.Row([ft.Text("SIZE:", width=100, weight="bold", color=ft.Colors.BLACK), self.text_size],
                           expand=True),
                ],
                spacing=5
            ),
            expand=True,
            bgcolor=ft.Colors.WHITE,
            padding=10
        )

    def clear(self):
        self.update("", "", "", "", "", "", "")

    def update(self, host: str, date: str, time: str, method: str, code: str, resource: str, size: str):
        self.text_remote_host.value = host
        self.text_date.value = date
        self.text_time.value = time
        self.text_method.value = method
        #self.text_code.value = code
        self.set_code(code)
        self.text_resource.value = resource
        self.text_size.value = size

        self.text_remote_host.update()
        self.text_date.update()
        self.text_time.update()
        self.text_method.update()
        self.text_code.update()
        self.text_resource.update()
        self.text_size.update()

    def update_from_log(self, log_dict):
        self.update(
            log_dict["host"],
            str(log_dict["ts"].date()),
            str(log_dict["ts"].time()),
            log_dict["method"],
            str(log_dict["status_code"]),
            log_dict["uri"],
            str(log_dict["request_body_len"])
        )
