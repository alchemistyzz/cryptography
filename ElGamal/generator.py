import random
import sympy
def generator():
    def gcd(a: int, b: int):
        """欧几里得算法求最大公约数"""
        while a != 0:
            a, b = b % a, a
        return b


    def euler(n):
        """欧拉函数"""
        # 如果n是质数直接返回n-1
        if (n, 1) == 1:
            return n - 1
        m = 0
        for i in range(n):
            if gcd(i, n) == 1:
                m += 1
        return m

    def quick_mod(base,exp,mod):
        ans  = 1
        while(exp):
            if(exp&1):
                ans = (ans * base) % mod
            base = (base * base) % mod
            exp >>= 1
        return ans 

    def primitive_element(p, q):

        while True:
            g = random.randint(2, p - 2)
            if quick_mod(g, 2, p) != 1 and quick_mod(g, q, p) != 1:
                return g

    while True:
        q = sympy.randprime(10**149, 10**150 / 2 - 1) #使得p也在150位
        if sympy.isprime(q):
            p = 2 * q + 1
            if len(str(p)) == 150 and sympy.isprime(p):
                break
    g = primitive_element(p, q)

    # 随机生成一个 x
    x = random.randint(1, p - 2)
    # 计算出 y = g^x mod p
    y = quick_mod(g, x, p)

    print(f"公开(p,g,y)：{(p, g, y)}")
    print(f"秘密保存k ：{x}")
    return (p,g,y,x)