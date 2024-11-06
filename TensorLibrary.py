class NDimensionTensor:
    def __init__(self, shape, fill=None):
        self.shape = shape
        self.tensor = self._create_tensor(shape, fill)
    
    def _create_tensor(self, shape, fill):
        if len(shape) <= 0:
            return None
        if len(shape) == 1:
            return [fill]*shape[0]
        else:
            return [self._create_tensor(shape[1:],fill) for _ in range(shape[0])]
    
    def __str__(self):
        return str(self.tensor)
    
    def __getitem__(self, indexes):
        if isinstance(indexes, list):
            indexes = tuple(indexes)
        elif not isinstance(indexes, tuple):
            indexes = (indexes,)
        return self._get_element(indexes)
    
    def _get_element(self, indexes):
        data = self.tensor
        for _ in indexes:
            data = data[_]
        return data
    
    def __setitem__(self, indexes, value):
        if value != None:
            if isinstance(indexes, list):
                indexes = tuple(indexes)
            elif not isinstance(indexes, tuple):
                indexes = (indexes,)
            return self._set_element(indexes, value)
    
    def _set_element(self, indexes, value):
        data = self.tensor
        for _ in indexes[:-1]:
            data = data[_]
        data[indexes[-1]] = value

    def __add__(self, tensor):
        if self.shape != tensor.shape:
            raise ValueError("The two tensors are of different shapes")
        if not isinstance(tensor, NDimensionTensor):
            raise ValueError("You can only add a tensor to another")
        result = NDimensionTensor(self.shape)
        result.tensor = self._recursive_addition(self.tensor, tensor.tensor, 1)
        return result
    
    def __sub__(self, tensor):
        if self.shape != tensor.shape:
            raise ValueError("The two tensors are of different shapes")
        if not isinstance(tensor, NDimensionTensor):
            raise ValueError("You can only add a tensor to another")
        result = NDimensionTensor(self.shape)
        result.tensor = self._recursive_addition(self.tensor, tensor.tensor, -1)
        return result
    
    def _recursive_addition(self, data1, data2, sign):
        if isinstance (data1, list):
            return [self._recursive_addition(subdata1, subdata2, sign) for subdata1, subdata2 in zip(data1, data2)]    
        else:
            if sign > 0:
                return data1 + data2
            else:
                return data1 - data2  
    
    def _get_DLine(self, indexes):
        dline = []
        for n in indexes:
            if isinstance (n, list):
                for _ in range(n[0], n[-1]):
                    data = self.tensor
                    indexe = tuple(_ if x == n else x for x in indexes)
                    for i in indexe:
                        data = data[i]
                    dline.append(data)
        return dline
    
    def _lst_nbr(self, indexes):
        count = 0
        for n in indexes:
            if isinstance(n, list):
                count += 1
        return count

    def extract_tensor(self, indexes):
        if self._lst_nbr(indexes) == 1:
            return self._get_DLine(indexes)
        else:
            extract = []
            for _ in indexes:
                if isinstance(_, list):
                    return[self.extract_tensor(tuple(i if x == _ else x for x in indexes)) for i in range(_[0], _[-1])]

    def partial_filing(self, filing, indexes):
        if self._lst_nbr(indexes) == 0:
            if isinstance(filing, NDimensionTensor):
                data = self.tensor
                data_filing = filing.tensor
                for _ in indexes[:-1]:
                    data = data[_]
                    data_filing = data_filing[_]
                data[indexes[-1]] = data_filing[indexes[-1]]
            else:
                data = self.tensor
                for _ in indexes[:-1]:
                    data = data[_]
                data[indexes[-1]] = filing
        else:
            for idx, item in enumerate(indexes):
                if isinstance(item, list):
                    for i in range(item[0], item[-1]):
                        new_indexes = indexes[:idx] + [i] + indexes[idx + 1:]
                        self.partial_filing(filing, new_indexes)
                    break
    
    def concatenate(self, tensor, dimension, position):
        if self.shape[:dimension] != tensor.shape[:dimension]:
            raise ValueError ("The two tensors must have coherent shapes")
        if not isinstance (tensor, NDimensionTensor):
            raise ValueError ("You can only concatenante a tensor to another")
        if dimension >= len(self.shape):
            raise ValueError ("Please specify a valid dimension")
        if position != "front" and position != "back":
            raise ValueError ("Please indicate clearly the point of concatenation")
        new_shape = [self.shape[dimension]+tensor.shape[dimension] if x == self.shape[dimension] else x for x in self.shape]
        result = NDimensionTensor(new_shape, 0)
        if position == "back":
            result.partial_filing(self.tensor, self.shape)
            result.partial_filing(tensor.tensor, [x+self.shape[dimension] if x == tensor.shape[dimension] else x for x in tensor.shape])
        elif position == "front":
            result.partial_filing(tensor.tensor, tensor.shape)
            result.partial_filing(self.tensor, [x+tensor.shape[dimension] if x == self.shape[dimension] else x for x in self.shape])
        return result
        

    


    
    
tensor1 = NDimensionTensor([3,3,3], 1)
tensor2 = NDimensionTensor([3,3,3], 2)
print(tensor1)
print(tensor2)
tensor3 = tensor1.concatenate(tensor2,0,"back")
print(tensor3)
