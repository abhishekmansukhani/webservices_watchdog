
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "webservices_watchdog.bat" & chr(34), 0
Set WshShell = Nothing
