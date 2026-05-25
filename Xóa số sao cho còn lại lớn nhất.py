n = input().strip()
k = int(input())

stack = []

for c in n:
    while stack and k > 0 and stack[-1] < c:
        stack.pop()
        k -= 1
    stack.append(c)

# nếu còn k thì xóa từ cuối
while k > 0:
    stack.pop()
    k -= 1

print(''.join(stack))
