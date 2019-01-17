from skc.basic_approx.file import *
from skc.utils import *
from skc.operator import OperatorTolerance

# Read in enumerated, potential group members, and check for uniqueness
def read_and_simplify(l_0):
	import pdb
	sequences = []
	# Start numbering gates from 1, since identity is 0
	i = 1

	for generation_num in range(1,l_0+1):
		filename_pattern = filename_prefix + "-g" + str(generation_num) \
			+ "*.pickle"
		print str(filename_pattern)
		
		filenames = glob.glob(filename_pattern)
		if (len(filenames) == 0):
			raise RuntimeError("No files found for generation " + str(generation_num))
		for filename in filenames:
			new_sequences = read_from_file(filename)
			
			print "Generation " + str(generation_num) + ":"
			print str(len(new_sequences)) + " read"
			#translate to a set
	
			for newop in new_sequences:
				new_op = OperatorTolerance(newop.name, newop.matrix, newop.ancestors)
				new_op.name = "G" + str(i)
				i += 1
				sequences.append(new_op)

			print str(len(sequences))
	
	# Takes too much time so comment to just write all with duplicates
	dump_to_file(sequences, "final-group-"+str(l_0))
	#final_sequences = []
	#l = len(sequences)
	#for ii in range(len(sequences)):
	#	op = sequences[ii]
	#	for f in final_sequences:
	#		if f == op:
	#			break
	#	else:
	#		final_sequences.append(op)
	#	print "processed %d/%d"%(ii,l)
	#
	## Write out the final group to a file
	#dump_to_file(final_sequences, "final-group-"+str(l_0))