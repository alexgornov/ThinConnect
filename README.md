# ConfiConnect

Need freerdp2-x11, python3-tk

Create a config.yml file with content:

```
domain: "example.com"
config: "global config for freerdp" # "/cert-ignore /multimon" and more
servers:
  server1:
    name: "servername"
    ip: serverip
    extendedconfig: "extended config for freerdp" # "/load-balance-info" and more
  server(i):
    ...
    
```
