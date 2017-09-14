qndRDP
===
I needed a very quick way to give users a
simple method of connecting to a Windows RDP server.
Remmina was off the table for various reasons.
This is a mere wrapper around yad and xfreerdp.
As a consequence, they have to be available in $PATH.

### Config
Example for _~/.config/rdpgui/config.json_:
```
{"rdpdomain":"foo", "rdphost":"bar"}
```

### FreeRDP Options
See https://github.com/FreeRDP/FreeRDP/issues/1612
and https://github.com/FreeRDP/FreeRDP/issues/3003
for interesting discussion about options.
Maybe switch on "/sec:rdp" because of expired passwords.

### Known Problems
RDP password is visible via process table.
I assume local users on the client-side to be trusted.

yad field labels are in german.
