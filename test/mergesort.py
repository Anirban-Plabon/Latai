def merge(left: list, right: list) -> list:
    """
    Merge two sorted lists into one sorted list.
    
    Args:
        left: Sorted left sublist
        right: Sorted right sublist
        
    Returns:
        Merged sorted list
    """
    merged = []
    i = j = 0
    
    # Compare elements from both sublists and append the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    # Append remaining elements from either sublist
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged

def merge_sort(arr: list) -> list:
    """
    Sort a list using the merge sort algorithm.
    
    Args:
        arr: List of elements to be sorted
        
    Returns:
        Sorted list
    """
    # Base case: list with 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr
    
    # Recursive case: split the list into two halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    # Merge the sorted halves
    return merge(left_half, right_half)

# Example usage
if __name__ == "__main__":
    test_array = [38, 27, 43, 3, 9, 82, 10]
    sorted_array = merge_sort(test_array)
    print(f"Original array: {test_array}")
    print(f"Sorted array: {sorted_array}")