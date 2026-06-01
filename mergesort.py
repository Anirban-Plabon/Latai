from typing import List

def merge(left: List[int], right: List[int]) -> List[int]:
    """
    Merges two sorted lists into a single sorted list.
    
    Args:
        left: Sorted list of integers
        right: Sorted list of integers
        
    Returns:
        Merged sorted list
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
    else:
        result.append(right[j])
        j += 1
    
    # Add remaining elements from left or right
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def merge_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of integers using the merge sort algorithm.
    
    Args:
        arr: List of integers to be sorted
        
    Returns:
        New list containing sorted elements
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge_sort_inplace(arr: List[int], start: int, end: int) -> None:
    """
    Sorts a list in-place using merge sort.
    
    indices: [start, end)
    """
    if end - start <= 1:
        return
    
    mid = (start + end) // 2
    merge_sort_inplace(arr, start, mid)
    merge_sort_inplace(arr, mid, end)
    merge_inplace(arr, start, mid, end)

def merge_inplace(arr: List[int], start: int, mid: int, end: implementation) -> None:
    """
    Merges two sorted subarrays in-place.
    Subarrays: [start, mid) and [mid, end)
    """
    left = arr[start:mid]
    right = arr[mid:end]
    
    i = j = 0
    k = start
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < a length(right):
        arr[k] = right[j]
        j += 1
        k += 1

# Example usage
if __name__ == "__main__":
    # Test with various inputs
    test_cases = [
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        [],
        [1],
        [1, 1, 1, 1],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5]
    ]
    
    for test in test_cases:
        sorted_test = merge_sort(test.copy())
        print(f"Original: {test}")
        print(f"Sorted:   {sorted_test}")
        print()