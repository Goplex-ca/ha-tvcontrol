# ha-tvcontrol
Home Assistant TV control scripts

These are a collection of home made scripts to control various TV in a restaurant through Home Assistant.

Sharp Aquos TVs
 - scripts/sharpaquos.py

 Based on: https://assets.sharpnecdisplays.us/documents/usermanuals/4p-bej2u_4w-bft5u_emanual.pdf

Samsung TVs
 - scripts/samsung.py

 Based on this info: https://groups.io/g/crestron/topic/samsung_ip_control/78332353
 
URayTech Multicast Decoder
 - script/uraytech_*

Usage:

configuration.yaml
```
shell_command:
  tv_sharpaquos: python scripts/sharpaquos.py -H "{{ host }}" -c "{{ command }}"
  tv_samsung: python scripts/samsung.py -H "{{ host }}" -c "{{ command }}"
  tv_mcast_decoder_channel: scripts/uray_channel_id.sh "{{ host }}" "{{ channel }}"
```

Lovelace button example
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
            host: 10.56.0.187
            command: hdmi2
        icon: mdi:television-box
        entity: binary_sensor.10_56_0_214
```