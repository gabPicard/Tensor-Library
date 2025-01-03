# Tensor Library

The Tensor Library is a Python package made to manage n-dimensional arrays: tensors. The package implements different functions to make the manipulation of a tensor easier: creation, navigation, addition and substraction, modification, etc...

This library is a personal project I made to learn more about Python and the maths behind the tensors. I wouldn't recommend using it, as it is neither perfect nor optimized. Furthermore, there already exist a lot of better made packages, such as [numpy](numpy.org), which provide much more utility.

## Installing the Tensor 

You can find the library [here](https://pypi.org/project/TensorLibrary/1.0.0/#description), or directly download it using this command:

```
pip install TensorLibrary==1.0.0
```

## Using the Tensor Library

### Creating a tensor

The first step of using this library is by simply creating a tensor.

To do so, you simply have to call the NDimensionalTensor class with the correct arguments:

- The shape: the shape is an array containing the different dimensions of the tensor and all of their sizes. For example, if we want to create a 3-dimensional tensor, 2 by 4 by 1, we write:
  ```python
  t1 = NDimensionalTensor([2,4,1])
  ```
  We can also use already existing array as the shape for creating tensor:
  ```python
  shape = [2,4,1]
  t1 = NDimensionalTensor(shape)
  ```
  If no shape is indicated, the class will create an empty tensor by default 
- The "filling": this specifies the initial value to fill the tensor. For a more simple use, it can only be an integer.
  
  To create a 3x4x1 tensor filled with the number 1, we write:
  ```python
  t1 = NDimensionalTensor([3,4,1], 1)
  ```
  If no filling is indicated, the tensor will be filled with 0 by default
  
### Converting a list to a tensor

To convert an already existing list to a tensor, you can use the class method ToTensor. 

To use it, you simply have to use the list as the argument:

```python

matrix = [[1,2,3],[4,5,6],[7,8,9]]
tensor = NDimensionTensor.ToTensor(matrix)

```
> Note: the list must have a "coherent" shape for the conversion to work.

### Navigating a tensor

To access an element of a tensor, you can either call it's indexes directly:
```python
element = t1[1,3,0]
```
Or you can use an already existing array:
```python
indexes = [1,3,0]
element = t1[indexes]
```
You can also access a sub-dimension of a tensor. For example, if you have the following matrix (2d-tensor):
```python
[[1,2],
[3,4]]
```
You can access the second line by writing:
```python
second_line = t1[1]
```
> Note: This only works if you are calling the dimensions in order. Here, we can access each line individually, because the lines are the first dimension, but we cannot access the column, because it is called in second.
> To access this type of dimensions, you will have to use the function *extract_tensor* that we will discuss later

The printing function works as usual:
```python
print(t1)
```
> Note: The printing function has a special visual for matrices. Any dimension greater to 2 will have a standard visual

### Basic manipulation of a tensor

We saw earlier that you can access an element inside a tensor using an array, but you can do the same to set an element:
```python
indexes = [0,1,1]
t1[indexes] = -1
```
You can also set entire lines by calling a sub-dimension:
```python
matrix = NDimensionTensor([3,3])
matrix[1] = 1
```
Here, all lines will be filled with 0 by default, but we set the entire middle line as 1.
> Note: As mentioned before, you can only do this if you call the sub-dimension in order. I changed here a line, but I am not able to change a column. To do so, we will have to use the *partial_filing* function that we will discuss later

The addition and substraction functions also work by default. You can simply use the mathematical symbols:
```python
t1 = NDimensionTensor([3,3],1)
t2 = NDimensionTensor([3,3],2)
t3 = t1+t2
```
> Note: You can only add of substract a tensor to another tensor of the same shape, exactly.

### Mass manipulation of a tensor

We saw earlier that you couldn't access or set a comun in a tensor, because you are limited to calling the sub-division in order. To solve this problem, I made two functions:

#### extract_tensor

The *extract_tensor* function allows you to access specific set of elements inside a tensor without being limited by the order of the sub-division. To use it, you must use an array of arrays, wich specifies the area to be modified. 

For example: let's say that we have a 5 by 5 matrix, and we want to extract all the element wich are not on the edges. This can be rewritten as all the elements from lines 2 to 4, and columns 2 to 4. We can write:
```python
elements = matrix.extract_tensor([[1,3],[1,3]])
```
If you want the same thing, but only the line in the middle (the 3rd one), you can call the function indicating only the 3rd line, and the columns from 2 to 4 (included). It looks like this:
```python
third_line = matrix.extract_tensor([2,[1,3]])
```
> Note: You can only extract tensors. For example, if you wanted to do the opposite as before, wich would be extracting the border of the matrix instead of the inside, it wouldn't be possible because you would end up with a tensor containing an empty middle

#### partial_filing

The *partial_filing* function allows you to set elements inside a tensor using an integer or another tensor. You basically use it the same way as the *extract_tensor* function. You call it using the indexes and the filing. 

For example, let's use the same 5 by 5 matrix. It is filled with 0, but we want to set the inside elements to 1. We can write:
```python
matrix = NDimensionTensor([5,5])
matrix.partial_filing([[1,3],[1,3]],1)
```
You can also fill the specified area using another tensor. If, instead of filing with 1, we wanted to fill the inside of the matrix with another tensor, we would have to write:
```python
matrix = NDimensionTensor([5,5])
smaller_matrix = NDimensionTensor([3,3],1)
matrix.partial_filing([[1,3],[1,3]],smaller_matrix)
```
> Note: the specified indexes must match the shape of the tensor used for filling

#### concatenate

The *concatenate* function allows use to "fuse" two tensors together. To use this function, you have to specify the second tensor, the dimension that will be expanded, and wich tensor will go in front of the other.

For example: we have two 3 by 3 matrices, one filled with 1, and the other with 2. If we want to put the one filled with 2 on the bottom of the other, we would have to write:
```python
m1 = NDimensionTensor([3,3],1)
m2 = NDimensionTensor([3,3],2)
fused_matrixes = m1.concatenate(m2,0,"back")
```
Here, we call the function using m1, m2, the number 0 and "back".
- The 0 is here to specify wich dimension will be expanded: because we put a matrix "on top" of the other, the number of columns will stay the same, but the number of lines will change. Because the lines are the first dimension, we use 0
- We use m1 as our "base" tensor, and m2 as our "target" tensor. Because we want m2 to be at the bottom, we can consider it to be at the "back", hence the use of this term in the function

For another example: using the same matrixes, we want to put them side by side, with the m2 before m1. The number of lines will stay the same, but the number of column will change. Also, wan can consider that m2 will be at the "front". We can then write:
```python
fused_matrixes = m1.concatenante(m2,1,"front")
```
> Note: The two tensors must have the same shape, except for the dimension that will be expanded.

### Contribution

Everything in this library was entirely made by me, [Gabriel Picard](https://github.com/gabPicard).
I used [this documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/) and [this youtube video](https://www.youtube.com/watch?v=zhpI6Yhz9_4&t=0s) to learn how to make the package and publish it.

### License

This project falls under the MIT license

### Version

Version 1.0.0 - First release on PyPi
