import json
import collections
import argparse
import random
import numpy as np
import requests
import re

# api key for query. see https://docs.together.ai/docs/get-started
def your_api_key():
    YOUR_API_KEY = 'd81c3ce387f83738bbf35a9cb47d1db77d55acd8b195f3c5dffd5c255fd758f3'
    return YOUR_API_KEY


# for adding small numbers (1-6 digits) and large numbers (7 digits), write prompt prefix and prompt suffix separately.
def your_prompt():
    """Returns a prompt to add to "[PREFIX]a+b[SUFFIX]", where a,b are integers
    Returns:
        A string.
    Example: a=1111, b=2222, prefix='Input: ', suffix='\nOutput: '
    """
    prefix = '''Question: Calculate the exact sum of 1234567+1234567?\nThe sum of the two numbers is: 2469134\n Question: Calculate the exact sum of '''

    suffix = '?\nThe sum of the two numbers is: '

    return prefix, suffix


def your_config():
    """Returns a config for prompting api
    Returns:
        For both short/medium, long: a dictionary with fixed string keys.
    Note:
        do not add additional keys. 
        The autograder will check whether additional keys are present.
        Adding additional keys will result in error.
    """
    config = {
        'max_tokens': 50, # max_tokens must be >= 50 because we don't always have prior on output length 
        'temperature': 0.3,
        'top_k': 20,
        'top_p': 0.5,
        'repetition_penalty': 1,
        'stop': []}
    
    return config


def your_pre_processing(s):
    return s

def assign_confidence(match, pattern):
    if pattern == r"sum of the two numbers is: (\d+)":
        return 1 
    elif pattern == r"sum is (\d+)":
        return 0.9  
    elif pattern == r"Answer: (\d+)" or r"answer is (\d+)":
        return 0.8
    elif pattern == r"equals (\d+)":
        return 0.7  
    elif pattern == r"total: (\d+)":
        return 0.6
    else:
        return 0.5  # Default for less specific patterns
  
def your_post_processing(output_string):
    """Returns the post processing function to extract the answer for addition
    Returns:
        For: the function returns extracted result
    Note:
        do not attempt to "hack" the post processing function
        by extracting the two given numbers and adding them.
        the autograder will check whether the post processing function contains arithmetic additiona and the graders might also manually check.
    """
    patterns = [r"sum is (\d+)", r"total: (\d+)", r"equals (\d+)", r"Answer: (\d+)", r"answer is (\d+)", r"sum of the two numbers is: (\d+)"]

    potential_answer = []
    
    for pattern in patterns:
        matches = re.findall(pattern, output_string)
        for match in matches:
            confidence = assign_confidence(match, pattern)
            potential_answer.append((int(match), confidence))

    if potential_answer:
        return max(potential_answer, key=lambda x: x[1])[0]

    only_digits = re.sub(r"\D", "", output_string.splitlines()[0])

    try:
        res = int(only_digits)
    except:
        res = 0
    return res
