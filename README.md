# Searching for digitized books by OCLC identifier

This repository has scripts to search the following websites for digitized books by their OCLC numbers.

- [Google Books](https://books.google.com/)
- [HathiTrust](https://www.hathitrust.org/)
- [Internet Archive](https://archive.org/)

***

## Data

### Formatting your OCLC numbers for searching.

OCLC identifiers should be entered into a spreadsheet in a column called 'oclc_id'. The OCLC identifiers should not have any prefixes like "ocm", "on", or "(OCoLC)". Save your spreadsheet as a UTF-8 encoded CSV. It does not matter if the identifiers are saved as integers or strings, as the scripts automatically converts identifiers into strings.

When your CSV is ready, put it in the same folder location as the scripts below on your local system.

### Test data

There is a folder called "test-data" in the repository with test data and results. This can help with formatting and troubleshooting the scripts on your local system.
- test.csv: A CSV with 9 items (3 items findable by OCLC number for each website). These items were selected at random.
- hathiTrustResults_test.csv: The results from running test.csv against searchHathiTrustByOCLC.py.
- googleBooksResults_test.csv: The results from running test.csv against searchGoogleBooksByOCLC.py.
- internetArchiveResults_test.csv: The results from running test.csv against searchInternetArchivesByOCLC.py.

***

## Scripts

## Requirements
- Python 3+
- [pandas](https://pandas.pydata.org/) library
- [requests](https://requests.readthedocs.io/en/latest/) library
- [internetarchive](https://archive.org/services/docs/api/internetarchive/) library

## searchGoogleBooksByOCLC.py

Note: There is a 60-second pause after searching a set of 100 OCLC numbers as Google Books limits the number of books searched per minute via API. So, if you have 1000 OCLC identifiers to search, this script will take at least 10 minutes. I'm sure there is a better solution, I just don't know what it is.

## searchHathiTrustByOCLC.py

## searchInternetArchiveByOCLC.py

## combineMyResults.py