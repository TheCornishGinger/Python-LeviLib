from importlib.util import find_spec

def check_no_gui(force_change: bool, imports: list):
    return check(imports, False, force_change)

def check(lib_list: list, enable_gui = True, force_changes = False):    
    error_list = []
    for lib in lib_list:
        if find_spec(lib) == False and len(lib) > 0:
            error_list.append(lib)

    if len(error_list) > 0:
        error_msg = ""
        index = 0
        for e in error_list:
            index = index + 1
            if index < len(error_list):
                error_msg = error_msg + e + ", "
            else:
                error_msg = error_msg + e + "."

        from subprocess import run
        error_pip = ""
        try:
            run("pip --version")
        except:
            error_pip = "\n'Pip' the free python package manager is also not installed, and is required to install these packages."

        if enable_gui:
            from tkinter import messagebox, Tk
            Tk().withdraw()
            query = messagebox.askyesno("Missing package(s)", "The following packages are missing: " + error_msg + error_pip + "\nWould you like to install them automatically?")
            if not query:
                return False
        elif not force_changes:
            return False

        if error_pip != "":
            r = None
            try:
                from platform import system as os_check
                if os_check() == "Windows":
                    r = run("py -m ensurepip --upgrade")
                else:
                    r = run("python -m ensurepip --upgrade")
            except:
                if enable_gui:
                    messagebox.showerror("Pip installation error", "'Pip' the free python package manager could not be installed, install pip manually and try again.")
                return False
            if r.returncode != 0:
                if enable_gui:
                    messagebox.showerror("Pip installation error", "'PIP INSTALLATION ERROR " + r.returncode + ":\n" + r.stdout.decode("utf-8"))
                return False
            try:
                run("pip --version")
            except:
                if enable_gui:
                    messagebox.showerror("Pip installation error", "'Pip' the free python package manager was installed but cannot be accessed, try restarting your device or re-installing pip manually.")
                return False

        for e in error_list:
            r = None
            try:
                r = run("pip install " + e)
            except:
                if enable_gui:
                    messagebox.showerror("Installation error", "The package '" + e + "' could not be installed.\nTo manually install use 'pip install <package>'")
                return False
            if r.returncode != 0:
                if enable_gui:
                    messagebox.showerror("Installation error", "The package '" + e + "' could not be installed.\nTo manually install use 'pip install <package>'")
                return False
        
    return True