import main

def count_inversions(arr, kv=False, retarr=False, func="ms"):
	"""
	A function to count the inversions in an array using various algorithms
	Args:
		arr (list): A list of elements
		kv = False (boolean): A flag that indicates the list passed will be a list of
		tuples whos inversions between each first component will be counted and sorted
		retarr = False (boolean): A flag to tell the function to return a tuple whos 
		first element is the sorted list and second element is the number of inversions in the list
		func = "ms" (string): A flag to indicate which sorting algorithm is used to
		count inversions and sort the array. Valid strings are "ms" for merge sort,
		"qs" for quick sort, and "is" for insertion sort
	Returns:
		If retarr is True, returns a tuple with it's first component being the sorted
		list and it's second component being the number of inversions in that list
		Otherwise returns the number of inversions in the list
	"""
	calc = _InvCalculator(arr) # Instantiate calculator
	if func == "qs": # Quicksort calculation
		if retarr == True: # Not used in main code but adds testing functionality
			arr_inv = calc.qs(kv, retarr=True) # (arr, inversion count)
			return arr_inv
		return calc.qs(kv)
	elif func == "is":
		if retarr == True:
			arr_inv = calc.ins(kv, retarr=True)
			return arr_inv
		return calc.ins(kv)
	else:
		if retarr == True:
			arr_inv = calc.ms(kv, retarr=True)
			return arr_inv
		return calc.ms(kv)

class _InvCalculator():
	"""
	A private class to preform computation to determine the number of inversions in
	an list

	Attributes:
		inversions (int): The number of inversions in the list (used to maintain global
		state)
		arr (list): A list of elements or a list of tuples
	"""
	def __init__(self, arr):
		"""
		The constructor for _InvCalculator

		Args:
			arr (list): A list of elements or a list of tuples to be sorted and or
			inversions within counted
		"""
		self.inversions = 0
		self.arr = arr
	
	def qs(self, kv, retarr=False):
		"""
		A function to count the inversions and or sort a list using quicksort

		Args:
			retarr=False (boolean): A flag to indicate whether to return a tuple with
			it's first component being the sorted list and it's second component being
			the number of inversions in the list
		Returns:
			Returns a tuple with its first component being the sorted list and it's
			second component being the number of inversions in the list. Simply returns
			the number of inversions otherwise
		"""
		arr = list(self.arr) # Used to copy self.arr, otherwise arr is treated as a pointer
		arr = main.make_equinumerous(arr) # Required for QS because QS does not sort with respect to index
		arr = self._qs_invcnt(arr, kv) # Count inversions and get array
		if retarr == True:
			new_arr = main.key_arr(arr)
			inv = self.inversions
			self.inversions = 0
			return (new_arr, inv) # Return tuple (sorted arr, inversion count)
		else:
			inv = self.inversions # Otherwise just return inversion count
			self.inversions = 0
			return inv
		
	def _qs_invcnt(self, arr, kv):
		"""
		A private helper function to actually preform the sorting and the counting of
		inversions
		
		Args: 
			arr (list): The list to sort and count the inversions of
		Returns:
			arr (list): The sorted list
		"""
		if len(arr) == 1 or len(arr) == 0:
			return arr
		pivot = int(len(arr)/2) # Pivot point
		if kv == True: # List comprehension has to be preformed differently with a list of tuples vs a list of elements
			less = [i for i in arr if i[0][0]<arr[pivot - 1][0][0]] # Copy all elements smaller, equal, or larger than the pivot element
			equal = [i for i in arr if i[0][0]==arr[pivot - 1][0][0]]
			greater = [i for i in arr if i[0][0]>arr[pivot - 1][0][0]]
		else:
			less = [i for i in arr if i[0]<arr[pivot - 1][0]]
			equal = [i for i in arr if i[0]==arr[pivot - 1][0]]
			greater = [i for i in arr if i[0]>arr[pivot - 1][0]]
		for i in equal: # Count all inversions between the same array and less array, same array and greater array, and less array and greater array
			for j in less:
				if i[1] < j[1]: # Checking for index value because regular quicksort does not care about index value
					self.inversions += 1
		for i in equal:
			for j in greater:
				if i[1] > j[1]:
					self.inversions += 1
		for i in less:
			for j in greater:
				if i[1] > j[1]:
					self.inversions += 1
		return self._qs_invcnt(less, kv) + equal + self._qs_invcnt(greater, kv) # Recursively sort and count inversions
	
	def ms(self, kv, retarr=False):
		"""
		A function to count the inversions and or sort a list using merge sort

		Args:
			retarr=False (boolean): A flag to indicate whether to return a tuple with
			it's first component being the sorted list and it's second component being
			the number of inversions in the list
		Returns:
			Returns a tuple with its first component being the sorted list and it's
			second component being the number of inversions in the list. Simply returns
			the number of inversions otherwise
		"""
		arr = list(self.arr) # Copy self.arr, otherwise arr is treated as a pointer
		arr = self._ms_invcnt(arr, kv)
		if retarr == True:
			inv = self.inversions
			self.inversions = 0
			return (arr, inv)
		else:
			inv = self.inversions
			self.inversions = 0
			return inv

	def _ms_invcnt(self, arr, kv):
		"""
		A private helper function to actually preform the sorting and the counting of
		inversions
		
		Args: 
			arr (list): The list to sort and count the inversions of
		Returns:
			arr (list): The sorted list
		"""
		if (len(arr) == 1):
			return arr
		middle = int(len(arr)/2) # Middle partition
		lower = [arr[i] for i in range(middle)] # Copy lower half
		upper = [arr[i] for i in range(middle, len(arr))] # Copy upper half
		arr = self._merge_invcnt(self._ms_invcnt(lower, kv), self._ms_invcnt(upper, kv), kv) # recursively sort sub arrays, count inversions and combine into bigger sorted array
		return arr
	
	def _merge_invcnt(self, lower, upper, kv):
		"""
		A private helper function to merge two sorted arrays and count the inversions
		between them. It is assumed that upper is at a greater index than lower, so
		inversions are counted whenever a lower element is greater than the upper
		element
		
		Args:
			lower (list): The lower list of elements
			upper (list): The upper list of elements
		"""
		new_arr = []
		i = 0
		j = 0
		while i<len(lower) and j<len(upper):
			if kv == True: # Have to access a list of tuples differently than a list of elements
				if lower[i][0]<= upper[j][0]: # (value, page)
					new_arr.append(lower[i]) # If the value of lower is less than the value of upper, we are going to append lower and move up the array
					i += 1
				else:
					new_arr.append(upper[j]) # If the value of upper is less than the value of lower, we are going to append upper and move up the array
					j += 1
					self.inversions += len(lower) - i # By definition an inversion exists when i<j and a[i]>a[j]
					# The number of inversions here is the number of numbers in lower that have not been added to the new array
			else:
				if lower[i]<= upper[j]:
					new_arr.append(lower[i])
					i += 1
				else:
					new_arr.append(upper[j])
					j += 1
					self.inversions += len(lower) - i
		while i!= len(lower): # If we already added all the elements in one array we add the rest to the array
			new_arr.append(lower[i])
			i += 1
		while j!= len(upper):
			new_arr.append(upper[j])
			j += 1
		return new_arr
	
	def ins(self, kv, retarr=False):
		"""
		A function to count the inversions and or sort a list using insertion sort

		Args:
			retarr=False (boolean): A flag to indicate whether to return a tuple with
			it's first component being the sorted list and it's second component being
			the number of inversions in the list
		Returns:
			Returns a tuple with its first component being the sorted list and it's
			second component being the number of inversions in the list. Simply returns
			the number of inversions otherwise
		"""
		arr = list(self.arr) # Copy self.arr, otherwise arr is treated as a pointer
		arr = self._ins_invcnt(arr, kv)
		if retarr == True:
			inv = self.inversions
			self.inversions = 0
			return (arr, inv)
		else:
			inv = self.inversions
			self.inversions = 0
			return inv
		
	def _ins_invcnt(self, arr, kv):
		"""
		A private helper function to actually preform the sorting and the counting of
		inversions
		
		Args: 
			arr (list): The list to sort and count the inversions of
		Returns:
			arr (list): The sorted list
		"""
		self.inversions = 0
		for i in range(1, len(arr)):
			elem = arr[i] # Grab an element [1,n]
			j = i-1 # Grab an element [0, n-1]
			# We go through 0,n-1 and if the element at j is greater than elem, we move j up one position in the array
			if kv==True: 
				while j>=0 and elem[0]<arr[j][0]:
					arr[j+1] = arr[j]
					j -= 1
					self.inversions += 1
			else:
				while j>=0 and elem<arr[j]:
					arr[j+1] = arr[j]
					j -= 1
					self.inversions += 1
			arr[j+1] = elem
		return arr
