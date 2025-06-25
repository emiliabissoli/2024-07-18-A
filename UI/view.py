import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP 2024 - Esame del 18/07/2024 - A"
        self._page.horizontal_alignment = 'CENTER'
        self._page.window_width = 1200
        self._page.window_height = 900
        #self._page.window_center()
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # title
        self._title = None
        # first row
        self.dd_min_ch: ft.Dropdown = None
        self.dd_max_ch: ft.Dropdown = None
        self.dd_localization: ft.Dropdown = None
        self.btn_graph: ft.ElevatedButton = None
        self.btn_dettagli: ft.ElevatedButton = None
        self.btn_path: ft.ElevatedButton = None
        # second row
        self.txt_result1: ft.ListView = None  # Qui scrivere gli outputs del punto 1
        self.txt_result2: ft.ListView = None  # Qui scrivere gli outputs del punto 2

    def load_interface(self):
        # title
        self._title = ft.Text("TdP 2024 - Esame del 18-07-2024 - A", color="blue", size=24)
        self._page.controls.append(self._title)

        # First row with some controls
        self.dd_min_ch = ft.Dropdown(label="Cromosoma min",
                               hint_text="Selezionare il valore minimo di cromosoma.", width=200)
        self._controller.fillDDMin()

        self.dd_max_ch = ft.Dropdown(label="Cromosoma max",
                               hint_text="Selezionare il valore massimo di cromosoma.", width=200)
        self._controller.fillDDMax()

        self.btn_graph = ft.ElevatedButton(text="Crea Grafo",
                                           tooltip="Crea il grafo",
                                           on_click=self._controller.handle_graph)

        self.dd_localization = ft.Dropdown(label="Localization",
                                      hint_text="Selezionare la Localization del gene", width=200)
        self._controller.fillDDLocalization()

        self.btn_dettagli = ft.ElevatedButton(text="Dettagli",
                                              tooltip="Stampa dettagli del grafo",
                                              on_click=self._controller.handle_dettagli)

        self.btn_path = ft.ElevatedButton(text="Cammino",
                                          tooltip="Trova cammino ottimo",
                                          on_click=self._controller.handle_path)

        row1 = ft.Row([self.dd_min_ch, self.dd_max_ch, self.btn_graph, self.dd_localization,
                       self.btn_dettagli, self.btn_path],
                      alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        self._page.controls.append(row1)

        # List View where the reply is printed
        self.txt_result1 = ft.ListView(width=400, expand=1, spacing=10, padding=20, auto_scroll=False)
        self.txt_result2 = ft.ListView(width=400, expand=1, spacing=10, padding=20, auto_scroll=False)
        self.txt_result1.controls.append(ft.Text("Risultati punto1"))
        self.txt_result2.controls.append(ft.Text("Risultati punto2"))

        container1 = ft.Container(
            content=self.txt_result1,
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.GREY_200,
            width=450,
            height=700,
            border_radius=10,
        )
        container2 = ft.Container(
            content=self.txt_result2,
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.GREY_200,
            width=450,
            height=700,
            border_radius=10,
        )

        row2 = ft.Row([container1, container2],
                      alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                      spacing=50)
        self._page.controls.append(row2)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()