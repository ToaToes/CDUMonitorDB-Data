from whatsminer import WhatsminerAccessToken, WhatsminerAPI
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import pywhatkit as kit
from threading import Lock
import win32api
import win32con
import schedule
import time
import gc
from datetime import datetime  # To log cleanup time

# Set default timeout
socket.setdefaulttimeout(0.5)

# WhatsApp group link or group ID
group_id = "HgJMTs9Kw9MLU1NHETjd3B"  # Replace with your group's unique ID or invite link

# Function to switch input method to English
def switch_to_english_input():
    try:
        win32api.PostMessage(0, win32con.WM_INPUTLANGCHANGEREQUEST, 0, 0x0409)  # 0x0409 is the hex code for EN-US
        print("Input method switched to English.")
    except Exception as e:
        print(f"Error switching input method to English: {e}")

# Main function to process IPs and send WhatsApp message
def run_task():
    alert_messages = []
    lock = Lock()

    # Function to process a single IP address
    def process_ip(ip_address):
        try:
            token = WhatsminerAccessToken(ip_address)
            summary_json = WhatsminerAPI.get_read_only_info(access_token=token, cmd="summary")
            error_json = WhatsminerAPI.get_read_only_info(access_token=token, cmd="get_error_code")

            hs_rt = summary_json["SUMMARY"][0]["HS RT"]
            error_code = error_json["Msg"]["error_code"]

            # Check for hs_rt == 0 AND an error code
            if hs_rt == 0 and error_code:
                output_message = f"Alert-Zero HR Miner\nIP = {ip_address} \nhs_rt = {hs_rt} \nerror code = {error_code}"
                with lock:
                    alert_messages.append(output_message)  # Thread-safe update to the list

        except (socket.timeout, Exception):
            pass  # Skip unreachable IPs silently

    # Generate IPs and scan them in parallel
    with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers as needed
        futures = []
        for i in range(1, 22):
            for j in range(1, 6):
                for k in range(1, 21):
                    ip_address = f"10.{i}.{j}.{k}"
                    futures.append(executor.submit(process_ip, ip_address))

        # Wait for all futures to complete
        for future in as_completed(futures):
            pass  # All results are processed within `process_ip`

    # Combine all alert messages into one WhatsApp message
    if alert_messages:
        combined_message = "\n\n".join(alert_messages)
        #print (combined_message)
        # Switch input method to English
        switch_to_english_input()

        # Send the combined message to the WhatsApp group
        try:
            kit.sendwhatmsg_to_group_instantly(group_id, combined_message)
            print (combined_message)
        except Exception:
            pass  # Silently handle any errors during message sending

# Function to clean up unused memory
def cleanup():
    cleanup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time
    print(f"Performing cleanup at {cleanup_time}...")
    gc.collect()  # Run garbage collection to free memory
    print(f"Cleanup completed at {cleanup_time}.")

# Schedule the main task to run every minute
schedule.every(8).minutes.do(run_task)

# Schedule the cleanup task to run every 10 minutes
schedule.every(1).hour.do(cleanup)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
