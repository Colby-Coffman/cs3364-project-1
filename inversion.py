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
	if kv == True:
		arr_table = dict(arr)
		arr = main.key_arr(arr)
	calc = _InvCalculator(arr)
	if func == "qs":
		if retarr == True:
			arr_inv = calc.qs(retarr=True)
			if kv == True:
				for i in range(len(arr_inv[0])):
					arr_inv[0][i] = (arr_inv[0][i], arr_table[arr_inv[0][i]])
			return arr_inv
		return calc.qs()
	elif func == "is":
		if retarr == True:
			arr_inv = calc.ins(retarr=True)
			if kv == True:
				for i in range(len(arr_inv[0])):
					arr_inv[0][i] = (arr_inv[0][i], arr_table[arr_inv[0][i]])
			return arr_inv
		return calc.ins()
	else:
		if retarr == True:
			arr_inv = calc.ms(retarr=True)
			if kv == True:
				for i in range(len(arr_inv[0])):
					arr_inv[0][i] = (arr_inv[0][i], arr_table[arr_inv[0][i]])
			return arr_inv
		return calc.ms()

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
	
	def qs(self, retarr=False):
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
		arr = main.make_equinumerous(self.arr)
		arr = self._qs_invcnt(arr)
		if retarr == True:
			new_arr = main.key_arr(arr)
			inv = self.inversions
			self.inversions = 0
			return (new_arr, inv)
		else:
			inv = self.inversions
			self.inversions = 0
			return inv
		
	def _qs_invcnt(self, arr):
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
		pivot = int(len(arr)/2)
		less = [i for i in arr if i[0]<arr[pivot][0]]
		equal = [i for i in arr if i[0]==arr[pivot][0]]
		greater = [i for i in arr if i[0]>arr[pivot][0]]
		for i in equal:
			for j in less:
				if i[1] < j[1]:
					self.inversions += 1
		for i in equal:
			for j in greater:
				if i[1] > j[1]:
					self.inversions += 1
		for i in less:
			for j in greater:
				if i[1] > j[1]:
					self.inversions += 1
		return self._qs_invcnt(less) + equal + self._qs_invcnt(greater)
	
	def ms(self, retarr=False):
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
		arr = self._ms_invcnt(self.arr)
		if retarr == True:
			inv = self.inversions
			self.inversions = 0
			return (arr, inv)
		else:
			inv = self.inversions
			self.inversions = 0
			return inv

	def _ms_invcnt(self, arr):
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
		middle = int(len(arr)/2)
		lower = [arr[i] for i in range(middle)]
		upper = [arr[i] for i in range(middle, len(arr))]
		arr = self._merge_invcnt(self._ms_invcnt(lower), self._ms_invcnt(upper))
		return arr
	
	def _merge_invcnt(self, lower, upper):
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
			if lower[i]<= upper[j]:
				new_arr.append(lower[i])
				i += 1
			else:
				new_arr.append(upper[j])
				j += 1
				self.inversions += len(lower) - i
		while i!= len(lower):
			new_arr.append(lower[i])
			i += 1
		while j!= len(upper):
			new_arr.append(upper[j])
			j += 1
		return new_arr
	
	def ins(self, retarr=False):
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
		arr = self._ins_invcnt(self.arr)
		if retarr == True:
			new_arr = main.key_arr(arr)
			inv = self.inversions
			self.inversions = 0
			return (new_arr, inv)
		else:
			inv = self.inversions
			self.inversions = 0
			return inv
		
	def _ins_invcnt(self, arr):
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
			elem = arr[i]
			j = i-1
			while j>=0 and elem<arr[j]:
				arr[j+1] = arr[j]
				j -= 1
				self.inversions += 1
			arr[j+1] = elem
		return arr