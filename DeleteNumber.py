def b1():
    n = input().strip()
    k = int(input())

    stack = []

    for c in n:
        while stack and k > 0 and stack[-1] < c:
            stack.pop()
            k -= 1
        stack.append(c)

    while k > 0:
        stack.pop()
        k -= 1

    print(''.join(stack))


b1()