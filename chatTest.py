import itchat, time
from itchat.content import *
import config


def getRobotInfo():
    if not config.robot:
        config.robot = itchat.search_mps(name=config.robotName)[0]
    return config.robot.UserName

def getMeInfo():
    if not config.meInfo:
        config.meInfo = itchat.search_friends()
    return config.meInfo.UserName

@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def text_reply(msg):
    fromUser = msg.FromUserName
    toUser = msg.ToUserName
    robot = getRobotInfo()
    content = msg.Content
    print('接收到信息:' + content)
    print('等待回复……')
    me = getMeInfo()
    if fromUser != me:
        # 将映射关系存储到字典中
        config.waitList.append(fromUser)
        # 将接收到的信息发送给小冰，等待小冰回复之后，将小冰的回复返回此用户
        itchat.send(content, robot)


@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    fromUser = msg.FromUserName
    toUser = msg.ToUserName
    robot = getRobotInfo()
    content = msg.Content
    me = getMeInfo()
    if fromUser != me:
        # 将映射关系存储到字典中
        config.waitList.append(fromUser)
        # 将接收到的信息发送给小冰，等待小冰回复之后，将小冰的回复返回此用户
        fileDir = '%s%s' % (msg['Type'], int(time.time()))
        print('接收到文件:' + content)
        print('等待回复……')
        msg['Text'](fileDir)
        itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', fileDir), robot)


@itchat.msg_register(TEXT,isMpChat=True,isGroupChat=True)
def text_reply(msg):
    # noinspection PyBroadException
    try:
        fromUser = msg.FromUserName
        toUser = msg.ToUserName
        robot = getRobotInfo()
        me = getMeInfo()
        content = msg.Content
        print(msg)
        #msg.user.send('%s: %s' % (msg.type, msg.text))
        # 来自robot的回复,获取回复，将信息发送给用户
        if fromUser == robot and len(config.waitList) > 0:
            #将回复发送给用户
            #config.contentList.append(content)
            itchat.send(content, config.waitList.pop())
            print('回复完毕:' + content)
    except Exception as e:
        raise e


itchat.auto_login(hotReload=True)
itchat.run()

if __name__ == '__main__': print('success')
