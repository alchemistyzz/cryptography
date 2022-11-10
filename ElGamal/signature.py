import random
import sys
sys.setrecursionlimit(10000) #递归深度设置为10000，防止递归深度不够
# 第一步公开的信息
def signature(p = 521,g = 186,x=401,m=1914168):
    def quick_mod(base,exp,mod):
        ans  = 1
        while(exp):
            if(exp&1):
                ans = (ans * base) % mod
            base = (base * base) % mod
            exp >>= 1
        return ans 
    def gcd(a: int, b: int):
        """欧几里得算法求最大公约数"""
        while a != 0:
            a, b = b % a, a
        return b


    # 选择k 使得 gcd(k,p-1)=1
    while True:
        k = random.randint(0, p - 1)
        if gcd(k, p - 1) == 1:
            break

    # 计算 r = g^k mod p
    r = quick_mod(g, k, p)
    # 求 k^-1

    # 扩展欧几里得算法求逆 ki即为最终需要的逆元
    ai, bi = k, p - 1
    ki, ti, xi, yi = 1, 0, 0, 1  # 初始化s,t,x2,y2
    while bi:
        qi, ri = divmod(ai, bi)
        ai, bi = bi, ri  # 求最大公约数
        ki, ti, xi, yi = xi, yi, ki - qi * xi, ti - qi * yi  # 辗转相除

    # s = k^{-1} * (m-xr) mod (p-1)
    s = ki * (m - x * r) % (p - 1)

    print(f"签署的消息(m,r,s)：{(m, r, s)}")
    return (m,r,s)