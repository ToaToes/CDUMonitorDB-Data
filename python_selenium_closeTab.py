from selenium import webdriver
import time

# Path to your WebDriver (replace with your WebDriver path)
driver_path = 'path/to/your/chromedriver'  # Replace with the path to your WebDriver

# Initialize the WebDriver
driver = webdriver.Chrome(executable_path=driver_path)

# Open a website
driver.get("https://www.example.com")

# Wait for some time to see the page
time.sleep(5)

# Open a second tab (just for demonstration)
driver.execute_script("window.open('https://www.google.com');")
time.sleep(2)

# Get the list of all open window handles (tabs)
handles = driver.window_handles

# Switch to the second tab (Google) and close it
driver.switch_to.window(handles[1])  # Switch to the second tab (Google)
driver.close()  # Close this tab

# Switch back to the first tab (Example) and wait or perform actions
driver.switch_to.window(handles[0])  # Switch back to the first tab

# Wait for a few seconds to observe
time.sleep(3)

# Optionally, close the browser after everything is done
driver.quit()

print("Closed one tab while keeping the other open.")
