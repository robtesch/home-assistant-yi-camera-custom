# yi-hack Home Assistant custom on/off integration

This is a custom integration designed to work with yi-hack cameras:

- https://github.com/TheCrypt0/yi-hack-v4 and previous
- https://github.com/roleoroleo/yi-hack-MStar
- https://github.com/roleoroleo/yi-hack-Allwinner
- https://github.com/roleoroleo/yi-hack-Allwinner-v2

The official HA integration (from the author of yi-hack) can be found here:
- https://github.com/roleoroleo/yi-hack_ha_integration

While this is an amazing integration, and offers a lot of functionality, it does not allow you to "turn off" the camera or turn it back on again.

This very basic integration connects directly to the yi_hack cam UI and changes the setting that can be found on the "camera settings" page allowing you to turn on/off the camera.
This can be useful for home/away routines, where perhaps you want to turn off the cameras while someone is home, and turn them on again as soon as the house is empty.

## Installation

Recomended way:

1. Install from HACS, add this repository as custom repository
2. Search into HACS store the yi hack custom and install
3. Full restart of home assistant is recomended

"Manual" way:

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `yi_hack_custom`.
4. Download _all_ the files from the `custom_components/yi_hack_custom/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant

## Configuration is done in YAML

example configuration.yaml entry:

```yaml
switch:
 - platform: yi_camera_custom
   friendly_name: "Yi Camera Lounge"
   ip_address: 192.168.0.1
   username: !secret yi_username
   password: !secret yi_pass
   
 - platform: yi_camera_custom
   friendly_name: "Yi Camera Kitchen"
   ip_address: 192.168.0.2
   username: !secret yi_username
   password: !secret yi_pass
```

Note that the username and password are the ones that you have set up in yi_hack camera UI, and is specific to each camera.
If you have not set up a username and password for your cameras, it is strongly recomended to do so.
If you do not wish to set up a username and password for your cameras, you will still need to provide values for them for this integration to work. These can be dummy values.

Example for camera without username and password:

```yaml
switch:
 - platform: yi_camera_custom
   friendly_name: "Yi Camera Lounge"
   ip_address: 192.168.0.1
   username: random_string
   password: random_string
```