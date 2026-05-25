n = int(input())
segments = [tuple(map(int, input().split())) for _ in range(n)]

segments.sort()
print(segments)
# l, r = segments[0]
# ans = 0

# for i in range(1, n):
#     L, R = segments[i]
    
#     if L <= r:
#         r = max(r, R)
#     else:
#         ans = max(ans, r - l)
#         l, r = L, R

# ans = max(ans, r - l)

# print(ans)
    