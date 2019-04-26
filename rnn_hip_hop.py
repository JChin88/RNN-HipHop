from mido import MidiFile, MidiTrack, Message
import torch
import torch.nn as nn
import torch.optim as optim

from parseMIDI import parseMsgs, reconstructFromMsgs, reconstruct, transpose, getTracksWithNotes

import glob
import time
import math

def findFiles(path): return glob.glob(path)

def createMidiFile(filename, output, tpb, program = 0):
    """Uncomment print statements to view output sequence"""
    # print('\nSequence for %s' % filename)
    sequence = []
    for out in output:
        o = out[0][1:]
        o[0] += 1
        note = [i for i, j in enumerate(o[:12]) if j == max(o[:12])][0]
        pitch = [i for i, j in enumerate(o[12:22]) if j == max(o[12:22])][0]
        length = [i for i, j in enumerate(o[22:]) if j == max(o[22:])][0]        
        
        # print((o[0].int().tolist(), pitch*12 + note, 90, length))

        sequence += [(o[0].int().tolist(), pitch*12 + note, 90, length)]
    return reconstruct(filename, sequence, tpb, program = program)

def createTransposed():
	songs = findFiles('tracks/*.mid')
	for s in songs:
		for i in range(12):
			mid = transpose(s, i, 0)

def extractTracks():
	tracks = findFiles('MidiFiles/*.mid')
	for t in tracks:
		mid = MidiFile(t)
		getTracksWithNotes(mid, t[10:])

def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def train(filenames, numEpochs):
	rnn = nn.LSTM(31, 31)
	criterion = nn.MSELoss()
	learning_rate = 0.05
	optimizer = optim.Adam(rnn.parameters(), lr = learning_rate)
	print('Begin Training\n')
	start = time.time()
	for i in range(numEpochs):
		for f in filenames:
			# print('Training on %s' % f)
			seq = parseMsgs(f)
			if len(seq) > 0:
				t = torch.tensor(seq).view(len(seq), 1, 31).float()
				rnn.zero_grad()
				hx = torch.zeros(1, 1, 31)
				cx = torch.zeros(1, 1, 31)
				out, (hx, cx) = rnn(t, (hx,cx))
				loss = criterion(out, t)
				loss.backward(retain_graph = True)
				optimizer.step()
			# mid = createMidiFile('%s_epoch_%d.mid' % (f[6:-4], i), out, 96)
		print('Epoch: %d / %d, Elapsed time: %s' % (i + 1, numEpochs, timeSince(start)))
	return rnn

if __name__ == '__main__':
	print("Extracting Tracks...")
	extractTracks()
	print("Transposing Samples...")
	createTransposed()
	# filenames = findFiles('input/*.mid')
	# rnn = train(filenames, 20)

	# rand = torch.rand(100, 1, 31)
	# randh = torch.rand(1, 1, 31)
	# randc = torch.rand(1, 1, 31)
	# out, (hx, cx) = rnn(rand, (randh, randc))
	# mid = createMidiFile('rand/random_output.mid', out, 96, program = 88)