#!/usr/bin/env python

import argparse
import json
import sys
import os

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def get_config(filename):
    """Return JSON of a paginated set of blog's posts."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return json.loads(open(script_dir + '/../config/' + filename).read())

def format_date(datestring):
    # Formatted date should look like: 2011-11-20 17:06:58
    return "%s-%s-%s %s:%s:00" % (datestring[:4], datestring[5:7], datestring[8:10], datestring[11:13], datestring[14:16])    

def create_target_dir(datestring, yaki_root):
    # Path should look like <yaki/blog>/2011/11/20/1760
    path = "%s/%s/%s/%s/%s%s" % (yaki_root, datestring[:4], datestring[5:7], datestring[8:10], datestring[11:13], datestring[14:16])
    try:
        os.makedirs(path, 0755);
        return path
    except OSError:
        return False

def write_post(contents, full_path):
    filename = "index.txt"
    try:
        file = open(full_path + "/" + filename, "w")
        file.writelines(contents)
        file.close()
        return True
    except TypeError:
        return False
         
def create_text(post, yaki_root):

    formatted_date = format_date(post["date"])
    contents = []
        
    contents.append(removeNonAscii("From: Matthew Finlayson\n"))
    if not post['title']:
        return False
    else:       
        contents.append(removeNonAscii("Title: %s\n" % post['title']))
    contents.append(removeNonAscii("Date: %s\n" % formatted_date))
    if not post["tags"]:
        contents.append(removeNonAscii("Tags:\n"))
    else:    
        contents.append(removeNonAscii("Tags: %s\n" % ', '.join(post["tags"])))
    contents.append(removeNonAscii("Content-Type: text/html\n"))
    contents.append("\n")
    contents.append(removeNonAscii("%s" % post['body']))
    
    full_path = create_target_dir(formatted_date, yaki_root)
    
    if full_path:
        return write_post(contents, full_path)
    else:
        return False 
    
def create_video(post, yaki_root):
    formatted_date = format_date(post["date"])
    contents = []
    contents.append(removeNonAscii("From: Matthew Finlayson\n"))
    contents.append(removeNonAscii("Title: Video from - %s\n" % formatted_date))
    contents.append(removeNonAscii("Date: %s\n" % formatted_date))
    if not post["tags"]:
        contents.append(removeNonAscii("Tags:\n"))
    else:    
        contents.append(removeNonAscii("Tags: %s\n" % ', '.join(post["tags"])))
    contents.append(removeNonAscii("Content-Type: text/html\n"))
    contents.append("\n")
    contents.append("%s\n" % post['player'][2]['embed_code'])
    if not post['caption']:
        pass
    else:
        contents.append(removeNonAscii("%s" % post['caption']))
    
    full_path = create_target_dir(formatted_date, yaki_root)
    if full_path:
        return write_post(contents, full_path)
    else:
        return False 
    
def populate_yaki(file, yaki_root):
    json_str = open(file).read()
    json_obj = json.loads(json_str)
        
    for raw_post in json_obj:
        if raw_post['type'] == 'text':
            create_text(raw_post, yaki_root)
        elif raw_post['type'] == 'video':
            create_video(raw_post, yaki_root)

if __name__ == '__main__':
    configfile='../config/config.json'
    config = get_config(configfile)
    populate_yaki(config['backup_file'], config['yaki_root'])
