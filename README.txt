Description:  Tool to evaluate real-time streams in a pcap file.  Program serches for RTP streams, checks with
user to determine which streams to evaluate, then generates a set of graphs (PDF format) for each stream.  User
can then choose to save streams in separate pcap files, check each file for UDP checksum, and finally it prints
a summary of what it found (size, bandwidth, packet loss, jitter, etc.) on the screen and offers to save this
information into a summary file.  

Suggested use is to quickly scan a pcap file to determine which streams are failing, and then use wireshark for
more detailed investigation.  PDF graphs show loss or jitter or bandwidth over time (1 second intervals by default)
so user can see dynamic behavior of the network.

Note that this program is set up to analyze the traditional pcap files, not the new pcap format.  If you have data
in the new format, open the file with wireshark and then save in the older pcap format.

Setup:

Install latest version of Python 2.7
Run the install.bat file in this folder.
Move your pcap file or files into this folder
execute the pcapEval.py script

ERRORS:
  * Getting the %PATH% variable set correctly, or set multiple times may still be a bug in the install.bat file, fix suggestions appreciated.
  * When running in the command prompt, TKINTER sometimes throws an error saying "can't invoke 'event' command: application has been destroyed ..."
      note that program is still running correctly and may have just asked if you want to save streams into a separate pcap file.  Answer y or n and continue.

johnbartlett19@gmail.com