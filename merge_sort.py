"""
Merge sort for efficiently organising specific data
"""


class MergeSort:
    """
    Merge sort algorithm.
    """

    @staticmethod
    def sort(list: list[int]) -> list[int]:
        """
        Sort list using a merge sort algorithm.

        Arguments:
            list (list[int]): List to be sorted.

        Returns:
            list (list[int]): Sorted list
        """
        if len(list) <= 1:
            return list
        mid = len(list) // 2
        left_half = list[:mid]
        right_half = list[mid:]
        left_half = MergeSort.sort(left_half)
        right_half = MergeSort.sort(right_half)
        return MergeSort._merge(left_half, right_half)

    @staticmethod
    def _merge(left: list[int], right: list[int]) -> list[int]:
        """
        Merge two lists (sorted) into one sorted list.

        Arguments:
            left (list[int]): Left list
            right (list[int]): Right list

        Returns:
            result (list[int]): Sorted list of integers, using the arguments
        """
        result = []
        left_index = right_index = 0
        while left_index < len(left) and right_index < len(right):
            if left[left_index] < right[right_index]:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1
        result.extend(left[left_index:])
        result.extend(right[right_index:])
        return result
