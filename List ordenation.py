import time
import sys
import numpy as np
import concurrent.futures


def method_1(target_list):

    change_occurred = True
    while change_occurred:
        change_occurred = False

        index = None
        copied_value = None
        for index in range(0, len(target_list)-1):
            if target_list[index] < target_list[index+1]:
                copied_value = target_list[index]
                target_list[index] = target_list[index+1]
                target_list[index + 1] = copied_value
                change_occurred = True
    return target_list


def method_2(target_list):
    new_list = [target_list[0]]
    index = int()
    jindex = int()
    for index in range(1, len(target_list)):
        x = target_list[index]
        for jindex in range(0, len(new_list)):
            if x < new_list[jindex]:
                new_list.insert(jindex, x)
                break
    return new_list


def method_3(target_list):
    new_list = [target_list[0]]
    index = int()
    jindex = int()
    for index in range(1, len(target_list)):
        x = target_list[index]
        left_lim = 0
        right_lim = len(new_list)-1
        while True:
            pos = int((right_lim-left_lim) / 2 + left_lim)
            if (right_lim - left_lim) <= 1:
                if x <= new_list[pos]:
                    new_list.insert(pos, x)
                else:
                    new_list.insert(pos+1, x)
                break
            else:
                if x <= new_list[pos]:
                    right_lim = pos
                else:
                    left_lim = pos

    return new_list


def method_4(target_list):
    if len(target_list) == 0 or len(target_list) == 1:
        return target_list
    else:
        i = len(target_list)//2
        return sum_2_ordered_lists(method_4(target_list[:i]), method_4(target_list[i:]))


def sum_2_ordered_lists(list_1, list_2):
    new_list = []
    i = 0
    j = 0
    while i < len(list_1) and j < len(list_2):
        if list_1[i] <= list_2[j]:
            new_list.append(list_1[i])
            i += 1
        else:
            new_list.append(list_2[j])
            j += 1
    if i == len(list_1):
        new_list.extend(list_2[j:])
    else:
        new_list.extend(list_1[i:])
    return new_list


# Helper function to measure execution time of a single sort operation
def measure_sort_time(list_type, func, data):
    start = time.time()
    result = func(data)
    end = time.time()

    if list_type == 0:
        evaluate_if_list_ordered_little_big(result)
    else:
        evaluate_if_list_ordered_big_little(result)
    return end - start


def evaluate_if_list_ordered_little_big(list_):
    for i in range(len(list_)-1):
        if list_[i] > [i+1]:
            print("it is not ordered little big!!!!!")
            break
    return


def evaluate_if_list_ordered_big_little(list_):
    for i in range(len(list_)-1):
        if list_[i] < [i+1]:
            print("it is not ordered big little!!!!!")
            break
    return


def comp_method_times():
    i = 3
    while True:
        times = []
        try:
            func = getattr(sys.modules[__name__], "method_" + str(i))
        except AttributeError:
            print("There are no more methods to evaluate.")
            break

        random_lists = [np.random.rand(5000) for _ in range(10)]

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(measure_sort_time, 0, func, lst) for lst in random_lists]
            for future in concurrent.futures.as_completed(futures):
                time_taken = future.result()
                times.append(time_taken)
                print(f"method_{i}_time = {time_taken}")

        avg_time = sum(times) / len(times)
        print(f"Avg. time for method {i}: {avg_time}")
        i += 1


# Protect the entry point
if __name__ == "__main__":
    comp_method_times()
