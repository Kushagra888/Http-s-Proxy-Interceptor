import tkinter
from Proxy import Proxy
from time import sleep


class GUI:
    def __init__(self, proxy: Proxy):
        self.proxy = proxy
        self.window = tkinter.Tk()

        self.applyDesign()

    def start(self):
        self.window.mainloop()

    def applyDesign(self):
        self.window.geometry("800x600")
        self.window.title("Python Proxy Server")

        # frame to hold the forward and drop buttons
        buttons_frame = tkinter.Frame(self.window)
        buttons_frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=5)

        # forward proxy to server button
        self.forwardButtonProxy2Server = tkinter.Button(
            buttons_frame,
            text="Forward to Server",
            padx=5,
            command=self.handleForwardProxy2Server,
            state="disabled",
        )

        # forward proxy to client button
        self.forwardButtonProxy2Client = tkinter.Button(
            buttons_frame,
            text="Forward to Client",
            padx=5,
            command=self.handleForwardProxy2Client,
            state="disabled",
        )

        # Drop button
        self.dropButton = tkinter.Button(
            buttons_frame,
            text="Drop",
            padx=5,
            command=self.handleDrop,
            state="disabled",
        )

        self.dropButton.pack(side=tkinter.RIGHT)
        self.forwardButtonProxy2Client.pack(side=tkinter.RIGHT)
        self.forwardButtonProxy2Server.pack(side=tkinter.RIGHT)

        # Create a frame for the text areas
        text_frame = tkinter.Frame(self.window)
        text_frame.pack(
            side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=10, pady=5
        )

        # Create and place the Request label and text area
        request_label = tkinter.Label(text_frame, text="Request")
        request_label.pack(side=tkinter.TOP, anchor="w")

        self.request_text = tkinter.Text(text_frame, height=10, width=50)
        self.request_text.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

        # Create and place the Response label and text area
        response_label = tkinter.Label(text_frame, text="Response")
        response_label.pack(side=tkinter.TOP, anchor="w", pady=(10, 0))

        self.response_text = tkinter.Text(text_frame, height=10, width=50)
        self.response_text.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    def handleForwardProxy2Server(self):
        request = self.request_text.get(1.0, tkinter.END)
        self.forwardButtonProxy2Server.config(state="disabled")
        self.dropButton.config(state="disabled")
        response = Proxy.getResponse(request)
        self.response_text.delete(1.0, tkinter.END)
        self.response_text.insert(1.0, response)
        self.forwardButtonProxy2Client.config(state="normal")
        self.dropButton.config(state="normal")

    def handleForwardProxy2Client(self):
        response = self.response_text.get(1.0, tkinter.END)
        with Proxy.PacketQueueLock:
            client = Proxy.PacketQueue.pop(0)
            client.send(response.encode("utf-8"))
            Proxy.terminateConnection(client)

        self.loadNewRequest()

    def handleDrop(self):
        self.response_text.delete(1.0, tkinter.END)
        self.request_text.delete(1.0, tkinter.END)

        with Proxy.PacketQueueLock:
            client = Proxy.PacketQueue.pop(0)
            Proxy.terminateConnection(client)

        self.loadNewRequest()

    def loadNewRequest(self):
        self.request_text.delete(1.0, tkinter.END)
        self.response_text.delete(1.0, tkinter.END)

        with Proxy.PacketQueueLock:
            self.forwardButtonProxy2Client.config(state="disabled")
            if len(Proxy.PacketQueue) == 0:
                self.forwardButtonProxy2Server.config(state="disabled")
                self.dropButton.config(state="disabled")
            else:
                client = Proxy.PacketQueue[0]
                try:
                    request = Proxy.getRequest(client)
                    self.forwardButtonProxy2Server.config(state="normal")
                    self.dropButton.config(state="normal")
                    self.request_text.insert(1.0, request)
                except:
                    self.forwardButtonProxy2Server.config(state="disabled")
                    self.dropButton.config(state="disabled")
                    Proxy.terminateConnection(client)
                    Proxy.PacketQueueLock.release()
                    self.loadNewRequest()
