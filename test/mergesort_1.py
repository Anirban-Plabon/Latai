def merge(left: list, right: list) -> list:
    """
    Merge two sorted lists into a single sorted list.
    
    Args:
        left: First sorted list
        right: Second sorted list
        
    Returns:
        Merged sorted list containing all elements from both lists
    """
    merged = []
    left_idx = right_idx = 0
    
    # Compare elements from both lists and add the smaller one to merged
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] <= right[right_idx]:
            merged.append(left[left_idx])
            left_idx += 1
        else:
            merged.append(right[right_idx])
            right_idx += 1
    
    # Add any remaining elements from left list
    while left_idx < len(left):
        merged.append(left[left_idx])
        left_idx += 1
    
    # Add any remaining elements from right list
    while right_idx < len(right):
        merged.append(right[right_idx])
        right_idx += 1
    
    return merged


def mergesort(arr: list) -> list:
    """
    Sort a list using the mergesort algorithm.
    
    Args:
        arr: List of elements to be sorted
        
    Returns:
        A new list containing the sorted elements
    """
    # Base case: list with 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr.copy()
    
    # Find the middle index
    middle = len(arr) // 2
    
    # Recursively sort both halves
    left_half = mergesort(arr[:middle])
    right_half = mergesort(arr[middle:])
    
    # Merge the sorted halves
    return merge(left_half, right_half)


def mergesort_inplace(arr: list) -> None:
    """
    Sort a list in-place using mergesort algorithm.
    This version modifies the original list.
    
    Args:
        arr: List to be sorted in-place
    """
    if len(arr) <= 1:
        return
    
    # Create a temporary array for merging
    temp = [0] * len(arr)
    
    def merge_inplace(start: int, middle: int, end: int) -> None:
        """Merge two sorted subarrays in-place."""
        left_idx = start
        right_idx = middle + 1
        temp_idx = start
        
        # Copy elements to temporary array
        for i in range(start, end + 1):
            temp[i] = arr[i]
        
        # Merge back into original array
        while left_idx <= middle and right_idx <= end:
            if temp[left_idx] <= temp[right_idx]:
                arr[temp_idx] = temp[left_idx]
                left_idx += 1
            else:
                arr[temp_idx] = temp[right_idx]
                right_idx += 1
            temp_idx += 1
        
        # Copy remaining elements from left subarray
        while left_idx <= middle:
            arr[temp_idx] = temp[left_idx]
            left_idx += 1
            temp_idx += 1
        
        # Remaining elements from right subarray are already in place
    
    def mergesort_helper(start: int, end: int) -> None:
        """Helper function for recursive sorting."""
        if start < end:
            middle = (start + end) // 2
            mergesort_helper(start, middle)
            mergesort_helper(middle + 1, end)
            merge_inplace(start, middle, end)
    
    mergesort_helper(0, len(arr) - 1)


def test_mergesort():
    """Test the mergesort implementation."""
    # Test with integers
    test_data = [64, 34, 25, 12, 22, 11, 90]
    expected = [11, 12, 22, 25, 34, 64, 90]
    
    # Test the basic mergesort
    sorted_data = mergesort(test_data)
    assert sorted_data == expected, f"Expected {expected}, got {sorted_data}"
    
    # Test with duplicates
    test_duplicates = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    expected_duplicates = [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    assert mergesort(test_duplicates) == expected_duplicates
    
    # Test with empty list
    assert mergesort([]) == []
    
    # Test with single element
    assert mergesort([42]) == [42]
    
    # Test with already sorted list
    sorted_list = [1, 2, 3, 4, 5]
    assert mergesort(sorted_list) == sorted_list
    
    # Test with reverse sorted list
    reverse_sorted = [5, 4, 3, 2, 1]
    assert mergesort(reverse_sorted) == sorted(reverse_sorted)
    
    # Test the in-place version
    test_inplace = [64, 34, 25, 12, 22, 11, 90]
    mergesort_inplace(test_inplace)
    assert test_inplace == expected
    
    print("All tests passed!")


if __name__ == "__main__":
    test_mergesort()