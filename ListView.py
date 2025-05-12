import flet as ft
from typing import List, Dict, Any, Tuple, Optional, Callable
from enums import *
from log_reader import LogReader

class LogListView:
    def __init__(self, on_select: Callable[[int], None]):
        self.list_view = ft.ListView(controls=[], expand=True, disabled=True,height=270)
        self.selected_index = -1
        self.on_select = on_select
        self.next_btn = ft.ElevatedButton("NEXT", icon=ft.Icons.ARROW_FORWARD, on_click=self.go_next, disabled=True)
        self.prev_btn = ft.ElevatedButton("PREV", icon=ft.Icons.ARROW_BACK, on_click=self.go_prev, disabled=True)


    def get_container(self) -> ft.Container:
        return ft.Container(content=self.list_view, expand=True, bgcolor=ft.Colors.WHITE)

    def get_navigation_buttons(self) -> List[ft.Control]:
        return [self.next_btn, self.prev_btn]

    def prepare_log_text(self, logs: List[Dict[str, Any]]) -> List[str]:
        result = []
        for log in logs:
            formatted_parts = []
            for idx in range(15):
                if idx < len(log) and idx in attribute_info:
                    value = log[attribute_info[idx][0]]
                    formatted_parts.append(f"{str(value)}")
            result.append(" | ".join(formatted_parts))
        return result

    def update_list(self, logs: List[Dict[str, Any]]):
        log_texts = self.prepare_log_text(logs)
        tiles = [
            ft.ListTile(
                title=ft.Text(
                    log,
                    size=18,
                    selectable=True,
                    max_lines=1,
                    color=ft.Colors.BLACK,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                key=str(i),
                on_click=self.select_item_handler(int(i))  # Zmienione na select_item_handler
            )
            for i, log in enumerate(log_texts)
        ]
        self.list_view.controls = tiles
        self.list_view.disabled = False  # Włączamy listę
        self.list_view.update()

    # Nowa metoda zwracająca handler zdarzenia click
    def select_item_handler(self, index: int):
        def handle_click(e):
            self.select_item(index)
        return handle_click

    def select_item(self, index: int):
        if 0 <= index < len(self.list_view.controls):
            if 0 <= self.selected_index < len(self.list_view.controls):
                self.list_view.controls[self.selected_index].bgcolor = None

            self.selected_index = index
            self.list_view.controls[self.selected_index].bgcolor = ft.Colors.BLUE
            self.list_view.update()

            self.update_navigation_buttons()
            self.on_select(index)

    def init_selecting(self):
        if self.list_view.controls:
            self.select_item(0)

    def go_next(self, e):
        if self.selected_index < len(self.list_view.controls) - 1:
            self.select_item(self.selected_index + 1)
            self.list_view.scroll_to(key=str(self.selected_index), duration=300)

    def go_prev(self, e):
        if self.selected_index > 0:
            self.select_item(self.selected_index - 1)
            self.list_view.scroll_to(key=str(self.selected_index), duration=300)

    def update_navigation_buttons(self):
        self._toggle_btn(self.prev_btn, self.selected_index > 0)
        self._toggle_btn(self.next_btn, self.selected_index < len(self.list_view.controls) - 1)

    def enable_next(self):
        self._toggle_btn(self.next_btn, True)

    def disable_next(self):
        self._toggle_btn(self.next_btn, False)

    def enable_prev(self):
        self._toggle_btn(self.prev_btn, True)

    def disable_prev(self):
        self._toggle_btn(self.prev_btn, False)

    def _toggle_btn(self, btn, enabled):
        btn.disabled = not enabled
        btn.update()
