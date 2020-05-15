from collections import defaultdict
import os
import re

def topic_directories(path) -> (list, list):
    topics = [topic for topic in os.listdir(path) if re.search(r"^Topic", topic)]

    directories = [
        os.path.join(path, topic)
        for topic in topics
        if os.path.isdir(os.path.join(path, topic))
    ]

    return topics, directories


def method_directories(topic_paths, topics, gradient, isotherms, methods):
    full = defaultdict(list)
    temp = defaultdict()
    md = _construct_methods_listing(gradient, isotherms, methods)
    for topic_directory, topic in zip(topic_paths, topics):
        for key in md.keys():
            for item in md[key]:
                full[key].append(os.path.join(topic_directory, item))
        temp[topic] = full.copy()
        full.clear()
    return temp


def method_sorting(method_paths):
    ir_list = defaultdict(list)
    ms_list = defaultdict(list)
    sta_list = defaultdict(list)
    gc_list = defaultdict(list)

    print("Running")
    for topic in method_paths.keys():
        for isograd in method_paths[topic].keys():
            for method in method_paths[topic][isograd]:
                technique = method.split("\\")[-1]
                if technique == "IR":
                    ir_list[isograd].append(method)
                if technique == "STA":
                    sta_list[isograd].append(method)
                if technique == "MS":
                    ms_list[isograd].append(method)
                if technique == "GC":
                    gc_list[isograd].append(method)
    return ir_list, ms_list, sta_list, gc_list


def _construct_methods_listing(gradient, isotherms, methods):
    root = ["Data"]
    method_dict = defaultdict(list)
    for m in methods:
        if isotherms:
            t = 'Isotherm'
            for i in isotherms:
                for r in root:
                    method_dict["isotherm"].append(f"{r}\\{t}\\{i}\\{m}")
        if gradient:
            t = 'Gradient'
            for i in gradient:
                for r in root:
                    method_dict["gradient"].append(f"{r}\\{t}\\{i}\\{m}")
        else: # For older data structure
            t = 'Gradient'
            for r in root:
                method_dict["gradient"].append(f"{r}\\{t}\\{m}")

    return method_dict