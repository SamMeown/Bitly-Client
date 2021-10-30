# Bitly-Client
A little console [*Bitly*](https://app.bitly.com) client which allows to shorten urls and count shortened bitlink clicks.:link::scissors:  
  

### How to install and setup
Python3 should already be installed. Then open terminal window and use `pip` to install dependencies:  
```
pip install -r requirements.txt
```
Client will need yout Bitly [*access token*](https://app.bitly.com/settings/api) to communicate with bitly API. You can setup your token using environment valiable `GENERAL_TOKEN`, or just create `.env` file and place it there like this:  
```
GENERAL_TOKEN=<Your Token>
```

### Usage
Interactive mode:  
```
python3 bclient.py
```
Enter url to get shortened bitlink or enter bitlink to get corresponding click count.  
You can also set a link via `--link` argument:  
```
python bclient.py --link https://www.google.com
```
