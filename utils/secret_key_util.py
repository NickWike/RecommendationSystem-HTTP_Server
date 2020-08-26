from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from utils.my_path import get_root_path
import base64
import os
import hashlib

"""
    @author:zh123
    @date: 2020-02-21
    @description:
        1.主要是对一些加密算法进行一定的封装
        2.MyRSA  非对称加密
        3.MD5 对称加密主
"""


class MyRSA:
    secret_key_save_dir = get_root_path() + "/SecretKey"        # 秘钥存放位置

    now_public_pem = None                       # 当前的公钥
    now_private_pem = None                      # 当前的私钥
    cipher_decrypt = None                       # 解码器

    @staticmethod
    def init_secret_key():
        status = True                                                               # 初始化是否成功标识
        try:
            if not os.path.exists(MyRSA.secret_key_save_dir):
                os.mkdir(MyRSA.secret_key_save_dir)                                 # 创建秘钥存放的文件夹

            random_generator = Random.new().read                                    # 生成一个随机因子
            rsa = RSA.generate(1024, random_generator)                              # 构造一个rsa对象
            private_pem = rsa.exportKey()                                           # 初始化公私钥信息
            public_pem = rsa.publickey().exportKey()
            MyRSA.now_private_pem = private_pem
            MyRSA.now_public_pem = public_pem
            MyRSA.cipher_decrypt = Cipher_pkcs1_v1_5.new(RSA.importKey(private_pem))    # 初始化解码器
            with open(MyRSA.secret_key_save_dir + "/public_key.pem", 'wb') as f:
                f.write(public_pem)                                                     # 写入公钥

            with open(MyRSA.secret_key_save_dir + "/private_key.pem", "wb") as f:
                f.write(private_pem)                                                    # 写入私钥
        except Exception as e:
            print("创建RSA公钥和私钥失败 ->　", e)                                          # 捕获异常
            status = False
        finally:
            return status

    @staticmethod
    def decryption(cipher_bytes: bytes) -> tuple:
        real_str = None                             # 解码后真实的字符串
        status = True                               # 解码状态
        try:
            real_str = MyRSA.cipher_decrypt.decrypt(base64.b64decode(cipher_bytes), "ERROR").decode()   # 进行解码
        except Exception as e:
            print("解密失败", e)                      # 解密异常
            status = False
        return status, real_str

    @staticmethod
    def encryption(real_text: str, public_pem: str) -> tuple:
        cipher_bytes = None                                 # 加密后的数据
        status = True                                       # 加密状态
        try:
            rsa_key = RSA.importKey(public_pem)             # 导入公钥
            cipher = Cipher_pkcs1_v1_5.new(rsa_key)         # 构建加密器
            cipher_bytes = base64.b64encode(cipher.encrypt(real_text.encode("utf-8")))  # 进行加密
        except Exception as e:
            status = False                                  # 加密失败
            print("加密失败",e)
        finally:
            return status, cipher_bytes


class MyMD5:

    @staticmethod
    def change_to_md5(s: str) -> (bool, str):
        result = None                                       # 返回数据
        status = True                                       # 状态码
        try:
            s_bytes = s.encode("utf-8")
            result = hashlib.md5(s_bytes).hexdigest()       # 将给的字符串转换成md5码
        except Exception as e:
            status = False                                  # 转换异常
        finally:
            return status, result


if __name__ == '__main__':
    p = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3LWdkBz00JUS1yLCMH0D
9ZHjzjD/C/6gJqIL27VZ/c2I12mR0blWP8fTYd/gGjiplBfkm2qeE57vYomd7HSw
P2Jdpj5Z1mRHMJi8Q8MbSl67SxYIqAPboC8HBMXAdkiJldIK6jFa/YoCqP51ouE9
iZ/nOKUgmccIHPLuI3kVqLypKeqnNA03vI14DnSSogiYGSckQdAzFIrOCSC4XOzw
U4WjMhoJfFpTVEOXNjIEq+qUquukhJWe/Br1DUJXy0fZ34pOayPUe5wmi7Ppe8Qm
PO/lSWYA0zPcMIZSDVgThsSKTBy11YY2u9qUwwc1XX0s7oLMULmT2RhzmBFVUY3Y
vQIDAQAB
-----END PUBLIC KEY-----"""
    l = "T1JGTDhySHdFelhWa0h2T2dUNzBLZk5VclQvZVBvazI3cWtta1RZbnZBTHVGZUhQRkhhZHBWVEVueWUwaXBYbHlvS1ZtM3gxZmtoQwpWWmFuTHR1bC9UcG1rV2l1T1NNV0xtcElhR21qNVJocytOSUdiZXNxQXo1ajNGTkNGaWMyWFdnRjY2b0tFQklaMEI0b0F2OXJpTE9ICm1uMGtlZmVRZFlsdmh2MXVrR3M9Cg=="

    print(MyRSA.encryption("123456",p))
    # print(MyMD5.change_to_md5("123456"))