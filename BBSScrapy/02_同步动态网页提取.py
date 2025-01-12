import csv
import time
from typing import Any, Dict, List

import requests

from common2 import SymbolContent,make_req_params_and_headers


HOST="https://query1.finance.yahoo.com"
SYMBOL_QUERY_API_URI="/v1/finance/screener"
PAGE_SIZE=100

# 解析动态网页
def parse_symbol_content(quote:Dict)->SymbolContent:
    symbol_content=SymbolContent()
    symbol_content.symbol = quote["symbol"]
    symbol_content.name = quote["shortName"]
    symbol_content.price = quote["regularMarketPrice"]["fmt"]
    symbol_content.change_price = quote["regularMarketChange"]["fmt"]
    symbol_content.change_percent = quote["regularMarketChangePercent"]["fmt"]
    symbol_content.market_price = quote["marketCap"]["fmt"]
    return symbol_content
    
# 获取数据列表
def fetch_currency_data_list(max_total:int)->List[SymbolContent]:
    symbol_data_list:List[SymbolContent]=[]
    page_start=0
    while page_start<=max_total:
        response_dict:Dict=send_request(page_start=page_start,page_size=PAGE_SIZE)
        for quote in response_dict["finance"]["result"][0]["quotes"]:
            parsed_content:SymbolContent=parse_symbol_content(quote)
            print(parsed_content)
            symbol_data_list.append(parsed_content)
            print(f"已获取到{len(symbol_data_list)}条数据")
        page_start+=PAGE_SIZE
    return symbol_data_list


def send_request(page_start: int, page_size: int) -> Dict[str, Any]:
    req_url=HOST+SYMBOL_QUERY_API_URI
    common_params, headers, common_payload_data= make_req_params_and_headers()
    common_payload_data["offset"]=page_start
    common_payload_data["size"]=page_size
    response=requests.post(url=req_url,params=common_params,json=common_payload_data,headers=headers)
    if response.status_code!=200:
        raise Exception(f"请求失败，状态码:{response.status_code},错误信息:{response.text}")
    try:
        response_dict:Dict=response.json()
        return response_dict
    except Exception as e:
        raise e


# 获取最大总数
def get_max_total_count()->int:
    print("获取最大总数")
    try:
        response_dict:Dict=send_request(page_start=0,page_size=PAGE_SIZE)
        total_count=response_dict["finance"]["result"][0]["total"]
        print(f"获取最大总数成功，总数:{total_count}")
        return total_count
    except Exception as e:
        print(f"获取最大总数失败，错误信息:{e}")
        raise e
    




# 保存数据到csv
def save_data_to_csv(save_file_name:str,data_list:List[SymbolContent])->None:
    with open(save_file_name,mode="w",newline="",encoding="utf-8") as file:
        writer=csv.writer(file)
        writer.writerow(SymbolContent.get_fields())
        for symbol in data_list:
            writer.writerow([symbol.symbol,symbol.name,symbol.price,symbol.change_price,symbol.change_percent,symbol.market_price])

# 运行爬虫
def run_crawler(save_file_name:str)->None:
    max_total:int=get_max_total_count()
    data_list:List[SymbolContent]=fetch_currency_data_list(max_total)
    save_data_to_csv(save_file_name,data_list)

if __name__=="__main__":
    timestamp=int(time.time())
    save_file_name=f"symbol_data_{timestamp}.csv"
    run_crawler(save_file_name)
    
