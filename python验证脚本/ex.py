# 快速验证脚本
from collections import defaultdict

fi = [
    (4,1,2),(5,1,4),(6,4,2),(6,2,3),(8,4,6),(8,5,4),
    (9,8,6),(10,1,5),(11,7,3),(13,5,8),(13,12,9),(13,10,5),
    (14,7,11),(15,12,13),(16,10,13),(16,7,14),(16,1,10),
    (16,2,1),(16,3,7),(17,16,13),(18,17,15),(18,9,12),
    (18,11,6),(19,11,18),(19,14,11),(19,16,14)
]
fi = [(a-1,b-1,c-1) for a,b,c in fi]

edge_count = defaultdict(int)
for a,b,c in fi:
    for e in [(min(a,b),max(a,b)),(min(b,c),max(b,c)),(min(a,c),max(a,c))]:
        edge_count[e] += 1

boundary = [e for e,cnt in edge_count.items() if cnt == 1]
print(f"边界边数量: {len(boundary)}")
for e in boundary:
    print(f"  边 ({e[0]+1}, {e[1]+1})")