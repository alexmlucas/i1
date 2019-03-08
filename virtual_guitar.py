import time 

class ChordStrummer:
	global midiout
	c_major_chord_notes = [[0, 48, 52, 55, 60, 64],[0, 0, 50, 57, 62, 65],[40, 47, 52, 55, 59, 64],[0, 0, 53, 55, 60, 65],[43, 47, 50, 55, 59, 65],[0, 45, 52, 57, 60, 64],[0, 47, 50, 55, 62, 0]]

	def play_chord(self, chord_number, string_number):
		# print(f"chord #: {chord_number}, string_number {string_number} ")
		if self.c_major_chord_notes[chord_number][string_number] != 0:
			note_on = [0x90, self.c_major_chord_notes[chord_number][string_number], 112]
			midiout.send_message(note_on)
			time.sleep(0.5)
			note_off = [0x80, self.c_major_chord_notes[chord_number][string_number], 0]
			midiout.send_message(note_off)


class StringSegmenter:
	def __init__(self, min_value, max_value, number_of_strings):
		self.min_value = min_value
		self.max_value = max_value
		# The number of segments needs to be twice the number of strings (+ 1) to allow for dead space.
		self.number_of_segments = (number_of_strings * 2) + 1
		self.range = max_value - min_value
		self.segment_size = self.range / self.number_of_segments
		self.segment_boundaries = []
		self.currently_selected_segment = 0

		index = 0
		while index <= self.number_of_segments:
			self.segment_boundaries.append(self.min_value + (self.segment_size * (index)))
			index += 1

	def get_segment_as_string_number(self, segment):
		string_number = (segment / 2) - 0.5
		return int(string_number)

	def get_segment_size(self):
		return self.segment_size

	def get_boundaries(self):
		return self.segment_boundaries

	def determine_segment(self, serial_value):
		for index, boundary_value in enumerate(self.segment_boundaries):
			if serial_value > boundary_value:
				# Update index and continue to iterate through boundary values
				self.currently_selected_segment = index
			else:
				break

		return self.currently_selected_segment

	def is_segment_a_string(self, segment):
		if segment <= 12 and segment >= 0 and segment % 2 > 0:
			return True
		else:
			return False
