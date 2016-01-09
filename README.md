# Garo-GM3D

Shows how to connect your Garo GM3D with a Raspberry Pi and sync the results with Google spreadsheet.

PCB
------------
Below is an example on how to connect the Garo GM3D with your Raspberry Pi. Here I have connected the Raspberry Pi with GPIO 17. You can choose any of the GPIO pins but if you do then make sure that you change to the same pin in the Python code.

![PCB Top View](https://github.com/SoShibby/Garo-GM3D/blob/master/Garo%20GM3D%20PCB.png)

Bill of Materials
-----------------
| Amount | Part Type                          |
| :----- | :------------------------------------ |
| 1      | 10kΩ Resistor                        |
| 1      | 1kΩ Resistor                          |

Google spreadsheet
-----------------
1. Head to [Google Developers Console](https://console.developers.google.com/project) and create a new project (or select the one you have.)
2. Click on Use Google APIs "Enable and manage APIs"
3. Go to “Credentials” and choose “New Credentials > Service Account Key”.
4. Select "New service account" in the drop-down menu and enter a name for you service account
5. Select "JSON" as key type
6. You will automatically download a JSON file with this data.
7. Save this file on your Raspberry Pi and remember where, as you will need it for the next step
8. Next create a new spreadsheet on [Google drive](https://drive.google.com/drive/my-drive).
9. Then give your service account access to this spreadsheet (you do this by click on share when you are viewing your newly created spreadsheet). You can find the email address to your service account by opening the file was downloaded in step 6.

Installation
-----------------
First we start off by installing Pyton
```sh
$ sudo apt-get update
$ sudo apt-get install build-essential python-dev python-openssl
```
Then we install oauth2client for Python
```sh
$ sudo apt-get install python-pip
$ sudo pip install gspread oauth2client
$ sudo pip install PyOpenSSL
```
Next lets download the code for synchronizing the data we receive from the Garo GM3D with the Google spreadsheet
```sh
$ git clone https://github.com/SoShibby/Garo-GM3D
$ cd Garo-GM3D
```
Open the Python file energy_meter.py and edit the line starting with GDOCS_OAUTH_JSON and enter the path to your Google oauth file that you download in the previous step. Also change the row that starts with GDOCS_SPREADSHEET_NAME and enter the name of the spreadsheet in your Google drive that you want to be updated with the current energy usage. When you are done run the following to run the Python code.
```sh
$ python energy_meter.py
```
If you now open your spreadsheet on [Google Drive]("https://drive.google.com/drive/my-drive") you should see that it gets updated with the current energy usage every 30 seconds (you can change the update frequency by changing the line FREQUENCY_SECONDS in the energy_meter.py file).

External Links
------------
[Forum thread about the Garo GM3D](https://community.particle.io/t/hookup-suggestions-for-connecting-a-photon-to-a-pulsing-energy-meter/14536)

[Garo GM3D manual](https://www.garo.ie/GAR1/GAR1-SHOP2/docs/Components/direct%20energy%20meters/GM3D%20Spec.pdf)

[Guide on how to connect to Google spreadsheet](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/connecting-to-googles-docs-updated)

[Using oauth2 for authentication](http://gspread.readthedocs.org/en/latest/oauth2.html)