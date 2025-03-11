import numpy as np

a = np.array(42)
b = np.array([1, 2, 3, 4, 5])
c = np.array([[1, 2, 3, -3, -2, -1], [4, 5, 6, -6, -5, -4], [11, 21, 31, -31, -21, -11]])
d = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])

print(c[1:3, 2:6:2])
print(b[::2]) # bierze kazdy X-owy element, gdzie ::X

# Create an array with data type 2 bytes integer:
arr = np.array([1, 2, 3, 4], dtype='i2')
print(arr)
print(arr.dtype) 


# The astype() function creates a copy of the array, 
# and allows you to specify the data type as a parameter.

arr = np.array([1.1, 0.0, 3.8])
newarr = arr.astype(bool)
print(newarr)
print(newarr.dtype) 


arr = np.array([1, 2, 3, 4, 5])
print("test: ")
print (arr.T)

x = arr.copy()
arr[0] = 42

print(arr)
print(x) 


arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
# pokazuje wszystkie elementy duzo-przestrzeniowej (1D, 2D, ..., nD) tablicy w jednym for
# dzieki np.nditer(arr) nie trzeba pisac n petli for 
for x in np.nditer(arr):
  print(x) 



arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])

for idx, x in np.ndenumerate(arr):
  print(idx, x) 



# NumPy provides a helper function: hstack() to stack along rows.
arr1 = np.array([1, 5, 3])
arr2 = np.array([4, 6, 2])
arr = np.hstack((arr1, arr2))
print(arr) 


# NumPy provides a helper function: vstack() to stack along columns.
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr = np.vstack((arr1, arr2))
print(arr) 


# To search an array, use the where() method.
arr = np.array([1, 2, 3, 4, 5, 4, 4])
x = np.where(arr == 4)
print(x)


# If you use the sort() method on a 2-D array, both arrays will be sorted:
arr = np.array([[3, 2, 4], [5, 0, 1]])
print(np.sort(arr))


# append() adds element to the end of array


# Create a filter array that will return only values higher than 42:
arr = np.array([41, 42, 43, 44])
filter_arr = arr > 42
newarr = arr[filter_arr]
print(filter_arr)
print(newarr) 


# random
from numpy import random
# randint <0,100)
x = random.randint(100)
print(x)

# Generate a random float from 0 to 1:
x = random.rand()


# Generate a 1-D array containing 5 random floats:
x = random.rand(5)
print(x)


# Generate a 2-D array with 3 rows, each row containing 5 random numbers:
x = random.rand(3, 5)
print(x)


#  The shuffle() method makes changes to the original array.
arr = np.array([1, 2, 3, 4, 5])
random.shuffle(arr)
print(arr)



import matplotlib.pyplot as plt
import seaborn as sns
print("sns and plt")
sns.distplot([0, 1, 2, 3, 4, 5])
plt.show() 

# Rozkład Gaussa
random.normal()

#