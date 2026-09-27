import json
import urllib.request

# 读取你仓库里的原始 resources.json
url = "https://raw.githubusercontent.com/stig619330653-dotcom/tvbox/refs/heads/main/resources/resources.json"

try:
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode("utf-8"))

    # 提取过滤后的源，转换为 TVBox 的 sites 格式
    sites = []
    # 假设原项目的 resources 结构里包含可用网址和名称
    for item in data.get("resources", []):
        # 你可以根据实际的筛选条件来写，比如只选在线视频且有有效 url 的
        if item.get("category") == "online_video" and item.get("url"):
            site = {
                "key": item.get("id"),
                "name": item.get("name"),
                "type": 3,  # TVBox 常规爬虫源类型
                "api": item.get("url"),
                "searchable": 1,
                "quickSearch": 1,
                "filterable": 1,
            }
            sites.append(site)

    # 构造标准的 TVBox 订阅格式
    tvbox_config = {"sites": sites}

    # 保存为 tvbox.json 输出
    with open("tvbox.json", "w", encoding="utf-8") as f:
        json.dump(tvbox_config, f, ensure_ascii=False, indent=4)
    print("转换成功，共生成标准源：", len(sites))

except Exception as e:
    print("转换失败:", e)
