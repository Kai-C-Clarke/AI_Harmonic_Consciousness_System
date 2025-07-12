# OSC parameter discovery script
from pythonosc import udp_client
client = udp_client.SimpleUDPClient("127.0.0.1", 53280)

# Request parameter list (if Surge supports it)
client.send_message("/dump_params", 1)