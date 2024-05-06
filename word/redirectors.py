import tkinter as tk
from tkinter.simpledialog import askstring
import H.Apps.word.form as form






class StdRedirector:
    def __init__(self, text_widget, tag):
        """Redirector for stderr and stdout"""
        self.text_widget = text_widget
        self.tag = tag

    def write(self, message):
        self.text_widget.insert(tk.END, message, (self.tag,))
        self.text_widget.see(tk.END)

    def flush(self):
        pass

class StdinRedirector:
    def __init__(self, text_widget:tk.Widget, tag):
        self.text_widget = text_widget
        self.tag = tag
        self.message=''

    def write(self, message):
        self.message=message
        self.text_widget.insert(tk.END,message,(self.tag,))
        self.text_widget.see(tk.END)

    def readline(self):
        rep=askstring('Input',self.message,parent=self.text_widget.master)
        return '' if rep == False else rep

    def flush(self):
        pass

