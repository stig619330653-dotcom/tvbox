import json
import urllib.request

url = "https://raw.githubusercontent.com/stig619330653-dotcom/tvbox/refs/heads/main/resources/resources.json"

try:
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode("utf-8"))

    sites = []
    for item in data.get("resources", []):
        tags = item.get("tags", [])
        name = item.get("name", "")
        
        # 精准匹配：只提取标签或名称中包含 tvbox、影视仓 或 配置地址的项
        is_tvbox_resource = (
            any("tvbox" in t.lower() or "影视仓" in t or "配置" in t for t in tags) or
            "tvbox" in name.lower() or "影视仓" in name
        )
        
        if is_tvbox_resource and item.get("url"):
            site = {
                "key": item.get("id", "free"),
                "name": name,
                "type": 3,
                "api": item.get("url"),
                "searchable": 1,
                "quickSearch": 1,
                "filterable": 1,
            }
            sites.append(site)

    # 构造标准的 TVBox 格式
    tvbox_config = {
        "sites": sites,
        "parses": [],
        "rules": []
    }

    with open("tvbox.json", "w", encoding="utf-8") as f:
        json.dump(tvbox_config, f, ensure_ascii=False, indent=4)
    print("成功精准过滤并生成 TVBox 源：", len(sites))

except Exception as e:
    print("转换失败:", e)
