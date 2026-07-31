# -*- coding: utf-8 -*-
"""US-004 临时验证脚本：店铺售后规则 API 全流程测试（用完删除）"""
import json
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8011/api/v1/rules"


def req(method, path="", body=None):
    url = BASE + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(r, timeout=10)
        status = resp.status
        text = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        status = e.code
        text = e.read().decode("utf-8")
    print(f"{method} {path} -> {status} {text[:200]}")
    return status, text


# 1. 列表（种子数据应为 5 条）
s, t = req("GET", "")
assert s == 200, t
data = json.loads(t)
print("list count:", len(data))
assert len(data) == 5, f"expected 5, got {len(data)}"
assert all("store_name" in x for x in data), "缺少 store_name"

# 2. 按店铺过滤
s, t = req("GET", "?store_id=1")
assert s == 200, t
data = json.loads(t)
print("store_id=1 count:", len(data))
assert len(data) > 0
assert all(x["store_id"] == 1 for x in data)

# 3. 创建（合法）
s, t = req("POST", "", {"store_id": 1, "rule_type": "退款", "title": "测试规则", "content": "测试内容"})
assert s == 201, t
created = json.loads(t)
rid = created["id"]
assert created["store_name"], "新建规则缺少 store_name"

# 4. 创建：store_id 不存在 → 400
s, t = req("POST", "", {"store_id": 999, "rule_type": "退款", "title": "x", "content": "x"})
assert s == 400, t

# 5. 创建：非法 rule_type → 400
s, t = req("POST", "", {"store_id": 1, "rule_type": "非法类型", "title": "x", "content": "x"})
assert s == 400, t

# 6. 详情
s, t = req("GET", f"/{rid}")
assert s == 200, t

# 7. 更新
s, t = req("PUT", f"/{rid}", {"title": "改后标题", "rule_type": "运费"})
assert s == 200, t
assert json.loads(t)["title"] == "改后标题"
assert json.loads(t)["rule_type"] == "运费"

# 8. 更新不存在的 id → 404
s, t = req("PUT", "/99999", {"title": "x"})
assert s == 404, t

# 9. 删除
s, t = req("DELETE", f"/{rid}")
assert s == 204, t

# 10. 删除不存在的 id → 404
s, t = req("DELETE", "/99999")
assert s == 404, t

print("ALL US-004 TESTS PASSED")
