WIFI_SSID = "YOUR WIFI NETWORK NAME"            #WiFi network name
WIFI_PASSWORD = "YOUR WIFI NETWORK PASSWORD"    #WiFi network password

#Relay Configuration
PIN = 1234                                      #Pin number for the button trigger
ENABLE_RELAY_1 = True                           #Enable or disable Relay 1
ENABLE_RELAY_2 = True                           #Enable or disable Relay 2
RELAY_1_TIME_BUTTON_DISABLED = 12000            #The time in milliseconds to disable the button from futher clicks e.g. this should be the length of time for your garage door to open/close 
RELAY_2_TIME_BUTTON_DISABLED = 12000            # ^
RELAY_1_TIME_BETWEEN = 0.5                      #The time in seconds to wait between relay activations e.g. 'on' > 'time' > 'off'
RELAY_2_TIME_BETWEEN = 0.5                      # ^
RELAY_1_PIN = 6                                 #GPIO pin number for Relay 1
RELAY_2_PIN = 7                                 #GPIO pin number for Relay 2

#Pushover Message API Configuration
USE_PUSHOVER=False                                  #Enable/Disable Pushover functionality
PUSHOVER_TOKEN=""                                   #The Pushover APP token - Register on https://pushover.net/ to generate a token
PUSHOVER_USER=""                                    #The Pushover APP user or group key - Configure this on https://pushover.net/
PUSHOVER_MESSAGE="Garage door action triggered!"    #Message for the doorbell message
PUSHOVER_HOST="api.pushover.net"                    #The hostname
PUSHOVER_PROTOCOL="https://"                        #Protocol to be used, usually 'https://'
PUSHOVER_API_BASE_MESSAGE="/1/messages.json"        #URL Base for messages API

#Theme settings
SITE_TITLE = "Garage Door Opener"
SITE_RELAY_1_BTN_LABEL = "Open/Close Relay 1"
SITE_RELAY_2_BTN_LABEL = "Open/Close Relay 2"
SITE_COPYRIGHT_YEAR = "2025"
SITE_VERSION = "1.1.0"
SITE_FOOTER_LINKS = [
    {
        "text": "Github", 
        "href": "https://github.com/ryanfitton/rpi-pico-garage-door-opener"
    },
    {
        "text": "About this project", 
        "href": "https://ryanfitton.co.uk/blog/rpi-pico-garage-door-opener-relay-3v/"
    }
]