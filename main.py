import os
import json
import app.constants as constants
from app.lib.phew import logging, is_connected_to_wifi, connect_to_wifi
from app.ota_updater import OTAUpdater

configs = {}
version = "0.0.0"

try:
    os.stat(constants.CONFIGS_FILE)

    # File was found, attempt to connect to wifi...
    with open(constants.CONFIGS_FILE) as f:
        configs = json.load(f)
        f.close()

    with open(constants.VERSION_FILE) as f:
        version = f.readline()
        f.close()

except Exception:
    configs = {}

logging.info(f"Firmware version: {version}")

wifi_current_attempt = 1
while wifi_current_attempt <= constants.WIFI_MAX_ATTEMPTS:
    wifi = configs.get("wifi", {})
    ssid = wifi.get("ssid")
    wifi_password = wifi.get("password")
    print(f"Connecting to wifi, ssid {ssid}, attempt {wifi_current_attempt}")

    ip_address = connect_to_wifi(ssid, wifi_password)

    if is_connected_to_wifi():
        print(f"Connected to wifi, IP address {ip_address}")
        break
    else:
        wifi_current_attempt += 1


ota = OTAUpdater(constants.RELEASE_REPO)

latest_release = ota.get_latest_release()
latest_version = ota.get_latest_version(latest_release)
if ota.compare_versions(current_version=version, latest_version=latest_version):
    ota.download_release(latest_release)
