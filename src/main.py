from phew import connect_to_wifi, is_connected_to_wifi, server
from phew.template import render_template
import json
import config
from machine import Pin                 #Micropython default lib
from machine import WDT                 #Micropython default lib
import time                             #Micropython default lib
import utime                             #Micropython default lib
import gc                               #Micropython default lib
import _thread                          #Micropython default lib


# Pin modifiers from machine
led = machine.Pin('LED', machine.Pin.OUT)   # The LED Pin - This is the internal Pico LED


# Start Watchdog
# =====================================================
wdt = WDT(timeout=8388)  # enable it with a timeout of 2s


######################################################
# Functions
######################################################

# Watchdog Feed
# =====================================================
def feedWatchdog():
 # Feed the watchdog to prevent system from halting
 wdt.feed()


# Initialise WiFi
# =====================================================
def initWiFi():
    feedWatchdog() # Feed Watchdog

    logger("Running `connect_to_wifi() function...`")
    # Connect to WiFi using credentials from config.py and return the IP address
    ip_address = connect_to_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)

    if is_connected_to_wifi():
        feedWatchdog() # Feed Watchdog
        logger(f"Connected to wifi network, IP is {ip_address}")
        return True
    else:
        feedWatchdog() # Feed Watchdog
        logger("Failed to connect to wifi, check credentials in config.py.")
        return False


# Message logger - Mainly for debugging
# =====================================================
def logger(message):
    feedWatchdog() # Feed Watchdog

    print(message)


# Main Code Function
# =====================================================
def main():
    feedWatchdog() # Feed Watchdog

    # Turn on the LED
    led.on()

    # Core 0 task - default, handles the web server and routes
    # =====================================================
    def core0_task():
        feedWatchdog() # Feed Watchdog

        logger("Running on Core 0 ****")

        # Global site metadata used across all templates
        site_meta = {
            "title": config.SITE_TITLE,
            "copyright_year": config.SITE_COPYRIGHT_YEAR,
            "version": config.SITE_VERSION,
            "footer_links": config.SITE_FOOTER_LINKS
        }

        # Home
        def route_home(request):
            # Pass in data for the button attributes
            door_buttons = [
                {
                    "relay": "relay1",
                    "text": config.SITE_RELAY_1_BTN_LABEL,
                    "css_class": "bg-indigo-600 hover:bg-indigo-500 focus-visible:outline-indigo-600" + (" hidden" if not config.ENABLE_RELAY_1 else "")
                },
                {
                    "relay": "relay2",
                    "text": config.SITE_RELAY_2_BTN_LABEL,
                    "css_class": "bg-purple-600 hover:bg-purple-500 focus-visible:outline-purple-600" + (" hidden" if not config.ENABLE_RELAY_2 else "")
                }
            ]
            
            return render_template("templates/index.html", site_meta = site_meta, door_buttons = door_buttons)

        # 404
        def route_catch_all(request):
            return render_template("templates/404.html", site_meta = site_meta), 404

        # API door route
        def route_api_relay(request):
            feedWatchdog() # Feed Watchdog

            response =  False   # Default response is False

            pin = request.data.get("pin", None)
            relay = request.data.get("relay", None)

            # Debugging
            #logger(relay)
            #logger(pin)

            # Sanitize pin: must be digits only and match expected PIN length
            if not isinstance(pin, str) or not pin.isdigit() or len(pin) != len(str(config.PIN)):
                response = False
                return json.dumps(response), 400, { "Content-Type": "application/json" }
            

            # Sanitize relay: only allow known relay names
            allowed_relays = ["relay1", "relay2"]
            if relay not in allowed_relays:
                response = False
                return json.dumps(response), 400, { "Content-Type": "application/json" }


            # Check PIN is correct to what is set in config.py
            if str(pin) == str(config.PIN):

                # Set GPIO pins for the relays if the relay use is enabled in config.py
                relay1 = Pin(config.RELAY_1_PIN, Pin.OUT) if config.ENABLE_RELAY_1 else False
                relay2 = Pin(config.RELAY_2_PIN, Pin.OUT) if config.ENABLE_RELAY_2 else False

                if relay == "relay1" and relay1 is not False:
                    relay1(1)  # Turn on Relay1
                    utime.sleep(config.RELAY_TIME_BETWEEN)
                    relay1(0)  # Turn off Relay1

                if relay == "relay2" and relay2 is not False:
                    relay2(1)  # Turn on Relay2
                    utime.sleep(config.RELAY_TIME_BETWEEN)
                    relay2(0)  # Turn off Relay2

                response =  True # Should return `True` to the AJAX request
                

            return json.dumps(response), 200, { "Content-Type": "application/json" }


        ###
        ### Define the routes and request types on the server
        ###
        server.add_route("/", handler=route_home, methods=["GET"])                  #Home route
        server.add_route("/api/relay", handler=route_api_relay, methods=["POST"])   #API Relay route
        server.set_callback(route_catch_all)                                        #Any other route


        # Run the server on port 80, this should be accessible on at `http://<pico w ip address>/`
        server.run(port=80)


    # Core 1 task - handles WiFi and Garbage Collection
    # =====================================================
    def core1_task():
        feedWatchdog() # Feed Watchdog

        logger("Running on Core 1 ****")

        logger("Running initial connection to WiFi...")
        initWiFi()

        feedWatchdog() # Feed Watchdog
        
        # Variables
        # =====================================================
        initialTicks = utime.ticks_ms()
    
        WiFiInterval = 600000 #Check the Wifi every: Milliseconds - 600000 = 10 minutes
        WiFiNowTicks = initialTicks
        WiFiNowTicksDeadline = 0

        GarbageCollectionInterval = 600000 #Run the Garbage Collection every: Milliseconds - 600000 = 10 minutes
        GarbageCollectionNowTicks = initialTicks
        GarbageCollectionDeadline = 0

        i = 0 # Loop counter
        
        # Loop
        while True:    
            feedWatchdog() # Feed Watchdog

            # Garbage Collection
            # =====================================================
            
            # Set a deadline for of 20 seconds since inital script start
            GarbageCollectionDeadline = utime.ticks_add(GarbageCollectionNowTicks, GarbageCollectionInterval)

            # Current time is greater than deadline
            if utime.ticks_ms() >= GarbageCollectionDeadline:
                feedWatchdog() # Feed Watchdog
                
                #logger("GarbageCollectionDeadline dealine has been reached")
                
                # Run Garbage Collection
                logger("Running Garbage Collection")
                gc.collect()
                logger("Finished Garbage Collection")

                # Update the ticks with current ticks
                GarbageCollectionNowTicks = utime.ticks_ms()

            # WiFi Connection check
            # =====================================================
            
            # Set a deadline for of 10 seconds since inital script start
            WiFiDeadline = utime.ticks_add(WiFiNowTicks, WiFiInterval)
            
            # Current time is greater than deadline
            if utime.ticks_ms() >= WiFiDeadline:
                feedWatchdog() # Feed Watchdog

                logger("WiFiDeadline has been reached")
                logger("Checking WiFi connection...")
                initWiFi()

                feedWatchdog() # Feed Watchdog
                
                # Sleep for a few seconds to ensure network is fully ready
                time.sleep(2)

                feedWatchdog() # Feed Watchdog
                
                # Update the ticks with current ticks
                WiFiNowTicks = utime.ticks_ms()

            # Increase counter by 1
            i += 1

        
    # Start logic function
    # =====================================================
    logger("Starting logic function")

    def logic():
        logger("Running")

        # Turn off the LED
        led.off()
        
        try:
            # Turn on the LED
            led.on()
            # Start a new thread on Core 1 and run tasks
            _thread.start_new_thread(core1_task, ())

            # Core 0 - Run usual tasks
            core0_task()

        except KeyboardInterrupt:
            feedWatchdog() # Feed Watchdog

            # Turn off the LED
            led.off()

            # Debugging
            logger('Keyboard interrupt')

            feedWatchdog() # Feed Watchdog

        except Exception as e:
            feedWatchdog() # Feed Watchdog

            # Turn off the LED
            led.off()
            
            # Debugging
            logger('Exception encountered:')
            logger(e)
            #logger('{} | {}'.format(e, traceback.format_exc()))

            logger('Restarting again')

            feedWatchdog() # Feed Watchdog

            # Retart `logic` function
            logic()

    feedWatchdog() # Feed Watchdog
    
    # Start `logic` function
    logic()


# Try `main` function and capture any Keyboard Interrupts or Exceptions
try:
    main()

except KeyboardInterrupt:
    feedWatchdog() # Feed Watchdog

    # Debugging
    logger('Keyboard interrupt')

    feedWatchdog() # Feed Watchdog


except Exception as e:
    feedWatchdog() # Feed Watchdog
    
    # Debugging
    logger('Exception encountered:')
    logger(e)
    #logger('{} | {}'.format(e, traceback.format_exc()))

    logger('Restarting again')

    feedWatchdog() # Feed Watchdog

    # Retart `main` function
    main()