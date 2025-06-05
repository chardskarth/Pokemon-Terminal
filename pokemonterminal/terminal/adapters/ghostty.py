import os
import subprocess

from . import TerminalProvider as _TProv


class GhosttyProvider(_TProv):

    __new_line_pattern = 'background-image = {}'
    __sed_command_pattern = "sed -i 's|{}|{}|' {}"

    def is_compatible() -> bool:
        return "TERM_PROGRAM" in os.environ and os.environ.get("TERM_PROGRAM") == "ghostty"

    def __run_replacescript(stream):
        p = subprocess.Popen(["osascript"], stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        p.stdin.write(stream)
        p.communicate()
        p.stdin.close()

    def change_terminal(path: str):
        old_line = r'background-image = .*'
        new_line = GhosttyProvider.__new_line_pattern.format(path)
        sed_command = GhosttyProvider.__sed_command_pattern.format(
            old_line, new_line, "~/.config/ghostty/config"
        )
 
        result = subprocess.run(sed_command, shell=True, check=True, capture_output=True, text=True)

    def clear():
        old_line = r'background-image = .*'
        new_line = GhosttyProvider.__new_line_pattern.format("")
        sed_command = GhosttyProvider.__sed_command_pattern.format(
            old_line, new_line, "~/.config/ghostty/config"
        )
 
        result = subprocess.run(sed_command, shell=True, check=True, capture_output=True, text=True)

    def __str__():
        return "Ghostty"
