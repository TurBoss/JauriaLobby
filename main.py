#!/usr/bin/env python

"""
    Hey, this is GPLv3 and copyright 2016 TurBoss from Jauria-Studios
"""

from __future__ import division
from __future__ import print_function

from sys import argv

import os
import gi
import ast
import time

import socket

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk

from gi.repository.GdkPixbuf import Pixbuf, InterpType

from lobby_client import LobbyClient


class Lobby(object):

    def __init__(self, app):
        self.app = app

        self.client = LobbyClient()
        print("INIT LOBBY")

    def login(self):
        username = self.app.username_login.get_text()
        password = self.app.password_login.get_text()

        login_data = False

        if username is "":
            self.app.dialog_message.set_text("Empty username")
            dialog.show()
        elif password is "":
            self.app.dialog_message.set_text("Empty password")
            dialog.show()
        else:
            login_data = True

        if login_data:
            self.client.username = username
            self.client.password = password

            if self.client.connected:

                self.client.Run(100)
                self.app.notebook.set_current_page(1)

            elif msg == "SERVERDOWN":
                self.app.dialog_message.set_text("Server down")
                dialog.show()

    def register(self):
        if self.client.connected is False:
            username = self.username_register.get_text()
            password = self.password_register.get_text()
            password2 = self.password2_register.get_text()

            register_data = False

            if username is "":
                self.app.dialog_message.set_text("Empty username")
                dialog.show()

            elif password is "":
                self.app.dialog_message.set_text("Empty password")
                dialog.show()

            elif password2 is "":
                self.app.dialog_message.set_text("Retype password")
                dialog.show()

            else:
                register_data = True

            if register_data:
                self.client.username = username
                self.client.password = password
                self.client.password2 = password2

                """
                msg = self.app.client.register()

                if msg == "REGISTRATIONDENIED":
                    self.app.dialog_message.set_text("Register failed")
                elif msg == "SERVERDOWN":
                    self.app.dialog_message.set_text("Server Down")
                elif msg == "REGISTRATIONACCEPTED":
                    self.app.dialog_message.set_text("Now you can login")

                dialog.show()
                """

    def append_text_to_chat(self, widget, username, message):
        model = widget.get_model()

        model.append([username, message])

    # sets chat user lis names in the treestore
    def set_list_model(self, widget, data):

        model = widget.get_model()
        widget.set_model(None)
        model.clear()

        for x in data:
            model.append([x.username])

        widget.set_model(model)

class Handler(object):

    def __init__(self):

        self.lobby = Lobby(self)

        self.notebook = builder.get_object("notebook1")

        self.cellrenderer_chat_username = builder.get_object("cellrenderertext_chat_username")
        self.treeview_chat_users = builder.get_object("treeview_chat_users")

        self.treeview_chat_log = builder.get_object("treeview_chat_log")

        self.username_login = builder.get_object("entry_username_login")
        self.password_login = builder.get_object("entry_password_login")

        self.username_register = builder.get_object("entry_username_register")
        self.password_register = builder.get_object("entry_password_register")
        self.password2_register = builder.get_object("entry_password2_register")

        self.dialog_message = builder.get_object("label_dialog")

    def on_applicationwindow1_delete_event(self, *args):
        Gtk.main_quit(*args)

    def on_button_dialog_clicked(self, widget, data=None):
        dialog.hide()

    def on_button_login_clicked(self, widget, data=None):
        self.lobby.login()

    def on_button_register_clicked(self, widget, data=None):
        self.lobby.register()


builder = Gtk.Builder()
builder.add_from_file("gui.glade")

builder.connect_signals(Handler())


"""
style_provider = Gtk.CssProvider()

css = open(os.path.join("style.css"), 'rb')
css_data = css.read()
css.close()

style_provider.load_from_data(css_data)

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
"""

win = builder.get_object("applicationwindow1")
win.show_all()

dialog = builder.get_object("messagedialog1")

Gtk.main()