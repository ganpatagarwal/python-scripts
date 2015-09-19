def permute(word):
	"""
	By Barry Carrol <Barry.Carroll at psc.com>
	on Tutor list, revised (last line) by me.
	"""
	retList=[]
	if len(word) == 1:
		# There is only one possible permutation
		retList.append(word)
	else:
		# Return a list of all permutations using all characters
		for pos in range(len(word)):
			# Get the permutations of the rest of the word
			permuteList=permute(word[0:pos]+word[pos+1:len(word)])
			# Now, tack the first char onto each word in the  list
			# and add it to the output
			for item in permuteList:
				retList.append(word[pos]+item)
	#return retList
	return list(set(retList)) # make elements of retList unique

def permuteset(word):
	return list(set(permute(word)))
	
print permuteset("abc")

###############################################################
def permutations(string, step = 0):
	#import pdb
	#pdb.set_trace()
	# if we've gotten to the end, print the permutation
	if step == len(string):
		print "".join(string)

	# everything to the right of step has not been swapped yet
	for i in range(step, len(string)):

		# copy the string (store as array)
		string_copy = [character for character in string]
		#print string_copy

		# swap the current index with the step
		string_copy[step], string_copy[i] = string_copy[i], string_copy[step]

		# recurse on the portion of the string that has not been swapped yet (now it's index will begin with step + 1)
		permutations(string_copy, step + 1)
		
permutations("abc")