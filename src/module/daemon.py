import json
@asynchronous
def module_init():
    busdir = "/var/lib/lightdm/"
    if os.path.exists("/{}/pardus-greeter".format(busdir)):
        os.unlink("/{}/pardus-greeter".format(busdir))
    if not get("enabled",True,"daemon"):
        return
    debug("Entering daemon loop")
    while True:
        debug("Creating fifo")
        os.mkfifo("/{}/pardus-greeter".format(busdir))
        try:
            debug("Listening fifo")
            with open("/{}/pardus-greeter".format(busdir),"r") as f:
                username=""
                password=""
                debug("Reading fifo")
                data=json.loads(f.read())
                debug("fifo data: {}".format(str(data)))
                os.unlink("/{}/pardus-greeter".format(busdir))
                debug("Removing fifo after read")
                if "message" in data:
                    lightdm.msg_handler(str(data["message"]))
                    continue
                if "username" in data:
                    username=str(data["username"])
                if "password" in data:
                    password = str(data["password"])
                if "session" in data:
                    lightdm.set(session = str(data["session"]))
                #myedit line 32-39
                loginwindow.o("ui_entry_search_user").set_text("")
                loginwindow.o("ui_popover_userlist").popdown()
                loginwindow.o("ui_stack_username").set_visible_child_name("show")
                loginwindow.o("ui_entry_username").set_text(username)
                loginwindow.o("ui_entry_password").grab_focus()
                loginwindow.update_username_button(username)
                #GLib.idle_add(loginwindow.o("ui_entry_username").set_text, username)
                GLib.idle_add(loginwindow.o("ui_entry_password").set_text, password)
                GLib.idle_add(loginwindow.event_login_button, loginwindow.o("ui_button_login"))
                lightdm.login()
                debug("daemon login done")
        except Exception as e:
           debug("Removing fifo")
           if os.path.exists("/{}/pardus-greeter".format(busdir)):
               os.unlink("/{}/pardus-greeter".format(busdir))
               debug("Removing fifo done")
           print(traceback.format_exc(), file=sys.stderr)
