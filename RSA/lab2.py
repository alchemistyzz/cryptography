from math import gcd
import random

def hex2int(x: str) -> int:
        # hex字符串转换为整数
        return int(x, 16)

def int2hex(x: int) -> str:
        # 整数转换为hex字符串
        return hex(x)[2:]

def hex2bin(x: str) -> str:
        # hex字符串转换为字节数组
        if len(x) & 1:
            x = "0" + x
        buffer = bytearray()
        for i in range(0, len(x), 2):
            buffer.append(hex2int(x[i:i+2]))
        x = bytes(buffer)
        return x.decode()
##快速幂
def quick_mod(base,exp,mod):
    ans  = 1
    while(exp):
        if(exp&1):
            ans = (ans * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return ans 

##找到大素数的方法

def MillerRabin( num: int, times=8):
        # Miller-Rabin素性检验
        # return False if n is not prime
        m = num-1
        k = 0
        while m & 1 == 0:
            m >>= 1
            k += 1

        for _ in range(times):
            x = random.randrange(2, num)
            x = quick_mod(x, m, num)
            for _ in range(k):
                y = (x*x) % num
                if y == 1 and x != 1 and x != num-1:
                    return False
                x = y
            if y != 1:
                return False
        return True

#判定是否为素数的方法
def isNotPrime(num:int):
    smallPrime=[2,3,5,7,11,13,17]
                
    for p in smallPrime:
            d, m = divmod(num, p)
            if m == 0:
                if d == 1:
                    return False
                else:
                    return True

    # Miller-Rabin
    isP = MillerRabin(num)
    return  not isP

#找到大素数
def find_prime(low_bits,high_bits):
    low_num = 1 << low_bits 
    high_num = 1 << high_bits
    n = random.randrange(low_num,high_num)

    while isNotPrime(n):
        # print(n)
        n = random.randrange(low_num,high_num)
    return n


#扩展欧几里得求乘法逆元，也是在求私钥
def extended_euclid(m,b):
    if b>m:
        m,b=b,m
    x1,x2,x3=1,0,m
    y1,y2,y3=0,1,b
    while True:
        if y3==0:
            return None
        if y3==1: 
            return y2
        Q=x3//y3
        t1,t2,t3=x1-Q*y1,x2-Q*y2,x3-Q*y3
        x1,x2,x3=y1,y2,y3
        y1,y2,y3=t1,t2,t3

#生成公钥私钥
def RSA_key_gen():
    key_len = 1024
    # print("before")
    p = find_prime(key_len-6, key_len-2)
    q = find_prime(key_len+2, key_len+6)
    print("素数p:",p)
    print("素数q:",q)
    # print("after")
    n = p * q
    phi = (p-1)*(q-1)

    e = random.randint(2,n-1)
    
    while e<phi:
        if(gcd(e,phi)==1):
            x = extended_euclid(e,phi)
            break
        else :
            e+=1
    if(x<0):
        x += phi
    d = x
    with open("RSA_Public_Key.txt", 'w') as f:
            res = str(n)+"\n"+str(e)
            f.write(res)
    with open("RSA_Secret_Key.txt", 'w') as f:
            res = str(n)+"\n"+str(d)
            f.write(res)
    return (n,e),(n,d)

# 加密
def encryption(plain_text:str, pubkey:tuple)->int:
    x = int(plain_text.encode().hex(),16)
    # print("x:",x)
    n = pubkey[0]
    e = pubkey[1]
    y = quick_mod(x,e,n)   # 加密
    return y


# 解密
def decryption(secret_text:int, prikey:tuple)->str:
    n = prikey[0]
    d = prikey[1]
    x = quick_mod(secret_text,d,n)    # 解密
    result = hex2bin(int2hex(x))
    return result        

if __name__ == '__main__':

    with open('lab2-Plaintext.txt','r',encoding='utf-8') as f:
        content = f.read()
    # content = "ab"
    print("加密前的消息是：", content)
    # print(isPrime(203))
    # prime=find_prime(8,10)
    # print("prime",prime)
    # 生成公钥私钥
    pubkey, prikey = RSA_key_gen()
    print("公钥:",pubkey)
    print("私钥:",prikey)
    ################################
    #for test
    # pubkey = (3233,17)
    # prikey = (3233,2753)
    result = ""
    for tem in content :
        # print("tem",tem)
        y = encryption(tem, pubkey)
        after_x = decryption(y, prikey)
        result += after_x
    ################################
    # y = encryption(content, pubkey)
    # print("加密后的消息是：", y)
    # after_x = decryption(y, prikey)
    # print("解密后的消息是：", after_x)'

    print("解密后的消息是：",result)
    with open("lab2-jiemitext.txt",'w',encoding='utf-8') as f:
        f.write(result)
        f.close()