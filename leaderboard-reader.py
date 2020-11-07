import math
import sys

SAVE_SIG = b'\x53\x43\x11\x01\x82\x62\x82\x73\x82\x71\x81\x46\x82\x72\x82\x81\x82\x96\x82\x85\x82\x84\x81\x40\x82\x66\x82\x81\x82\x8D\x82\x85\x82\x93\x81\x40\x82\x81\x82\x8E\x82\x84\x81\x40\x82\x72\x82\x83\x82\x8F\x82\x92\x82\x85\x82\x93\x81\x40\x81\x40\x81\x40\x81\x40\x81\x40\x81\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xA0\xFC\xB2\x84\x6C\x88\x59\x89\x22\x84\xDF\xFB\xAD\xAD\x25\x85\x9D\xCE\x18\xBE\xA0\xE8\xF1\x9C\xF8\xE2\x61\xBC\x96\xB5\x81\xC8'

with open(sys.argv[1], "rb") as f:
	bytes = f.read()
saveOffset = bytes.find(SAVE_SIG)

if saveOffset:
	print("CTR save found at " + '0x{:02x}'.format(saveOffset-128))
else:
	print("CTR save not found")
	quit(1)

charName = (
	"Crash",
	"Cortex",
	"Tiny",
	"Coco",
	"N.Gin",
	"Dingodile",
	"Polar",
	"Pura",
	"Pinstripe",
	"Papu Papu",
	"Ripper Roo",
	"Komodo Joe",
	"N.Tropy",
	"Penta Penguin",
	"Fake Crash",
	"Oxide (?)"
	)
tO = (3,6,4,14,9,2,8,0,5,1,12,10,15,7,11,13,16,17)
trackName = (
	"Dingo Canyon", #0
	"Dragon Mines",
	"Blizzard Bluff", #2
	"Crash Cove",
	"Tiger Temple", #4
	"Papu's Pyramid",
	"Roo's Tubes", #6
	"Hot Air Skyway",
	"Sewer Speedway", #8
	"Mystery Caves",
	"Cortex Castle", #10
	"N.Gin Labs",
	"Polar Pass", #12
	"Oxide Station",
	"Coco Park", #14
	"Tiny Arena",
	"Slide Coliseum", #16
	"Turbo Track"
	)
	
trackDataLength = 292
timesOffset = saveOffset + 592

def getRecord(off):
	ms = int.from_bytes(bytes[off:off+4], byteorder='little')
	return {"time": ms, "name":bytes[off+4:off+12], "char":bytes[off+22]}
def stopwatch(ms):

	secs = ms * 0.001041667
	# I have no idea what the significance of this float is, but it is necessary to match the times displayed in-game
	# Maybe weird CPU/framerate stuff?
	m = math.floor(secs/60)
	s = (secs % 60)
	ss = s-s%0.001
	return str(m) + ":" + '{:06.3f}'.format(ss)


for track in range(18):
	print("\n\nTrack: " + trackName[tO[track]])
	
	for record in range(12):
		if record == 0:
			print("\nTime Trial\n  Best Lap  ", end="")
		if record > 0 and record < 6:
			print("        " + str(record) + "#  ", end="")
		if record == 6:
			print("\nRelic Race\n  Best Lap  ", end="")
			pass
		if record > 6:
			print("        " + str(record - 6) + "#  ", end="")
		cRec = getRecord(timesOffset + tO[track] * trackDataLength + record * 24)
		print(str(cRec["time"]).rjust(6) + " ms " + stopwatch(cRec["time"]) + (" '" + cRec["name"].decode("utf-8").replace("\x00","") + "' ").ljust(12) + charName[cRec["char"]])
		
