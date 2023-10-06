def quick_sort(arr):
	"""
	Sorts a list using quicksort
	Args:
		arr (list): A list of elements
	Returns:
		arr (list): A sorted list of elements
	"""
	if len(arr) == 1 or len(arr) == 0:
		return arr
	pivot = int(len(arr)/2)
	less = [i for i in arr if i<arr[pivot]]
	equal = [i for i in arr if i==arr[pivot]]
	greater = [i for i in arr if i>arr[pivot]]
	return quick_sort(less) + equal + quick_sort(greater)

def merge_sort(arr):
	"""
	Sorts a list using merge sort
	Args:
		arr (list): A list of elements
	Returns:
		arr (list): A sorted list of elements
	"""
	if (len(arr) == 1):
		return arr
	middle = int(len(arr)/2)
	lower = [arr[i] for i in range(middle)]
	upper = [arr[i] for i in range(middle, len(arr))]
	arr = _merge(merge_sort(lower), merge_sort(upper))
	return arr

def _merge(lower, upper):
	"""
	A private helper function to merge two sorted arrays using quicksort
	Args:
		lower (list): A list of sorted elements
		upper (list): A list of sorted elements
	Returns:
		arr (list): A sorted list of elements from lower and upper
	"""
	new_arr = []
	i = 0
	j = 0
	while i!=len(lower) or j!=len(upper):
		if i==len(lower) or (j<len(upper) and upper[j]<=lower[i]):
			new_arr.append(upper[j])
			j += 1
		else:
			new_arr.append(lower[i])
			i += 1
	return new_arr

def insertion_sort(arr):
	"""
	Sorts a list using insertion sort
	Args:
		arr (list): A list of elements
	Returns:
		arr (list): A sorted list of elements
	"""
	for i in range(1, len(arr)):
		elem = arr[i]
		j = i-1
		while j>=0 and elem<arr[j]:
			arr[j+1] = arr[j]
			j -= 1
			inversions += 1
		arr[j+1] = elem
	return inversions