# Wechat telephone using 
import itchat

def main():
    itchat.auto_login()
    send_hello_message()
    search_friends()

def send_hello_message():
    itchat.send('Hello, filehelper', toUserName='filehelper')

def search_friends():
    friend_by_username = itchat.search_friends(userName='@abcdefg1234567')
    friend_by_account = itchat.search_friends(wechatAccount='littlecodersh')
    friend_by_name_and_account = itchat.search_friends(name='LittleCoder机器人', wechatAccount='littlecodersh')

    print("Search results by username:", friend_by_username)
    print("Search results by account:", friend_by_account)
    print("Search results by name and account:", friend_by_name_and_account)

if __name__ == "__main__":
    main()