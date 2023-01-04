import sys
import re
import fileinput 
class concord:
	
	def __init__(self, input=None, output=None):
		self.input = input
		self.output = output
		if self.output != None:
			output_text = self.full_concordance()
			self.__write_file(output_text, self.output)
	def __write_file(self, output_text, output_file):
		f = open(output_file, "w")
		for line in output_text: 
			f.write(line + '\n')
		f.close()
	def __sort_lines(self, exc_words, concord_lines):
		"""
		Purpose: Sorts standard input into correct arrays for indexing. Checks 
		if version number is correct.
	
		Parameters: None
	
		Returns: "Input is version 1, concord2.py expected version 2" - if 
		 	first line is a 1
			 exc_words - array
			 concord_lines - array
	
		Pre-Conditions: - self.input is a text file
			- line contains word for indexing at most once
			- Three single quotation marks indicate the start of 
			  lines containing exclusion words
			- Three double quotation marks indicate the
			  start of lines to be indexed
		"""
		in_checker = 0
		for line in fileinput.input(self.input):
			line = line.strip()
			if line == "1":
				print("Input is version 1, concord4.py expected version 2")
				in_checker = in_checker + 1
				exit(0)
			if line == "''''":
				in_checker = 1
			elif line == '""""':
				in_checker = 2
			else:
				if len(line) > 0:
					if in_checker == 1:
						exc_words.append(line.lower())
					elif in_checker == 2:
						concord_lines.append(line)
		return exc_words, concord_lines

	def __tokenize_lines(self, concord_lines, exc_words):
		"""
		Purpose: Puts all words from each line of text in an array each
		on their own line in the concord_words array. Does not append 
		word that is an exclusion word or one that is already in 
		concord_words
		
		Parameters: line: string
	
		Returns: concord_words - array
	
		Pre-Conditions: - lines in concord_lines are strings.
				- Words are seperated by spaces
		"""
		concord_words = []
		for line in concord_lines:
			line = line.lower()
			line = line.split(" ") 
			for word in line:		
				if word not in exc_words and word not in concord_words:
					concord_words.append(word)
		return concord_words
	def __capitalize_lines(self, concord_words, concord_lines):
		"""
		Purpose: Capitalizes every word in concord_lines that appears
			 in concord_words within its text, appends capitalized
			 line and index of its capitalized word to cap_lines
			 array of tuples, returns it. 

		Parameters: concord_words: array[string]
			    concord_lines: array[string]
	
		Returns: (cap_line[], char_index - int) - tuple 
	
		Pre-Conditions: None
		"""	
		cap_line = ""
		cap_lines = []
		num_subs = 0
		for word in concord_words:
			for line in concord_lines:
				word_match = re.search(r"\b{}\b".format(word), line, flags = re.I)
				if (word_match):
					cap_line = re.sub(r"\b{}\b".format(word), word.upper(), line, flags = re.I)
					char_index = word_match.start() 
					cap_lines.append((cap_line,char_index))
		return cap_lines	

	def __space_lines(self, capped_lines):
		"""
		Purpose: Adds spaces before each line in output_array so that each word
			 pointed to by char_index starts at the 30th column/29th index.
			 Calls __strip_lines on each capped_line.
	
		Parameters: capped_line:       string
		
		Returns: void
	
		Pre-Conditions:  - char_index is less than the length of the line
				 - char_index is not negative  
		"""
		output_array = []
		for line_index in capped_lines:
			line = line_index[0]
			char_index = line_index[1]
			
			num_spaces = 29 - char_index
			if num_spaces < 0:
				num_spaces = abs(num_spaces)
				line = self.__strip_lines(line[num_spaces:])
			else:
				line = (num_spaces * " ") + line
				line = self.__strip_lines(line)	
			output_array.append(line)
		return output_array
		
	def __strip_lines(self, line):
		"""
		Purpose: Strips words that span farther left than column 10 and words
			 that fall farther right than column 60. Returns stripped line
			 to __space_lines function to be added to final output array

		Parameters: None
	
		Returns: void

		Pre-Conditions: - output_array is sorted alphabetically by indexed word
				- output_array contains indexed word positioned at
				  index 29
		"""
		space_positions = list(((s.start(0)) for s in re.finditer(" ", line)))
		f_index = 8
		b_index = 60
		if line[f_index] != " ":
			for s in space_positions:
				if s > f_index:
					f_index = s
					break
		if b_index < len(line) and line[b_index] != " ":
			for s in reversed(space_positions):
				if s < b_index:
					b_index = s
					break
		new_line = ""
		for i in range(f_index):
			new_line += " "
		new_line += line[f_index:b_index]
		return new_line

	def full_concordance(self):
		exc_words = []     #holds exclusion words
		concord_lines = [] #holds lines to be indexed
		concord_words = [] #holds key words
		capped_lines = []  #holds lines with capitalized key words
		output = []        #holds final formatted lines 
		
		exc_words, concord_lines = self.__sort_lines(exc_words, concord_lines)
		concord_words = self.__tokenize_lines(concord_lines, exc_words)
		concord_words.sort()
		capped_lines = self.__capitalize_lines(concord_words, concord_lines)
		output = self.__space_lines(capped_lines)
		return output
	
