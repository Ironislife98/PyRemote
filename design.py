import tkinter
import customtkinter
import json
from typing import Callable
from PIL import Image


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

DEFAULT_SETTINGS = {"Command": {
    "description": "This tool allows you to run commands on a remote server and see the output from the remote server",
    "warnings": ""}}

layouts = []

try:
    with open("settings.json") as f:
        SETTINGS = json.load(f)
except FileNotFoundError:
    with open("settings.json", "w+") as f:
        json.dump(DEFAULT_SETTINGS, f)
        SETTINGS = DEFAULT_SETTINGS


# Custom CTk Frames
class Frame(customtkinter.CTkFrame):    # Just here to avoid repeating adding layouts
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        layouts.append(self)


class commandFrame(Frame):
    def __init__(self, *args, headerName="", onsubmit: Callable, **kwargs):
        super().__init__(*args, **kwargs)

        self.headerName = headerName

        self.frameTitle = customtkinter.CTkLabel(self, text=self.headerName,
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frameTitle.grid(row=0, column=1, padx=(200, 0))

        self.description = SETTINGS["Command"]["description"]
        self.descriptionLabel = customtkinter.CTkLabel(self, text=self.description, font=customtkinter.CTkFont(size=15))
        self.descriptionLabel.grid(row=1, column=1, padx=(200, 0))

        self.outputBox = customtkinter.CTkTextbox(self, state="disabled")
        self.outputBox.grid(row=2, column=1, sticky="nsew", padx=(20, 0))
        self.outputBox.insert("0.0", "No Output...")

        self.commandEntry = customtkinter.CTkEntry(self, placeholder_text="Enter Command")
        self.commandEntry.grid(row=3, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.runCommandButton = customtkinter.CTkButton(master=self, text="Run Command", fg_color="transparent",
                                                        border_width=2,
                                                        text_color=("gray10", "#DCE4EE"), command=onsubmit)
        self.runCommandButton.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


class screenshotFrame(Frame):
    def __init__(self, *args, ontakeScreenshot: Callable, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="transparent")
        self.screenshot = customtkinter.CTkImage(light_image=Image.open("images/placeholder.png"),
                                          dark_image=Image.open("images/placeholder.png"),
                                          size=(400, 200))
        self.screenshotContainerLabel = customtkinter.CTkLabel(self, image=self.screenshot, text="")
        self.screenshotContainerLabel.grid(row=0, column=0)

        self.takeScreenshot = customtkinter.CTkButton(self, text="Take Screenshot", command=ontakeScreenshot)
        self.takeScreenshot.grid(row=1, column=0)


class cameraFrame(Frame):
    def __init__(self, *args, onCapture: Callable, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="transparent")
        self.capture = customtkinter.CTkImage(light_image=Image.open("images/placeholder.png"),
                                          dark_image=Image.open("images/placeholder.png"),
                                          size=(400, 200))
        self.captureContainerLabel = customtkinter.CTkLabel(self, image=self.capture, text="")
        self.captureContainerLabel.grid(row=0, column=0)

        self.takeCapture = customtkinter.CTkButton(self, text="Take Camera Capture", command=onCapture)
        self.takeCapture.grid(row=1, column=0)


# Main Application Class
class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("PyRemote")
        self.geometry(f"{1100}x{580}")
        # self.resizable(False, False)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar
        self.sidebarFrame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(4, weight=1)

        # Sidebar Labels and Buttons
        self.sidebarHeader = customtkinter.CTkLabel(self.sidebarFrame, text="PyRemote",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sidebarHeader.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.commandButton = customtkinter.CTkButton(self.sidebarFrame, text="Run Command",
                                                     command=self.switchLayoutCommand)
        self.commandButton.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebarFrame, text="Screen Capture", command=self.switchLayoutScreenshot)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebarFrame, text="CameraCapture",
                                                        command=self.switchLayoutScreenshot)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebarFrame)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        # Create main frame
        self.mainFrame = commandFrame(self, headerName="Run Commands", onsubmit=self.sendCommand)
        self.mainFrame.grid(row=0, column=1, padx=20, pady=20)

        # Create Screenshot frame and Camera Capture Frame
        self.ssFrame = screenshotFrame(self, ontakeScreenshot=self.takeScreenshot)
        # self.ssFrame.grid(row=0, column=1, padx=20, pady=20)
        self.cameraCaptureFrame = cameraFrame(self, onCapture=self.takeCapture)

    # Going to start a new connection every time
    # One thread will remain open for other connection stuff
    def sendCommand(self):
        pass

    def switchLayoutCommand(self) -> None:
        self.clearLayout()
        self.mainFrame.grid(row=0, column=1, padx=20, pady=20)

    def switchLayoutScreenshot(self):
        self.clearLayout()
        self.ssFrame.grid(row=0, column=1, padx=20, pady=20)
        self.cameraCaptureFrame.grid(row=0, column=2, padx=20, pady=20)

    def clearLayout(self):
        for layout in layouts:
            layout.grid_forget()

    # Placeholder funcs
    def takeScreenshot(self):
        pass

    def takeCapture(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
