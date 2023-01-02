import threading
import tkinter
import customtkinter
from typing import Callable
from PIL import Image
import io
import time
import os

MAINFOLDER = "PyRemoteClient/"

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

layouts = []


# Global Functions
def Invoke(func: Callable, delay: float):
    start = threading.Timer(delay, func)
    start.start()


# Custom CTk Frames

class Popups:
    @staticmethod
    def savedLogs(root: customtkinter.CTk, saveDirectory:str = "PyRemoteClient/logs", geometry: str ="450x200"):
        def closeWindow():
            window.destroy()
            window.update()

        Invoke(closeWindow, 3)

        window: customtkinter.CTkToplevel = customtkinter.CTkToplevel(root)
        #window.geometry(geometry)
        window.title("Log(s) saved!")
        window.resizable(False, False)

        title = customtkinter.CTkLabel(window, text=f"File(s) Saved to: {saveDirectory}", font=customtkinter.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, padx=20, pady=10)

        quitButton = customtkinter.CTkButton(window, text="Exit", command=closeWindow)
        quitButton.grid(row=1, column=0, padx=20, pady=10)


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

        self.description = "This tool allows you to run commands on a remote server and see the output"
        self.descriptionLabel = customtkinter.CTkLabel(self, text=self.description, font=customtkinter.CTkFont(size=15))
        self.descriptionLabel.grid(row=1, column=1, padx=(200, 0))

        self.outputBox = customtkinter.CTkTextbox(self, state="disabled")
        self.outputBox.grid(row=2, column=1, sticky="nsew", padx=(20, 0))
        self.outputBox.insert("0.0", "No Output...")

        self.commandTextVariable = ""
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
        self.screenshot = customtkinter.CTkImage(light_image=Image.open("PyRemoteClient/images/placeholder.png"),
                                                 dark_image=Image.open("PyRemoteClient/images/placeholder.png"),
                                                 size=(400, 200))
        self.screenshotContainerLabel = customtkinter.CTkLabel(self, image=self.screenshot, text="")
        self.screenshotContainerLabel.grid(row=0, column=0)

        self.takeScreenshot = customtkinter.CTkButton(self, text="Take Screenshot", command=ontakeScreenshot)
        self.takeScreenshot.grid(row=1, column=0)


class cameraFrame(Frame):
    def __init__(self, *args, onCapture: Callable, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="transparent")
        self.capture = customtkinter.CTkImage(light_image=Image.open("PyRemoteClient/images/placeholder.png"),
                                              dark_image=Image.open("PyRemoteClient/images/placeholder.png"),
                                              size=(400, 200))
        self.captureContainerLabel = customtkinter.CTkLabel(self, image=self.capture, text="")
        self.captureContainerLabel.grid(row=0, column=0)

        self.takeCapture = customtkinter.CTkButton(self, text="Take Camera Capture", command=onCapture)
        self.takeCapture.grid(row=1, column=0)


# The Admin frame is not one frame
# It consists of multiple frames
class keyloggerFrame(Frame):
    def __init__(self, *args, keyloggerFunc: Callable, getoutput: Callable, **kwargs):
        super().__init__(*args, **kwargs)
        # Tools available - Keylogger, download software, disable self

        self.Title = customtkinter.CTkLabel(self, text="Keylogger Settings", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.Title.grid(row=0, column=0, padx=20, pady=10)
        # self.keyloggerOutput = customtkinter.CTkTextbox(self)
        # self.keyloggerOutput.grid(row=1, column=0, padx=20)

        self.keyloggerToggle = customtkinter.CTkButton(self, text="Enable Keylogger", command=keyloggerFunc)
        self.keyloggerToggle.grid(row=1, column=0, padx=10, pady=10)

        self.getOutput = customtkinter.CTkButton(self, text="Get Logs", command=getoutput)
        self.getOutput.grid(row=2, column=0, padx=10, pady=10)


class softwareDownloaderFrame(Frame):
    def __init__(self, *args, downloadSoftware: Callable, deploySoftware: Callable, **kwargs):
        super().__init__(*args, **kwargs)
        self.Title = customtkinter.CTkLabel(self, text="Download \"Software\"", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.Title.grid(row=0, column=0, padx=(200, 20))

        self.url = customtkinter.CTkEntry(self, placeholder_text="https://example.com")
        self.url.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.downloadButton = customtkinter.CTkButton(self, text="Download Files", command=downloadSoftware)
        self.downloadButton.grid(row=3, column=3, padx=(0, 20))

        self.runargs = customtkinter.CTkEntry(self, placeholder_text="Run Command")
        self.runargs.grid(row=4, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.deployButton = customtkinter.CTkButton(self, text="Deploy Software", command=deploySoftware)
        self.deployButton.grid(row=4, column=3, padx=(0, 20))


# Main Application Class
class App(customtkinter.CTk):
    def __init__(self, client) -> None:
        super().__init__()

        self.client = client

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

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebarFrame, text="Admin Controls", command=self.switchLayoutAdmin)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Create main frame
        self.mainFrame = commandFrame(self, headerName="Run Commands", onsubmit=self.sendCommand)
        self.mainFrame.grid(row=0, column=1, padx=20, pady=20)

        # Create Screenshot frame and Camera Capture Frame
        self.ssFrame = screenshotFrame(self, ontakeScreenshot=self.takeScreenshot)
        # self.ssFrame.grid(row=0, column=1, padx=20, pady=20)
        self.cameraCaptureFrame = cameraFrame(self, onCapture=self.takeCapture)
        self.adminFrame = keyloggerFrame(self, keyloggerFunc=self.keyloggerDeployWrapper, getoutput=self.getKeyloggerOutputWrapper)
        self.downloaderFrame = softwareDownloaderFrame(self, downloadSoftware=self.downloadSoftwareWrapper, deploySoftware=self.deploySoftwareWrapper)


    # Going to start a new connection every time
    # One thread will remain open for other connection stuff
    def sendCommand(self):
        print(self.mainFrame.commandEntry.get())
        output = self.client.command(cmd=self.mainFrame.commandEntry.get())
        self.mainFrame.outputBox.configure(state="normal")
        self.mainFrame.outputBox.insert("0.0", output)

    def switchLayoutCommand(self) -> None:
        self.clearLayout()
        self.mainFrame.grid(row=0, column=1, padx=20, pady=20)

    def switchLayoutScreenshot(self):
        self.clearLayout()
        self.ssFrame.grid(row=0, column=1, padx=20, pady=20)
        self.cameraCaptureFrame.grid(row=0, column=2, padx=20, pady=20)

    def switchLayoutAdmin(self):
        self.clearLayout()
        self.adminFrame.grid(row=0, column=1, padx=20)
        self.downloaderFrame.grid(row=1, column=1, padx=20)

    def clearLayout(self):
        for layout in layouts:
            layout.grid_forget()

    def takeScreenshot(self):
        self.client.screenshot()
        bytesScreenshot = self.client.screenshot()
        pilscreenshot: Image = Image.open(io.BytesIO(bytesScreenshot))
        try:
            os.mkdir(f"{MAINFOLDER}Screenshots")
        except FileExistsError:
            print()
        pilscreenshot.save(f"{MAINFOLDER}Screenshots/{time.strftime('%d-%m-%Y')}.png")
        pilscreenshot = pilscreenshot.resize((400, 200))
        self.ssFrame.screenshot.configure(dark_image=pilscreenshot, light_image=pilscreenshot)

    def takeCapture(self):
        self.client.capture()
        bytesCapture = self.client.capture()
        pilCapture = Image.open(io.BytesIO(bytesCapture))
        try:
            os.mkdir(f"{MAINFOLDER}Captures")
        except FileExistsError:
            print()
        pilCapture.save(f"{MAINFOLDER}Captures/{time.strftime('%d-%m-%Y')}.png")
        pilCapture = pilCapture.resize((400, 200))
        self.cameraCaptureFrame.capture.configure(dark_image=pilCapture, light_image=pilCapture)

    """ Wrapper functions for admin tools to allow passthrough of arguements """
    def keyloggerDeployWrapper(self):
        self.client.deployKeylogger()

    def getKeyloggerOutputWrapper(self) -> None:
        Popups.savedLogs(self)
        return self.client.getKeyloggerOutput()
    def downloadSoftwareWrapper(self):
        self.client.downloadSoftware(self.downloaderFrame.url.get())

    def deploySoftwareWrapper(self):
        self.client.deploySoftware(self.downloaderFrame.runargs.get())

    """ END WRAPPERS"""


if __name__ == "__main__":
    app = App()
    app.mainloop()
