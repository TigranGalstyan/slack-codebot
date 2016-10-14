def listSum(list): 
    return sum(list)

def sumOfCubesInRange(begin, end):
    s = 0
    for i in range(begin, end):
        s += i ** 3
    return s

def fibonacci(n): 
    if n == 1 or n == 2:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def isSquare(n):
    i = int(n**(1./2))
    return (i*i == n)

def isPrime(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
	i += 1
    return True

def factorial(n):
    s = 1
    for i in range(2,n+1):
        s *= i
    return s

def diskArea(r):
    import math
    return math.pi*r*r

def numberOfVowels(s):
    vowels = 'aeuio'
    ans = 0
    for i in s:
        if i in vowels:
            ans += 1
    return ans

def fibonacciFast(n):
    a = 1
    b = 1
    c = 1
    while(n > 1):
        x = c
        c = a + b
        a = b
        b = x
        n -= 1
    return c
def nthRoot(x,n):
    return x**(1.0/float(n))

def longestConsecutiveLetterCount(s):
	x = [1]
	now = [0,0]
	now[ord(s[0]) - ord('0')] = 1
	for i in range(1, len(s)):
		if s[i] != s[i-1]:
			now[0] = 0
			now[1] = 0
		now[ord(s[i]) - ord('0')] += 1
		x.append(max(now))
	return max(x)

def isFooInThere(s):
	foo = "foo"
	f1 = s.find('f')
	o3 = s.rfind('o')
	if f1 == -1 or o3 == -1 or f1 > o3:
		return False
	for i in range(f1,o3):
		if s[i] == 'o':
			return True
	return False
def isFooInThereAdvanced(s, foo):
	i = 0
	for c in s:
		if c == foo[i]:
			i += 1
		if i == len(foo):
			return True
	return False
def digitSum(x):
	x = x % 9
	if x == 0:
		x = 9
	return x
def zeroSumCount(l):
	ans = 0
	ongoing_sum = 0
	sums = {}
	sums[0] = 1
	for i in l:
		ongoing_sum += i
		if ongoing_sum not in sums:
			sums[ongoing_sum] = 0
		ans += sums[ongoing_sum]
		sums[ongoing_sum] += 1
	return ans

def removeVowels(s):
	vowels = 'aiuoe'
	n = [c for c in s if c not in vowels]
	return ''.join(n) 

def cylinderSort(d):
	
	return [name[0] for name in sorted(d, key = lambda x : x[2] * x[1] * x[1], reverse = True)]

def primeList(l):
	return sorted([x for x in l if isPrime(x)])
