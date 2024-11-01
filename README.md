# IoT Petal Matrix for the 2024 Hackaday Supercon 8 badge

Demo to show using MQTT to communicate between a web interface and the Raspberry Pi Pico W running on the Supercon 8 badge with the Petal Matrix SAO

## Quickstart

1. Copy the contents of [`badge`](./badge/) to the Pico.
2. Update [`constants.py`](./badge/constants.py) as is relevant
   - Set the `WIFI_SSID` and `WIFI_PASSWORD` to connect to your wifi network
   - (Optional) If you want to use a different MQTT broker, set `MQTT_HOST` as you see fit
   - Set the `DEVICE_ID` to something unique (play nice if you're using a public MQTT broker)
3. Go to https://thzinc.com/2024-supercon-iot-petal-matrix/ and click the button next to "Device" and type in the name you used for `DEVICE_ID`

## Building

## Code of Conduct

We are committed to fostering an open and welcoming environment. Please read our [code of conduct](CODE_OF_CONDUCT.md) before participating in or contributing to this project.

## Contributing

We welcome contributions and collaboration on this project. Please read our [contributor's guide](CONTRIBUTING.md) to understand how best to work with us.

## License and Authors

[![Daniel James logo](https://secure.gravatar.com/avatar/645145afc5c0bc24ba24c3d86228ad39?size=16) Daniel James](https://thzinc.com)

[![license](https://img.shields.io/github/license/thzinc/2024-supercon-iot-petal-matrix.svg)](https://github.com/thzinc/2024-supercon-iot-petal-matrix/blob/master/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/thzinc/2024-supercon-iot-petal-matrix.svg)](https://github.com/thzinc/2024-supercon-iot-petal-matrix/graphs/contributors)

This software is made available by Daniel James under the MIT license.
