from typing import List
import requests
from bs4 import BeautifulSoup
from common1 import NodeContent,NodeContentDetail,NodePushComment
FIRST_N_PAGE=10 # 爬取前10页
BASE_HOST="https://www.ptt.cc"  # 改回https
HEADERS={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def parse_node_use_bs(html_content:str)->NodeContent:
    note_content=NodeContent()
    soup=BeautifulSoup(html_content,"lxml")
    print(soup.select("div.r-ent div.title a"))
    note_content.title = soup.select("div.r-ent div.title a")[0].text.strip() if len(
        soup.select("div.r-ent div.title a")) > 0 else ""
    note_content.author=soup.select("div.r-ent span.author")[0].text.strip() if len(
        soup.select("div.r-ent span.author"))>0 else ""
    note_content.publish_date = soup.select("div.r-ent div.meta div.date")[0].text.strip() if len(
        soup.select("div.r-ent div.meta div.date")) > 0 else ""
    note_content.detail_link = soup.select("div.r-ent div.title a")[0]["href"] if len(
        soup.select("div.r-ent div.title a")) > 0 else ""
    return note_content

def get_previous_page_number()->int:
    url="/bbs/stock/index.html"
    response=requests.get(url=BASE_HOST+url,headers=HEADERS)
    if response.status_code!=200:
        raise Exception("send request got error")
    soup=BeautifulSoup(response.text,"lxml")
    css_selector="#action-bar-container > div > div.btn-group.btn-group-paging > a:nth-child(2)"
    pagination_link=soup.select(css_selector)[0]["href"].strip()
    previos_page_number=int(pagination_link.replace("/bbs/Stock/index","").replace(".html",""))
    return previos_page_number

def fetch_bbs_note_list(previous_page_number:int)->List[NodeContent]:
    notes_list:List[NodeContent]=[]
    start_page_number=previous_page_number+1
    end_page_number=start_page_number-FIRST_N_PAGE
    print(start_page_number,end_page_number)
    for page_number in range(start_page_number,end_page_number,-1):
        print(f"开始获取第{page_number}页的帖子内容")
        url=f"/bbs/Stock/index{page_number}.html"
        response=requests.get(url=BASE_HOST+url,headers=HEADERS)
        if response.status_code!=200:
            print(f"获取第{page_number}页的帖子内容失败")
            continue
        soup=BeautifulSoup(response.text,"lxml")
        all_node_elements=soup.select("div.r-ent")
        for node_element in all_node_elements:
            node_content:NodeContent=parse_node_use_bs(node_element.prettify())
            notes_list.append(node_content)
        print(f"获取第{page_number}页的帖子内容成功")
    return notes_list

def fetch_bbs_note_detail(note_content: NodeContent) -> NodeContentDetail:
    """
    获取帖子详情页数据
    :param note_content:
    :return:
    """
    print(f"开始获取帖子 {note_content.detail_link} 详情页....")
    note_content_detail = NodeContentDetail()

    # note_content有值的, 我们直接赋值，就不要去网页提取了，能偷懒就偷懒（初学者还是要老老实实的都去提取一下数据）
    note_content_detail.title = note_content.title
    note_content_detail.author = note_content.author
    note_content_detail.detail_link = BASE_HOST + note_content.detail_link

    response = requests.get(url=BASE_HOST + note_content.detail_link, headers=HEADERS)
    if response.status_code != 200:
        print(f"帖子：{note_content.title} 获取异常,原因：{response.text}")
        return note_content_detail

    soup = BeautifulSoup(response.text, "lxml")
    note_content_detail.publish_datetime = soup.select("#main-content > div:nth-child(4) > span.article-meta-value")[
        0].text

    # 处理推文
    note_content_detail.push_comment = []
    all_push_elements = soup.select("#main-content > div.push")
    for push_element in all_push_elements:
        note_push_comment = NodePushComment()
        if len(push_element.select("span")) < 3:
            continue

        note_push_comment.push_user_name = push_element.select("span")[1].text.strip()
        note_push_comment.push_cotent = push_element.select("span")[2].text.strip().replace(": ", "")
        note_push_comment.push_time = push_element.select("span")[3].text.strip()
        note_content_detail.push_comment.append(note_push_comment)

    print(note_content_detail)
    return note_content_detail

def run_crawler(save_notes:List[NodeContentDetail]):
    previous_number:int= get_previous_page_number()
    print(previous_number)
    note_list:List[NodeContent]=fetch_bbs_note_list(previous_number)
    for note_content in note_list:
        if not note_content.detail_link:
            continue
        note_content_detail = fetch_bbs_note_detail(note_content)
        save_notes.append(note_content_detail)

    print("爬取完成")


if __name__=="__main__":
    save_notes:List[NodeContentDetail]=[]
    run_crawler(save_notes)



