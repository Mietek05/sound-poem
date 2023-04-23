import pygame as pg
import numpy as np
import math

pg.init()
pg.mixer.init()

def synth(frequency, duration=1.5, sampling_rate=44100, square=False):
	frames = int(duration*sampling_rate)
	arr = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
	arr = arr + np.cos(4*np.pi*frequency*np.linspace(0,duration, frames))
	arr = arr - np.cos(6*np.pi*frequency*np.linspace(0,duration, frames))
	if square:
		arr = np.clip(arr*10, -1, 1)
	arr = arr/max(np.abs(arr))
	sound = np.asarray([32767*arr,32767*arr]).T.astype(np.int16)
	sound = pg.sndarray.make_sound(sound.copy())
	return sound

keys_file = open("keylist.txt")
keylist = keys_file.read()
keys_file.close()

print("ADMITTED CHARACTERS: ", keylist)
print("Enter your text: ", end="")
text = input().lower()
if text == "":
	text = "your text goes here."
print("Enter the BPM: ", end="")
try:
	bpm = float(input())
except:
	bpm = 60
if bpm == "":
	bpm = 60
barTempo = (60/bpm)*1000
print("Enter the scale range [1-3]: ", end="")
try:
	scaleRange = float(input())
except:
	scaleRange = 1
if scaleRange == "":
	scaleRange = 1
print("Enter scale/mode [e.g. C Ionian, A Mixolydian, E Lydian]: ", end="")
scaleName = input().upper().split(" ")
chromaticScale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
scale = ["C", "D", "E", "F", "G", "A", "B"]
print(scaleName)
if scaleName[0] in chromaticScale:
	gradeIndex = chromaticScale.index(scaleName[0])
	scale[0] = chromaticScale[gradeIndex]
	if scaleName[1] == "LYDIAN":
		scale[1] = chromaticScale[(gradeIndex+2)%12]
		scale[2] = chromaticScale[(gradeIndex+4)%12]
		scale[3] = chromaticScale[(gradeIndex+6)%12]
		scale[4] = chromaticScale[(gradeIndex+7)%12]
		scale[5] = chromaticScale[(gradeIndex+9)%12]
		scale[6] = chromaticScale[(gradeIndex+11)%12]
	elif scaleName[1] == "IONIAN":
		scale[1] = chromaticScale[(gradeIndex+2)%12]
		scale[2] = chromaticScale[(gradeIndex+4)%12]
		scale[3] = chromaticScale[(gradeIndex+5)%12]
		scale[4] = chromaticScale[(gradeIndex+7)%12]
		scale[5] = chromaticScale[(gradeIndex+9)%12]
		scale[6] = chromaticScale[(gradeIndex+11)%12]
	elif scaleName[1] == "MIXOLYDIAN":
		scale[1] = chromaticScale[(gradeIndex+2)%12]
		scale[2] = chromaticScale[(gradeIndex+4)%12]
		scale[3] = chromaticScale[(gradeIndex+5)%12]
		scale[4] = chromaticScale[(gradeIndex+7)%12]
		scale[5] = chromaticScale[(gradeIndex+9)%12]
		scale[6] = chromaticScale[(gradeIndex+10)%12]
	elif scaleName[1] == "DORIAN":
		scale[1] = chromaticScale[(gradeIndex+2)%12]
		scale[2] = chromaticScale[(gradeIndex+3)%12]
		scale[3] = chromaticScale[(gradeIndex+5)%12]
		scale[4] = chromaticScale[(gradeIndex+7)%12]
		scale[5] = chromaticScale[(gradeIndex+9)%12]
		scale[6] = chromaticScale[(gradeIndex+10)%12]
	elif scaleName[1] == "AEOLIAN":
		scale[1] = chromaticScale[(gradeIndex+2)%12]
		scale[2] = chromaticScale[(gradeIndex+3)%12]
		scale[3] = chromaticScale[(gradeIndex+5)%12]
		scale[4] = chromaticScale[(gradeIndex+7)%12]
		scale[5] = chromaticScale[(gradeIndex+8)%12]
		scale[6] = chromaticScale[(gradeIndex+10)%12]
	elif scaleName[1] == "PHRYGIAN":
		scale[1] = chromaticScale[(gradeIndex+1)%12]
		scale[2] = chromaticScale[(gradeIndex+3)%12]
		scale[3] = chromaticScale[(gradeIndex+5)%12]
		scale[4] = chromaticScale[(gradeIndex+7)%12]
		scale[5] = chromaticScale[(gradeIndex+8)%12]
		scale[6] = chromaticScale[(gradeIndex+10)%12]
	elif scaleName[1] == "LOCRIAN":
		scale[1] = chromaticScale[(gradeIndex+1)%12]
		scale[2] = chromaticScale[(gradeIndex+3)%12]
		scale[3] = chromaticScale[(gradeIndex+5)%12]
		scale[4] = chromaticScale[(gradeIndex+6)%12]
		scale[5] = chromaticScale[(gradeIndex+8)%12]
		scale[6] = chromaticScale[(gradeIndex+10)%12]

	print(scale)
if len(scaleName[0]) != 1 and len(scaleName) != 2:
	print("(Invalid scale, picking chromatic by default)")
	scale = chromaticScale

print("Enter ending grade [1-"+str(len(scale))+"]: ", end="")
try:
	endingGrade = int(input())
except:
	endingGrade = 0
if endingGrade < 1 or endingGrade > 12:
		print("(Ending grade set to 0 by default. It will not be added)")
		endingGrade = 0

print("Enter pitch [1-7]: ", end="")
try:
	pitch = int(input())
except:
	pitch = 2
if pitch < 1 or pitch > 7:
	print("(Pitch set to 2 by default)")
	pitch = 2

print("Loop [y/n]: ", end="")
loopQuery = input()
if loopQuery == "y":
	loop = True
else:
	loop = False

print(text)


notes_file = open("noteslist.txt")
file_contents = notes_file.read()
notes_file.close()
noteslist = file_contents.splitlines()

notesNum = {}
grade = 1
for i in range(len(keylist)):
	key = keylist[i] 
	notesNum[key] = [grade, i]
	if grade < scaleRange*12:
		grade += 1
	else:
		grade = 1

textNum = []
words = text.split(" ")
timeSignature = 4
for w in words:
	wordLength = len(w)
	modulus = timeSignature % wordLength
	modulus2 = wordLength % timeSignature
	if modulus == 0 or modulus2 == 0:
		duration = int(barTempo*timeSignature/wordLength)
		waiting = duration
		for c in w:
			textNum.append([notesNum[c][0], duration, waiting])
	else:
		blanca = int(barTempo*2)
		negra = int(barTempo)
		corchea = int(barTempo*0.5)
		semicorchea = int(barTempo*0.25)
		if wordLength == 3:
			for c in range(2):
				textNum.append([notesNum[w[c]][0], negra, negra])
			textNum.append([notesNum[w[2]][0], blanca, blanca])
		elif wordLength == 5:
			for c in range(3):
				textNum.append([notesNum[w[c]][0], negra, negra])
			for c in range(2):
				textNum.append([notesNum[w[c+3]][0], corchea, corchea])
		elif wordLength == 6:
			for c in range(4):
				textNum.append([notesNum[w[c]][0], corchea, corchea])
			for c in range(2):
				textNum.append([notesNum[w[c+4]][0], negra, negra])
		elif wordLength == 7:
			for c in range(4):
				textNum.append([notesNum[w[c]][0], corchea, corchea])
			textNum.append([notesNum[w[4]][0], negra, negra])
			for c in range(2):
				textNum.append([notesNum[w[c+5]][0], corchea, corchea])
		elif wordLength == 9:
			for c in range(7):
				textNum.append([notesNum[w[c]][0], corchea, corchea])
			for c in range(2):
				textNum.append([notesNum[w[c+7]][0], semicorchea, semicorchea])
		elif wordLength == 10:
			for c in range(3):
				textNum.append([notesNum[w[c]][0], corchea, corchea])
			for c in range(2):
				textNum.append([notesNum[w[c+3]][0], semicorchea, semicorchea])
			for c in range(3):
				textNum.append([notesNum[w[c]][0], corchea, corchea])
			for c in range(2):
				textNum.append([notesNum[w[c+8]][0], semicorchea, semicorchea])



melodyNotes = []

for i in range(len(textNum)):
	textNum[i][0] = round(textNum[i][0]*(len(scale)/12))
	mod = 0
	j = textNum[i][0]-textNum[0][0]
	mod += math.floor(j/len(scale))
	if j >= 0:
		while abs(j) >= len(scale):
			j = len(scale)-abs(j)
	else:
		while j < 0:
			j = len(scale)+j
	melodyNotes.append([scale[abs(j)], mod, textNum[i][1], textNum[i][2]])

letterNotes = {}
#freq = 16.3516
freq = 16
for i in range(len(noteslist)):
    mod = int(i/12)
    key = noteslist[i]
    sample = synth(freq)
    letterNotes[key] = [sample, mod, freq]
    letterNotes[key][0].set_volume(0.33)
    freq = freq * 2 ** (1/12)

def playNote(note, mod):
	print(note[0]+str(note[1]+pitch), end=" ")
	key = note[0]+str(note[1]+mod)
	letterNotes[key][0].play()
	letterNotes[key][0].fadeout(note[2])
	pg.time.wait(note[3])

def playMelody(melody, mod, signature):
	pulse = 1
	for i in range(len(melody)):
		playNote(melody[i], mod)
		if pulse < signature:
			pulse += 1
		else:
			pulse = 1
	if endingGrade > 0 or not loop:
		endingNote = melody[0]
		endingNote[0] = scale[endingGrade-1]
		endingNote[2] *= 3
		endingNote[3] *= 4
		playNote(endingNote, mod)

if loop == False:
	playMelody(melodyNotes, pitch+2, timeSignature)

loopCount = 0
while loop == True:
	playMelody(melodyNotes, pitch+2, timeSignature)
	loopCount+=1
	print(loopCount)

pg.mixer.quit()
pg.quit()
