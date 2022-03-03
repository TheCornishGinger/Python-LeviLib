import os
from datetime import datetime

try:
    from . import lib_check
except ImportError:
    try:
        import lib_check
    except ImportError:
        print("FATAL: Can't find 'logger.py' dependency.")
        exit()

__lib_found__ = lib_check.check_no_gui(False, ["tkinter"])
if __lib_found__:
    from tkinter import messagebox, Tk

class Log:
    def __init__(self, identity: str, file_path = "default", write_to_file = True, include_date = True, include_time = True, show_warning = False, show_error = True):
        """
        identity -> Shown when logging to help identify this instance.\n
        file_path -> Path of the log file (do not include the file name.)\n
        write_to_file -> Enable/disable writing to the log file.\n
        include_date -> Enable/disable inclduing the date.\n
        include_time -> Enable/disable inclduing the time.\n
        show_warning -> Enable/disable gui warning box. (uses tkinter).\n
        show_error -> Enable/disable gui error box. (uses tkinter).
        """
        if write_to_file:
            if file_path == "default":
                self.__file_path__ = os.path.join(os.curdir, "log.txt")
            else:
                if os.path.exists(self.__file_path__):
                    self.__file_path__ = file_path
                else:
                    self.__file_path__ = None
                    self.__err__("Can't find given file path, writing to file has been disabled.'")
        else:
            self.__file_path__ = None

        self.__cache__ = []
        self.__ID__ = identity
        self.__inc_date__ = include_date
        self.__inc_time__ = include_time
        self.__show_warning__ = show_warning
        self.__show_error__ = show_error
        if show_warning or show_error:
            if __lib_found__:
                tk = Tk()
                tk.withdraw()
            else:
                self.__show_warning__ = False
                self.__show_error__ = False
                self.__err__("Could not import the tkinter module, gui disabled.")


    def __build_prefix__(self, msg_title: str, overwrite_id = None):
        "Builds a prefix string for log messages, overwriting the log ID is optional."
        if overwrite_id is None:
            overwrite_id = self.__ID__
        layout = ""
        if self.__inc_date__:
            layout = layout + "[ %D ]"
        if self.__inc_time__:
            layout = layout + "[ %H:%M:%S ]"
        return datetime.now().strftime(layout) + "[ " + overwrite_id.upper() + " ]" + "[ " + msg_title.upper() + " ] "


    def __verify_file__(self):
        "Checks for the log file and creates it if necessary."
        if not os.path.exists(self.__file_path__):
            try: 
                open(self.__file_path__, mode="x").close()
            except IOError:
                temp = self.__file_path__
                self.__file_path__ = None
                self.__err__("Error creating '" + temp + "', writing to file disabled.")
                return False
        return True


    def __log__(self, msg: str):
        "Write a message to the log file and cache."
        self.__cache__.append(msg)
        print(msg)

        if self.__file_path__ == None:
            return False

        if self.__verify_file__():
            try:
                f = open(self.__file_path__, mode="r", encoding="utf-8")
                data = f.read()
                f.close()
                f = open(self.__file_path__, mode="w", encoding="utf-8")
                if len(data.split("\n")) == 0:
                    f.write(msg)
                else:
                    f.write(data + "\n" + msg)
                f.close()
            except IOError:
                temp = self.__file_path__
                self.__file_path__ = None
                self.__err__("Error editing '" + temp + "', writing to file disabled.")
                return False
        else:
            return False
        return True


    def get_path(self):
        "Returns path of the log file, including the filename."
        return self.__file_path__


    def get_last_log(self):
        "Returns the last log message as a string."
        return self.__cache__[len(self.__cache__) - 1]


    def __err__(self, msg: str):
        "Log an internal error."
        if self.__show_error__:
            messagebox.showerror("Internal Error", "INTERNAL ERROR\n\n" + msg)
        return self.__log__(self.__build_prefix__("fatal", "internal") + msg)
    
    def info(self, msg: str):
        "Log a general message."
        return self.__log__(self.__build_prefix__("info") + msg)

    def warn(self, msg: str):
        "Log a warning message."
        if self.__show_warning__:
            messagebox.showwarning("Warning - " + self.__ID__[0].upper() + self.__ID__[1:len(self.__ID__)].lower(), "WARNING\n\n" + msg)
        return self.__log__(self.__build_prefix__("warn") + msg)

    def error(self, msg: str):
        "Log an error message."
        if self.__show_error__:
            messagebox.showerror("Error - " + self.__ID__[0].upper() + self.__ID__[1:len(self.__ID__)].lower(), "ERROR\n\n" + msg)
        return self.__log__(self.__build_prefix__("error") + msg)

    def fatal(self, msg: str):
        "Log a fatal message."
        if self.__gui_enabled__:
            messagebox.showerror("Fatal - " + self.__ID__[0].upper() + self.__ID__[1:len(self.__ID__)].lower(), "FATAL\n\n" + msg)
        return self.__log__(self.__build_prefix__("fatal") + msg)