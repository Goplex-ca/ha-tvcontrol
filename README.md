# ha-tvcontrol
## Home Assistant TV control scripts

These are a collection of home made scripts to control various TV in a restaurant through Home Assistant.  It can obviousely be used standalone or by any other tools that can trigger scripts.

### Sharp Aquos TVs
Based on the manual: 
 https://assets.sharpnecdisplays.us/documents/usermanuals/4p-bej2u_4w-bft5u_emanual.pdf

- `scripts/sharpaquos.py`
-  Requires `pexpect` python module


### Samsung TVs
Based on this info:
 https://groups.io/g/crestron/topic/samsung_ip_control/78332353

- `scripts/samsung.py`
- Requires `pexpect` python module

 
### URayTech Multicast Decoder
- `script/uraytech.py`
- Requires `requests` python module

## Usage in Home Assistant:

Define the shell commands in `configuration.yaml`:
```
shell_command:
  tv_sharpaquos: python scripts/sharpaquos.py -H "{{ host }}" -c "{{ command }}"
  tv_samsung: python scripts/samsung.py -H "{{ host }}" -c "{{ command }}"
  tv_uraytech: python scripts/uraytech.py -H "{{ host }}" -c "{{ command }}"
```

Lovelace button example:
```
      - show_name: true
        show_icon: true
        type: button
        name:
          - type: text
            text: TV
          - type: text
            text: HDMI2
        icon_height: 25px
        tap_action:
          action: call-service
          service: shell_command.tv_sharpaquos
          service_data:
            host: x.x.x.x
            command: hdmi2
        icon: mdi:television-box
        entity: binary_sensor.x_x_x_x
```