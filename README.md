# Codecks Import


This script imports cards from a CSV file into Codecks. Right now it ONLY imports Titles, and adds them to the deck you specify.  Your CSV file should be a simple list of tasks, one per line. It might add in more fields as the use case arises.

## USAGE
```
Usage: python codecksimport.py <access_token> <org> <csv_file> <deck_search>
       access_token: Your Codecks API access token
       org: Your Codecks organisation name (>>yoursubdomain<<.codecks.io)
       csv_file: The path to the CSV file containing the card data
       deck_search: The name of the deck to add cards to

Example: python codecksimport.py 1234567890abcdef mycompany cards.csv MyDeck

```
Details on how to obtain your Codecks access token can be found here: (https://manual.codecks.io/api/)
---
Codecks is a playfully simple project management tool for teams
https://codecks.io

Copyright (c) 2023 Phil Merricks

I am not affiliated with Codecks in any way.
