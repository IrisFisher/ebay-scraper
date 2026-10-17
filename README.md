This program was created for [Project 2](https://csci40.rtealwitter.com/projects/02_webscraping/project.html#build-the-scraper) in R. Teal Witter's course CSCI40, "Computing for the Web."

'ebay-dl.py' scrapes the first 10 pages of search results for a given search term and creates a JSON file ('searchterm.json') listing the name, price (in cents), status, shipping cost (in cents) return policy and number of items sold of each product listing.

To run 'ebay-dy.py' on a search term "SEARCH TERM," run the following command from the terminal:
```
python ebay-dl.py "SEARCH TERM"
```

To run ebay-dy.py on the provided practice files run:
```
python ebay-dl.py "SEARCH TERM" --pages_dir practice-page
```

The three files 'garden tools.json', 'poster.json', and 'stuffed animal.json' are examples of the output of ebay-dl.py run on the practice files. Their contents is the same because the output of the practice files doesn't change depending on the search term. They were generated with the following commands:

'garden tools.json':
```
python ebay-dl.py "garden tools" --pages_dir practice-page
```

'poster.json':
```
python ebay-dl.py "poster" --pages_dir practice-page
```

'stuffed animal.json':
```
python ebay-dl.py "stuffed animal" --pages_dir practice-page
```