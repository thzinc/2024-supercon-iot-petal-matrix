def do_connect():
    import network
    import constants as constants

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(constants.WIFI_SSID, constants.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print("network config:", sta_if.ipconfig("addr4"))


# do_connect()
print("boot")
