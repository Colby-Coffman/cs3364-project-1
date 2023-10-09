import numpy as np
import sorts
import inversion as inv
import time


def key_sort(arr):
	"""
	A helper function to sort a list of tuples by it's first value ("key")

	Args:
		arr (list): A list of tuples
	Returns:
		arr (list): A list of tuples sorted by it's first component
	"""
	page_rankings = sorts.quick_sort(arr, kv=True)
	return page_rankings

def page_sort(arr, rank_arr):
	"""
	A helper function to sort a list of elements by the occurance of the second
	component of a list of tuples. All elements in the first list must be also in
	the second component of a tuple in the second list and vice versa. The second
	component is assumed to be an index for some element in the first list.

	 Args:
		arr (list): A list of elements
		rank_arr (list): A list of tuples whos second component of each tuple are in
		the first list and are an index to a component in the first list
	Returns:
		arr (list): A list sorted by the rank_arr
	"""
	reversed_rank_arr = []
	for tupl in rank_arr: # Reverse rank arr for convenience
		reversed_rank_arr.append((tupl[1], tupl[0])) # (rank, page) -> (page, rank)
	page_sorted_arr = []
	for tupl in reversed_rank_arr: 
		page_sorted_arr.append((arr[tupl[0] - 1], tupl[0])) # (index, page)
	return page_sorted_arr

def make_equinumerous(arr):
	"""
	A helper function to make a list equinumerous with a subset of N

	Args:
		arr (list): A list of elements
	Returns:
		arr (list): A list of tuples with its first component being an element in arr
		and the second component being a number indexing each element from 1 to len(arr)
	"""
	return list(zip(arr, range(1,len(arr) + 1))) # [4,4,3] -> [(4,1), (4,2), (3,3)]

def key_arr(arr):
	"""
	A helper function to put all first components of a list of tuples into a list
	
	Args:
		arr (list): A list of tuples
	Returns:
		arr (list): A list of elements with each element being from the first component
		of a list of tuples
	"""
	new_arr = []
	for tupl in arr:
		new_arr.append(tupl[0])
	return new_arr # [(4,1), (4,2), (3,3)] -> [4, 4, 3]

if __name__ == "__main__": # To prevent import execution
	engine_1=[]
	with open("source1.txt", "r") as file:
		for line in file:
			engine_1.append(int(line.strip("\n"))) # Load engine listing data, strip newline and treat as integer
	engine_1= np.array(engine_1)
	eng1_cpy = engine_1 # Get a copy of the data for later use
	engine_2=[]
	with open("source2.txt", "r") as file:
		for line in file:
			engine_2.append(int(line.strip("\n")))
	engine_2= np.array(engine_2)
	eng2_cpy = engine_2
	engine_3=[]
	with open("source3.txt", "r") as file:
		for line in file:
			engine_3.append(int(line.strip("\n")))
	engine_3= np.array(engine_3)
	eng3_cpy = engine_3
	engine_4=[]
	with open("source4.txt", "r") as file:
		for line in file:
			engine_4.append(int(line.strip("\n")))
	engine_4= np.array(engine_4)
	eng4_cpy = engine_4
	engine_5=[]
	with open("source5.txt", "r") as file:
		for line in file:
			engine_5.append(int(line.strip("\n")))
	engine_5= np.array(engine_5)
	eng5_cpy = engine_5
	
	engine_rank = engine_1 + engine_2 + engine_3 + engine_4 + engine_5 # Sum the rankings of each page
	engine_rank = make_equinumerous(engine_rank) # Used to keep track of pages
	engine_rank = key_sort(engine_rank) # Sort the rankings
	engine_1 = page_sort(engine_1, engine_rank) # Sort the engines by the page rankings
	engine_2 = page_sort(engine_2, engine_rank)
	engine_3 = page_sort(engine_3, engine_rank)
	engine_4 = page_sort(engine_4, engine_rank)
	engine_5 = page_sort(engine_5, engine_rank)
	
	start = time.time()
	eng1_inv = inv.count_inversions(engine_1, kv=True, func="ms") # Count inversions and time
	end = time.time()
	print("Number of inversions in engine 1 using merge sort: ", eng1_inv)
	print("In ", end - start, " seconds")
	
	start = time.time()
	eng1_inv = inv.count_inversions(engine_1, kv=True, func="qs")
	end = time.time()
	print("Number of inversions in engine 1 using quick sort: ", eng1_inv)
	print("In ", end - start, " seconds")

	start = time.time()
	eng1_inv = inv.count_inversions(engine_1, kv=True, func="is")
	end = time.time()
	print("Number of inversions in engine 1 using insertion sort: ", eng1_inv)
	print("In ", end - start, " seconds\n")

	eng2_inv = inv.count_inversions(engine_2, kv=True)
	print("Number of inversions in engine 2 ", eng2_inv)
	eng3_inv = inv.count_inversions(engine_3, kv=True)
	print("Number of inversions in engine 3 ", eng3_inv)
	eng4_inv = inv.count_inversions(engine_4, kv=True)
	print("Number of inversions in engine 4 ", eng4_inv)
	eng5_inv = inv.count_inversions(engine_5, kv=True)
	print("Number of inversions in engine 5 ", eng5_inv)
	print()

	print("First 5 pages in un-weighted rank-sorted array: ")
	for i in range(6):
		print(" ", engine_rank[i][1])

	engine_1 = eng1_inv*np.array(eng1_cpy) # Weight each engine by the inversion count
	engine_2 = eng2_inv*np.array(eng2_cpy)
	engine_3 = eng3_inv*np.array(eng3_cpy)
	engine_4 = eng4_inv*np.array(eng4_cpy)
	engine_5 = eng5_inv*np.array(eng5_cpy)
	engine_rank = engine_1 + eng2_inv + engine_3 + engine_4 + engine_5 # Rank the pages by the sum of the indexes
	engine_rank = make_equinumerous(engine_rank) # Used to keep track of pages
	engine_rank = key_sort(engine_rank) # Sort the rankings from lowest to highest
	print("\nFirst 5 pages of weighted rank-sorted array:")
	for i in range(6):
		print(" ", engine_rank[i][1])
