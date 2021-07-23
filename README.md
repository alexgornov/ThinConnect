# ThinConnect

Create a config.yml file with content:

```
domain: "example.com"
config: {"/cert-ignore", "/usb:auto", "/multimon", "/audio-mode:0","/microphone:sys:alsa,format:1,rate:44100", "/sound:sys:alsa", "/printer"} #global config for freerdp
servers:
  server1:
    name: "servername"
    ip: serverip
    extendedconfig: { "/load-balance-info:tsv://MS\ Terminal\ Services\ Plugin.1.RDP", "/f" } # extended config for freerdp
  server(i):
    ...
    
```
