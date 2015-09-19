def find_missing_items(host_lun_id_list):
	
	"""Returns the host lun id for the LUN to be 
	added in the storage group."""
	
	temp_list=[]
	for item in host_lun_id_list:
		temp_list.append(int(item))
		
	existing_hlu_set = set(temp_list)
	print existing_hlu_set
	smallest_hlu = min(existing_hlu_set)

	#check for the smallest value of HLU 
	if smallest_hlu != 0:
	    return 0

	largest_hlu = max(existing_hlu_set)
	print largest_hlu

	#check for the largest value of HLU 
	if largest_hlu != 12:
	    return (int(largest_hlu)+1)

	#If 0 and 255 both are occupied , search for the unassigned number
	full_hlu_set = set(xrange(smallest_hlu, largest_hlu + 1))
	print full_hlu_set
	missing_hlu_list = sorted(list(full_hlu_set - existing_hlu_set))
	print missing_hlu_list
	if missing_hlu_list:
	    return missing_hlu_list[0]

host_lun_id = find_missing_items(['0','1','2','10','11'])
print host_lun_id
if host_lun_id == None:
	print "error"