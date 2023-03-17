#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(re)Created on Thursday, 16 March 2023
Copyright (c) 2023 Phil Merricks
I am not affiliated with Codecks in any way
This script imports cards from a CSV file into Codecks
Codecks is a playfully simple project management tool for teams
https://codecks.io
Version 0.1
"""

import sys
import requests
import csv
import time
import json
import logging

# Set up logging
logging.basicConfig(filename='codecksimport.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG) # TODO: add logging output throughout the script

# Check if the correct number of arguments were passed to the script
if len(sys.argv) == 1:
    print("Usage: python <script_name> <access_token> <org> <csv_file> <deck_search>")
    print("       access_token: Your Codecks API access token")
    print("       org: Your Codecks organization name")
    print("       csv_file: The path to the CSV file containing the card data")
    print("       deck_search: The name of the deck to add cards to")
    print("Example: python codecksimport.py 1234567890abcdef mycompany cards.csv 'My Deck'")
    sys.exit()

# Set up the Codecks API endpoint and access token
api_endpoint = "https://api.codecks.io"
access_token = sys.argv[1]
account = sys.argv[2]
csvfile = sys.argv[3]
deck_search = sys.argv[4]

# Set up the headers for the API request
headers = {
    "X-Auth-Token": access_token,
    "X-Account": account,
    "Content-Type": "application/json",
}


# Set up the URL for creating a new card in Codecks
create_card_url = f"{api_endpoint}/dispatch/cards/create"

# Set up the URL for searching for a deck in Codecks
search_decks_url = api_endpoint

search_query = json.dumps({
  "query": {
    "_root": [
      {
        "account": [
          {"decks({\"title\":{\"op\":\"contains\",\"value\":\""+deck_search+"\"}})": ["title"]}
        ]
      }
    ]
  }
})

# Test the search query to make sure it's valid JSON
try:
    json.dumps(search_query)
except:
    print(f"Error: Invalid search query: {search_query}")
    exit()
    

# Send the API request to search for a deck in Codecks
response = requests.post(search_decks_url, headers=headers, data=search_query)

decksearch_response = response.json()
if response.status_code == 200:
    # If the deck key is not found, the search was unsuccessful
    if 'deck' not in decksearch_response:
        print(f"Error searching for deck name containing '{deck_search}'")
        print('This is likely due to no results being found, or an invalid search query')
        exit()
    decksearch_results = (decksearch_response['deck'])
    # count the number of decks found
    decksfound = len(decksearch_results)
    # If more than one result is returned, make a list of their names and ids
    if decksfound > 1:
        print(f"Found {decksfound} decks containing '{deck_search}'")
        print(f"Decks found:") # print the name and id of each deck found
        for k, v in decksearch_results.items():
            print(v['title'], v['id'])
        print(f"Be more specific to avoid adding cards to the wrong deck, or name the deck more uniquely in Codecks.")
        exit()
    # If only one result is returned, get the name and id
    else:
        k, v = next(iter(decksearch_results.items())) # get the first item in the dictionary
        decktitle = v['title'] # get the title of the deck
        deckid = v['id'] # get the ID of the deck
        print(f"Found deck '{decktitle}' with ID {deckid}")

else:
    print(f"Error searching for deck containing '{deck_search}': {response.text}")
    exit()

# Open the CSV file and read each line
with open(csvfile, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    # Count the number of lines in the CSV file
    numcards = sum(1 for line in csv_file)
    # Rewind the file so we can read it again
    csv_file.seek(0)
    #
    #  print number of cards to be created and ask for confirmation, allow escape to quit
    print(f"About to create {numcards} cards in deck '{decktitle}' with ID {deckid}")
    print("Press any key to continue, or press Ctrl+C to quit")
    input()
    for row in csv_reader:
        # Create the payload for the API request
        payload = {
            "addAsBookmark": False,
            # "assigneeId": "",
            # "attachments":[],
            # "childcards":[],
            "content": f"{row[0]}", # surround the card content in quotes to avoid issues with commas in the content
            "deckId": deckid,
            # "effort": "",
            # "fakeCoverFileId": "",
            # "inDeps":[],
            # "isDoc": False,
            # "masterTags":[],
            # "milestoneId": "",
            # "outDeps": [],
            # "priority": "",
            # "putInQueue": False,
            # "putOnHand": False,
            # "sessionId": "",
            # "subscribeCreator": False,
            # "userId": "",
            # Add any other fields you want to use as card attributes
        }
        # Test the payload to make sure it's valid JSON
        try:
            json.dumps(payload)
        except:
            print(f"Error: Invalid payload: {payload}")
            exit()
   
        # Send the API request to create a new card in Codecks
        response = requests.post(create_card_url, json=payload, headers=headers)

        # Check if the API request was successful
        print(response.status_code)
        if response.status_code == 200:
            print(f"Card '{payload['content']}' created successfully!")
        else:
            print(f"Error creating card '{payload['content']}': {response.text}")
            
        # Rate limit to <40 Requests every 5 seconds
        time.sleep(0.125)
