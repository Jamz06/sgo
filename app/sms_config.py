# -*- coding: utf-8 -*-
###SMS CONF###

from urllib import request
from urllib.parse import quote

class Sms():
    '''
    Класс смс
    '''
    sender = "rodn.svyaz"
    gwhost = "http://kannel1.cocos.perm.ru"
    gwport = ":80"
    gwpath = "/cgi-bin/sendsms"
    user = "user"
    password= "ppaSsWoRdd"

    def send(self, text, number):

        send_url = self.gwhost + self.gwport + self.gwpath + '?username=' + \
               self.user + '&validity=2880&password=' + self.password + \
               '&text=' + quote(text) +  '&to=' + number + '&from=' + self.sender + '&coding=2&charset=UTF-8'
        print(send_url)
        response = request.urlopen(send_url)
        return response


if __name__ == '__main__':
    sms = Sms()
    resp = sms.send('тестовое', '79519429049')
    print(resp)