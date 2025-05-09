import re
BLACKLIST = [ # Change at your own risk, or  the AI could cause irreversable damage to your computer.
    r"rm\s+-rf\s+/?",
    r":\(\)\s*{\s*:.*:.*&\s*};:",
    r"mkfs",
    r"dd\s+if=",
    r"shutdown",
    r"reboot",
    r"halt",
    r"poweroff",
    r"chmod\s+000",
    r"chown\s+.*nobody",
    r"mv\s+/bin",
    r"yes\s+>",
    r"eval\s+",
    r"(wget|curl).*\|.*sh",
    r"kill\s+-9\s+-1",
    r"pkill",
    r"mount\s+/dev",

    r"del\s+/f\s+/q",
    r"rd\s+/s\s+/q",
    r"format\s+c:",
    r"reg\s+delete",
    r"cipher\s+/w:",
    r"vssadmin",
    r"net\s+user.*\*",
    r"net\s+stop",
    r"taskkill",
    r"powershell\s+.*(remove|invoke)",
    r"bcdedit",
    r"echo\s+y\|cacls",
    r"echo\s+test"
]
def is_blocked(command):
    return any(re.search(p, command, re.IGNORECASE) for p in BLACKLIST)
