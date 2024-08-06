# OldRedPhone
A Raspberry Pi powered rotary dial telepone which plays back a random audio from a folder corresponding to the number dialed

# Fun because
- Get a prerecorded response from the phone based on the input dialed.
- You cannot dial M for Murder

# Set up
1. Clone the Repository:
```
git clone https://github.com/030jmk/OldRedPhone.git
```
2. Install Dependencies:
```
sudo apt-get install sox
```
4. Add or replace audio files: Place .wav and .mp3 files in the audio folders ranging from 1 to 10.
5. Connect a Button: Use GPIO pin 26 on the Raspberry Pi.
6. Connect the speaker of the handset to a 3.5mm audio jack (male) pin
7. Connect a speaker to the 3.5mm audio output jack. (in case of a missing audio-jack, you will have to make use of an adapter or the hdmi output)
8. Run the Script.
```
python phone.py
```


# Automated start and restart
1. Copy the .service file to the systemd system directory:
```
sudo cp phone.service /etc/systemd/system/
```
2. Reload the systemd daemon to recognize the new service file:
```
sudo systemctl daemon-reload
```
3. Enable the service to start on boot:
```
sudo systemctl enable phone.service
```
4. Check the status of the service to ensure it's running:
```
sudo systemctl status phone.service
```

# Video
<a href="http://www.youtube.com/watch?feature=player_embedded&v=bTR6DwSzY9M
" target="_blank"><img src="http://img.youtube.com/vi/bTR6DwSzY9M/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
