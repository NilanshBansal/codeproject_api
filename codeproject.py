import requests
from bs4 import BeautifulSoup
import json
import random
from pymongo import MongoClient
import urllib
import sys
import datetime

mongo_client = MongoClient('localhost', 27017)

user_agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0)", "Mozilla/5.0 (Windows NT 6.1; Win64; x64)", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko)"
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko)",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko)", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)",
]

ico_projects = ['Bitcoin', 'Ethereum', 'XRP', 'Bitcoin Cash', 'EOS', 'Stellar', 'Litecoin', 'Tether', 'Cardano', 
                'Monero', 'TRON', 'IOTA', 'Dash', 'Binance Coin', 'NEO', 'Ethereum Classic', 'NEM', 'Tezos', 'VeChain',
                'Dogecoin', 'Zcash', 'OmiseGO', 'Bitcoin Gold', 'Maker', 'Bytecoin', 'Ontology', 'Lisk', '0x','Decred',
                'Qtum', 'Bitcoin Diamond', 'BitShares', 'Nano', 'Zilliqa', 'Siacoin', 'DigiByte', 'ICON', 'Steem', 
                'Aeternity', 'Verge', 'Waves', 'Pundi X', 'Bytom', 'Electroneum', 'Basic Attention Token', 
                'Metaverse ETP', 'Holo', 'Stratis', 'Golem', 'Augur', 'Status', 'Populous', 'Komodo', 'TrueUSD', 
                'Chainlink', 'Waltonchain', 'Cryptonex', 'Ardor', 'Wanchain', 'Mithril', 'ReddCoin', 'KuCoin Shares',
                'IOST', 'MaidSafeCoin', 'ETERNAL TOKEN', 'HyperCash', 'MOAC', 'Aion', 'Aurora', 'Huobi Token', 'aelf',
                'Loopring', 'Bancor', 'DigixDAO', 'CyberMiles', 'GXChain', 'RChain', 'FunFair', 'Decentraland', 
                'Dropil', 'Dentacoin', 'QASH', 'Horizen', 'Nebulas', 'Ark', 'TenX', 'MonaCoin', 'Crypto.com', 
                'Theta Token', 'Nxt', 'Loom Network', 'Noah Coin', 'Power Ledger', 'WAX', 'Bitcoin Private', 
                'Mixin', 'PIVX', 'Elastos', 'Dai', 'Gas']

def insert_project(project_name,mongo_client):

    ## Insert in Databse 
    db = mongo_client.copernicus
    collection = db.blockchain_projects
    project_in_db = collection.find_one({"project": project_name})
    if project_in_db is None:
        collection.insert_one({"project": project_name})


## Delete Blockchain project name from Database
def delete_project(project_name,mongo_client):

    ## Deleting from Database
    db = mongo_client.copernicus
    collection = db.blockchain_projects
    collection.delete_one({"project":project_name})


def get_access_token():
    
    data = {
        "grant_type":"client_credentials",
        "client_id":"wudREc7Zqge_iJgt30IyRWxldjmK1vo2",
        "client_secret":"DSVRoGaLT8umByUFJsVr73CxUGcNLboRZ6eA2mcC_Q30KERoo8JbM6AfJkBUi1We"
    }
    
    url = 'https://api.codeproject.com/token'
    try:
        re = requests.post(url, data=data, headers={'User-Agent': random.SystemRandom().choice(user_agents)})
        access_token = json.loads(re.text)['access_token']
        return access_token
    except Exception as e:
        print(e)
        sys.exit(1)



def get_data():
    access_token = get_access_token()
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.copernicus
    projects_db = []
    projects_collection = db.blockchain_projects
    for project in projects_collection.find():
        projects_db.append(project['project'])
        
    ## Inserting project data to database 
    collection = db.codeproject_projects_reports
    
    for project in projects_db:
        query = project
        query = urllib.parse.quote_plus(query)
        url = 'https://api.codeproject.com/v1/Articles?tags=%s' %  query
        
        headers_get_posts = {
            "Authorization":"Bearer " + access_token,
            'User-Agent':random.SystemRandom().choice(user_agents)
        }
        
        try:
            response = requests.get(url, headers=headers_get_posts)
            result = json.loads(response.text)
            
            date = datetime.date.today().strftime ("%Y-%m-%d")
            project_in_db = collection.find_one({"project_name": project,"date":date})
            
            if project_in_db == None:
                collection.insert_one({'project_name': project, 'data': result['items'],'date':date})
            else:
                collection.update_one({'project_name': project}, {'$set': {'data': result['items']}})
        
        except Exception as e:
            print(e)
            sys.exit(1)

