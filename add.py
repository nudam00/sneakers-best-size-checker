import json


def get_settings(setting):
    # Gets setting from settings.json
    settings_file = open("input/settings.json")
    settings = json.load(settings_file)
    return settings[setting]


def get_size(name, size):
    # Converts sizes to EU
    json_file = open("converters/sizes.json")
    sizes = json.load(json_file)
    try:
        if "new balance" in name:
            return sizes["New_balance"][size]
        elif "adidas" in name:
            return sizes["Adidas"][size]
        elif "nike" in name or "jordan" in name:
            return sizes["Nike"][size]
        elif "ugg" in name:
            return sizes["UGG"][size]
        elif "asics" in name:
            return sizes["Asics"][size]
    except:
        return ""
