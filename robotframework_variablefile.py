# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def catenate(string1,string2):
    result = string1+string2
    return result

username = "fengguangke"    #字符串类型的scalar变量${username}
password = "fengguangke2010"    #字符串类型的scalar变量${password}
age = 26    #int类型变量 ${age}
address = "广东省深圳市".decode("utf-8")  #中文需要转换成unicode编码
hobby = ['badminton','movie','walk'] #list变量 ${hobby}
userinfo_robot = {"username":"fengguangke","password":"fengguangke2010"}    #dict变量${userinfo_robot}
LIST__hobbies = ['badminton','movie','walk']  #以LIST__开始的变量list变量：${hobbies}
DICT__userinfos_robot = {"username":"fengguangke","password":"fengguangke2010"} #以DICT_开始的变量dict变量${userinfos_robot}
catenate_str = catenate("feng","guangke")

