from typing import List

# 帖子简介
class NodeContent:
    title:str="" # 帖子标题
    author:str="" # 帖子作者
    publish_date:str="" # 帖子发布时间
    detail_link:str="" # 帖子详情链接
    def __str__(self): # 打印帖子简介
        return f"""
        title:{self.title}
        author:{self.author}
        publish_date:{self.publish_date}
        detail_link:{self.detail_link}
        """
    
# 推文评论
class NodePushComment:
    push_user_name:str="" # 推文评论用户名
    push_content:str="" # 推文评论内容
    push_time:str="" # 推文评论时间
    def __repr__(self): # 打印推文评论内容
        return f"NotePushComment(push_user_name={self.push_user_name}, push_content={self.push_content}, push_time={self.push_time})"
    
# 帖子详情
class NodeContentDetail:
    title:str="" # 帖子标题
    author:str="" # 帖子作者
    publish_date:str="" # 帖子发布时间
    detail_link:str="" # 帖子详情链接
    push_comment:List[NodePushComment] # 推文评论
    def __str__(self): # 打印帖子详情
        return f"""
        Title:{self.title}
        User:{self.author}
        Publish Datetime:{self.publish_date}
        Detail Link:{self.detail_link}
        Push Comments:{self.push_comment}
        """
