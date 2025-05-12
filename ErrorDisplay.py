import flet as ft
from typing import List, Dict, Any, Tuple, Optional, Callable
from enums import *
from log_reader import LogReader

class ErrorDisplay:
    def __init__(self):
        self.error_text = ft.Text("", size=20, text_align=ft.TextAlign.CENTER)
        self.error_box = ft.Container(
            expand=True,
            bgcolor=ft.Colors.RED_50,
            content=ft.Row(
                [ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.RED), self.error_text],
            ),
            visible=False,
            padding=10
        )

    def get_container(self) -> ft.Container:
        return self.error_box

    def show(self, error: str):
        self.error_text.value = error
        self.error_box.visible = True
        self.error_text.update()
        self.error_box.update()

    def clear(self):
        self.error_text.value = ""
        self.error_box.visible = False
        self.error_text.update()
        self.error_box.update()
