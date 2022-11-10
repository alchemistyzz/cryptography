from generator import generator
from signature import signature
from hashlib import sha256
def quick_mod(base,exp,mod):
        ans  = 1
        while(exp):
            if(exp&1):
                ans = (ans * base) % mod
            base = (base * base) % mod
            exp >>= 1
        return ans 
m=200111102
for i in range(3):
    #  发出方的公钥
    print(f'第{i+1}次签字')

    (p, g, y, x) = generator()
    (m, r, s) = signature(p, g, x, m)
    # 经过签字后的消息
    # 计算 v1 v2 并比较
    if(i==2):
        m=114514
        print(f'm篡改为{m}')
    v1 = quick_mod(y, r, p) * quick_mod(r, s, p) % p
    v2 = quick_mod(g, m, p)

    print(f"v1:{v1},v2:{v2}")
    if v1 == v2:
        print("验证成功，签名有效")
    else :
        print("验证失败, 签名异常")