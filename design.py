import tkinter
import customtkinter
import json


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

DEFAULT_SETTINGS = {"Command": {"description": "This tool allows you to run commands on a remote server and see the output from the remote server",
                                "warnings": ""}}

try:
    with open("settings.json") as f:
        SETTINGS = json.load(f)
except FileNotFoundError:
    with open("settings.json", "w+") as f:
        json.dump(DEFAULT_SETTINGS, f)
        SETTINGS = DEFAULT_SETTINGS


# Custom CTk Frames
class commandFrame(customtkinter.CTkFrame):
    def __init__(self, *args, headerName="",  **kwargs):
        super().__init__(*args, **kwargs)

        self.headerName = headerName

        self.frameTitle = customtkinter.CTkLabel(self, text=self.headerName, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frameTitle.grid(row=0, column=0)

        self.description = SETTINGS["Command"]["description"]
        print(self.description)


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("PyRemote")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar
        self.sidebarFrame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(4, weight=1)

        # Sidebar Labels and Buttons
        self.sidebarHeader = customtkinter.CTkLabel(self.sidebarFrame, text="Hello", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sidebarHeader.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.commandButton = customtkinter.CTkButton(self.sidebarFrame, text="Run Command", command=self.switchLayoutCommand)
        self.commandButton.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebarFrame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebarFrame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Create main frame
        self.mainFrame = commandFrame(self, headerName="Run Commands")
        self.mainFrame.grid(row=0, column=1, padx=20, pady=20)

        self.mainFrameButton = customtkinter.CTkButton(self, text="Print value of frame 2")
        self.mainFrameButton.grid(row=1, column=1, padx=20, pady=10)

    def switchLayoutCommand(self) -> None:
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
