import os, lib_check
from datetime import datetime

class Log:
    def __init__(self, identity: str, file_name = "log.txt", write_to_file = True, include_date = True, include_time = True, display_warns = True, display_errors = True):
        "Create a new log instance."
        self.__ID__ = identity
        if write_to_file:
            self.file_name = file_name
        else:
            self.file_name = None
        self.inc_date = include_date
        self.inc_time = include_time
        self.__disp_warn__ = display_warns
        self.__disp_err__ = display_errors
        if display_warns or display_errors:
            r = lib_check.check_no_gui(False, ["tkinter"])
            if r:
                import tkinter
            else:
                self.__err__("Could not import tkinter")

    def __err__(self, msg: str, write_to_file = True):
        "Log an internal error."
        msg = self.__build_prefix__("fatal", "internal") + msg
        print(msg)
        if write_to_file:
            return self.__write_to_file__(msg)


    def __build_prefix__(self, msg_title: str, alt_id = None):
        "Builds a prefix string for log messages."
        if alt_id is None:
            alt_id = self.__ID__
        layout = ""
        if self.inc_date:
            layout = layout + "[ %D ]"
        if self.inc_time:
            layout = layout + "[ %H:%M:%S ]"
        return "[ " + alt_id.upper() + " ]" + datetime.now().strftime(layout) + "[ " + msg_title.upper() + " ] "


    def __write_to_file__(self, msg: str):
        "Write a message to the log file."
        if self.file_name == None:
            return False

        if not os.path.exists(os.getcwd()):
            try: 
                open(self.file_name, mode="x").close()
            except IOError:
                self.__err__("Error trying to create '" + self.file_name + "'", False)
                return False
        try:
            f = open(self.file_name, mode="r", encoding="utf-8")
            file_data = f.read()
            f.close()
            f = open(self.file_name, mode="w", encoding="utf-8")
            f.write(file_data + "\n" + msg)
            f.close()
        except IOError:
            self.__err__("Error trying to edit '" + self.file_name + "'", False)
            return False
        return True

    
    def info(self, msg: str):
        "Log a general message."
        msg = self.__build_prefix__("info") + msg
        print(msg)
        return self.__write_to_file__(msg)

    def warn(self, msg: str):
        "Log a warning message."
        msg = self.__build_prefix__("warn") + msg
        print(msg)
        return self.__write_to_file__(msg)

    def error(self, msg: str):
        "Log an error message."
        msg = self.__build_prefix__("error") + msg
        print(msg)
        return self.__write_to_file__(msg)

    def fatal(self, msg: str):
        "Log a fatal message."
        msg = self.__build_prefix__("fatal") + msg
        print(msg)
        return self.__write_to_file__(msg)

log = Log("logger", write_to_file=False)