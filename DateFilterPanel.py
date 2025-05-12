import flet as ft
from typing import List, Dict, Any, Tuple, Optional, Callable
from enums import *
from log_reader import LogReader

class DateFilterPanel:
    def __init__(self, page: ft.Page, on_apply: Callable, on_reset: Callable):
        self.page = page
        self.on_apply = on_apply
        self.on_reset = on_reset

        self.start_date_text = ft.Text("Date")
        self.end_date_text = ft.Text("Date")
        self.start_date_raw = ""
        self.end_date_raw = ""

        self.apply_btn = ft.ElevatedButton("Apply filter", icon=ft.Icons.INFO, on_click=self.on_apply, disabled=True)
        self.reset_filter_btn = ft.ElevatedButton("Reset filter", icon=ft.Icons.CANCEL, on_click=self.on_reset,
                                                  disabled=True,bgcolor=ft.Colors.RED_100,color=ft.Colors.BLACK,icon_color=ft.Colors.BLACK)

        self.start_date_btn = ft.ElevatedButton(
            "Start date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(2000, 10, 1),
                    last_date=datetime.datetime(2035, 10, 1),
                    on_change=self.start_date_on_change,
                )
            ),
            disabled=True
        )

        self.end_date_btn = ft.ElevatedButton(
            "End date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(2000, 10, 1),
                    last_date=datetime.datetime(2035, 10, 1),
                    on_change=self.end_date_on_change,
                )
            ),
            disabled=True
        )

    def get_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.apply_btn,
                    self.reset_filter_btn,
                    self.start_date_btn,
                    self.end_date_btn,
                    self.start_date_text,
                    self.end_date_text,
                ],
                wrap=True,
                spacing=5
            ),
            expand=True,
            bgcolor=ft.Colors.WHITE,
            padding=10
        )

    def get_date_range(self):
        return (
            datetime.datetime.strptime(self.start_date_raw, '%m/%d/%Y'),
            datetime.datetime.strptime(self.end_date_raw, '%m/%d/%Y')
        )

    def start_date_on_change(self, e):
        self.start_date_raw = e.control.value.strftime('%m/%d/%Y')
        self.start_date_text.value = f'START: {self.start_date_raw}'
        self.start_date_text.update()
        self.check_apply_ready()

    def end_date_on_change(self, e):
        self.end_date_raw = e.control.value.strftime('%m/%d/%Y')
        self.end_date_text.value = f'END: {self.end_date_raw}'
        self.end_date_text.update()
        self.check_apply_ready()

    def check_apply_ready(self):
        if self.start_date_raw and self.end_date_raw:
            self.enable_apply()
        else:
            self.disable_apply()

    def reset_dates(self):
        self.start_date_raw = ""
        self.end_date_raw = ""
        self.start_date_text.value = 'Date'
        self.end_date_text.value = 'Date'
        self.start_date_text.update()
        self.end_date_text.update()

    # Button controls
    def enable_apply(self):
        self._toggle_btn(self.apply_btn, True)

    def disable_apply(self):
        self._toggle_btn(self.apply_btn, False)

    def enable_reset(self):
        self.reset_filter_btn.bgcolor=ft.Colors.RED_700
        self._toggle_btn(self.reset_filter_btn, True)

    def disable_reset(self):
        self.reset_filter_btn.bgcolor=ft.Colors.RED_100
        self._toggle_btn(self.reset_filter_btn, False)

    def enable_start_date(self):
        self._toggle_btn(self.start_date_btn, True)

    def disable_start_date(self):
        self._toggle_btn(self.start_date_btn, False)

    def enable_end_date(self):
        self._toggle_btn(self.end_date_btn, True)

    def disable_end_date(self):
        self._toggle_btn(self.end_date_btn, False)

    def _toggle_btn(self, btn, enabled):
        btn.disabled = not enabled
        btn.update()

