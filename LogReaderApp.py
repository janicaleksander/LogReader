APP_TITLE = "Log Reader"
import flet as ft
from typing import List, Dict, Any, Tuple, Optional, Callable
from enums import *
from log_reader import LogReader
from DateFilterPanel import DateFilterPanel
from DetailPanel import DetailPanel
from ErrorDisplay import ErrorDisplay
from ListView import LogListView

class LogReaderApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.Colors.BLUE_50
        self.page.title = APP_TITLE
        self.page.window_width = 900
        self.page.window_height = 900
        self.page.window.resizable = True
        self.page.update()
        self.page.scroll = "adaptive"


        # Data model
        self.log_reader = LogReader()
        self.current_logs = []
        self.backup_logs = []

        # Components
        self.counter = ft.Row(
            controls=[
                ft.Text("Logs ready to read:", size=15),
                ft.Text("", size=25, color=ft.Colors.BLUE,weight=ft.FontWeight.BOLD)
            ],
        )

        self.error_display = ErrorDisplay()
        self.detail_panel = DetailPanel()
        self.list_view = LogListView(on_select=self.on_log_selected)
        self.date_filter = DateFilterPanel(
            page=self.page,
            on_apply=self.apply_date_filter,
            on_reset=self.reset_filter
        )

        # File selection
        self.file_picker = ft.FilePicker(on_result=self.load_file)
        self.page.overlay.append(self.file_picker)
    def update_counter(self,value):
        self.counter.controls[1].value = value
        self.counter.update()
    def on_page_resize(self, e):
        self.page.update()

    def init_ui(self):
        content_area = ft.Column(
            controls=[
                ft.Row(controls=[
                    ft.Text(
                        "HTTP LOG BROWSER",
                        color=ft.Colors.BLACK87,
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    self.counter
                ]),

                ft.ElevatedButton(
                    "CHOOSE FILE",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["log"]),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    color=ft.Colors.BLUE

                ),
                self.list_view.get_container(),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            *self.date_filter.get_container().content.controls,
                            *self.list_view.get_navigation_buttons(),

                        ],

                        wrap=True
                    ),
                    expand=True,
                    bgcolor=ft.Colors.BLUE_50,
                ),
                self.detail_panel.get_container()
            ],
            expand=True,
            spacing=10
        )

        self.page.add(ft.Column(controls=[
            content_area,
            self.error_display.get_container()
        ],
            expand=True,
            spacing=10))
        self.page.update()


    def load_file(self, e):
        self.error_display.clear()
        self.update_counter(0)
        if not e.files:
            return

        file_path = e.files[0].path
        load_result = self.log_reader.load_file(file_path)

        if not load_result.success():
            self.error_display.show(load_result.get_error())
            self.disable_all_controls()
            self.detail_panel.clear()
            return

        display_result = self.log_reader.display_logs()
        if not display_result.success():
            self.error_display.show(display_result.get_error())
            self.current_logs = []
            self.list_view.update_list([])
            self.disable_all_controls()
            self.detail_panel.clear()
            self.update_counter(0)

            return

        self.date_filter.reset_dates()
        self.detail_panel.clear()
        self.backup_logs = display_result.get_value()
        self.current_logs = display_result.get_value()

        self.list_view.update_list(self.current_logs)
        self.list_view.init_selecting()

        self.date_filter.enable_start_date()
        self.date_filter.enable_end_date()
        self.date_filter.disable_apply()
        self.date_filter.disable_reset()
        self.update_counter(len(self.current_logs))

    def on_log_selected(self, index: int):
        if 0 <= index < len(self.current_logs):
            self.detail_panel.update_from_log(self.current_logs[index])

    def apply_date_filter(self, e):
        self.date_filter.enable_reset()
        try:
            date_range = self.date_filter.get_date_range()
            filter_result = self.log_reader.sort_by(
                (Conditions.INTERVAL,),
                date_range,
                self.current_logs
            )

            if not filter_result.success():
                self.error_display.show(filter_result.get_error())
                self.disable_all_controls()
                self.list_view.update_list([])
                self.detail_panel.clear()
                self.date_filter.enable_reset()
                self.update_counter(0)
                return

            self.error_display.clear()
            self.backup_logs = self.current_logs
            self.current_logs = filter_result.get_value()
            self.list_view.update_list(self.current_logs)
            self.update_counter(len(self.current_logs))
            self.list_view.init_selecting()

            self.date_filter.disable_start_date()
            self.date_filter.disable_end_date()
            self.date_filter.disable_apply()
            self.date_filter.enable_reset()

        except Exception as e:
            self.error_display.show(f"Error applying filter: {str(e)}")

    def reset_filter(self, e):
        self.error_display.clear()
        self.date_filter.reset_dates()

        self.current_logs = self.backup_logs
        self.list_view.update_list(self.current_logs)

        self.date_filter.disable_reset()
        self.date_filter.enable_start_date()
        self.date_filter.enable_end_date()
        self.list_view.enable_next()
        self.list_view.enable_prev()

        self.list_view.init_selecting()

    def disable_all_controls(self):
        self.date_filter.disable_start_date()
        self.date_filter.disable_end_date()
        self.date_filter.disable_apply()
        self.date_filter.disable_reset()
        self.list_view.disable_next()
        self.list_view.disable_prev()


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"

    app = LogReaderApp(page)
    app.init_ui()


if __name__ == "__main__":
    ft.app(target=main)