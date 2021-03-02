# EMS E-Ink Display Project

This is the Python code that runs the UCLA EMS E-Ink Display to show logbook information, announcements, and maintenance duties. To maintain the functionality of the paper maintenance calendar, the screen also recognizes holidays and our EMTs' birthdays. This project gets information from various Google Sheets (used by administrators as a "back-end"), parses the data, and prints to an e-ink display. 

## Installation

Download this repository to your device using the following command:

```bash
git clone http://github.com/ethan-mccarthy/EMS-Display
```

## Hardware
- Raspberry Pi Zero W
- [Waveshare 7.5" (800x480) black and white e-ink display](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm)
- Waveshare e-Paper HAT 
- 3D printed enclosure (STL files in repository)
- 12x M2.5 Heat-set inserts from Virtjoule ([buy on Amazon as a bundle with tip for soldering iron](https://www.amazon.com/gp/product/B000NHVPPO/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1))
- 12x M2.5 5mm machine screws ([buy on Amazon here](https://www.amazon.com/gp/product/B000NHVPPO/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)) -- I think these could have been a bit shorter (<5mm length)

Information about getting started with the Waveshare e-ink display may be found [here](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT).

## Note

Additional software must be installed for the program to work properly! You should also follow the instructions to install the Waveshare EPD package (available [here](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)).

```bash
# Pandas for Python 3
apt-get install python3-python-pandas

# Google API Packages
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Generating QR Codes with PyQRCode
pip install PyQRCode

# Shortening links to be made into QR codes (to make the QR codes more simple)
pip install bitlyshortener

# Working with PNGs (e.g. QR codes and celebratory icons)
pip install pypng
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
