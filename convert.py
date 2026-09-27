import json
import urllib.request

url = "https://raw.githubusercontent.com/stig619330653-dotcom/tvbox/refs/heads/main/resources/resources.json"

try:
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode("utf-8"))

    urls_list = []
    for item in data.get("resources", []):
        tags = item.get("tags", [])
        name = item.get("name", "")
        
        # 精准筛选出属于 TVBox / 影视仓配置地址的条目
        is_tvbox_config = (
            any("tvbox" in t.lower() or "影视仓" in t or "配置" in t for t in tags) or
            "tvbox" in name.lower() or "影视仓" in name
        )
        
        item_url = item.get("url")
        if is_tvbox_config and item_url:
            # 构造多仓格式里每一条线路的对象
            urls_list.append({
                "name": name,
                "url": item_url
            })

    # 构造标准的 TVBox 多仓聚合格式
    multi_config = {
        "urls": urls_list
    }

    with open("tvbox.json", "w", encoding="utf-8") as f:
        json.dump(multi_config, f, ensure_ascii=False, indent=4)
    print("成功生成多仓配置，共包含源：", len(urls_list))

except Exception as e:
    print("转换失败:", e)
