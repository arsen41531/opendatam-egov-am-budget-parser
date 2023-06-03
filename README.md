opendatam-egov-am-budget-parser
-------------------------------

This script's purpose is to extract Armenian goverment budget data from interactive budget website (e-gov.am/interactive-budget/)
The script is written using Python `3.11.1`. 

You must first install dependencies:

```console
$ pip install -r requirements.txt
```
And then run the script:

```console
$ ./budget_parser.py
```

The script produces data files in the following format:
```
{budget_year}-{data_source}.{csv,json}
```
And it places them under `_data/{current_date}/` folder.




