# china-domain-allowlist-singbox

把 [pluwen/china-domain-allowlist](https://github.com/pluwen/china-domain-allowlist)（SwitchyOmega 中国网站白名单，GPL-3.0）自动转换成 sing-box 规则集（source JSON），供 Karing / sing-box / mihomo 等客户端使用。

- 数据来源：pluwen/china-domain-allowlist（GPL-3.0，本仓库数据沿用同许可证）
- 每天通过 GitHub Actions 自动同步一次
- 输出文件：[`china-domains.json`](./china-domains.json)

## 在 Karing 中使用

1. 分流规则 → 自定义分流组 → 新建/编辑 → 规则集，填入 URL：
   ```
   https://raw.githubusercontent.com/bluesxu/china-domain-allowlist-singbox/main/china-domains.json
   ```
2. 该规则集用于「国内直连」方向的分流组。

## 转换规则

| SwitchyOmega (.sorl) | sing-box rule set |
| --- | --- |
| `*.example.com` | `domain_suffix: example.com` |
| `example.com` | `domain: example.com`（精确匹配） |
| `*.foo.*` | `domain_keyword: foo.` |
| `10.*.*.*` 等 5 条内网 IP | `ip_cidr`（10/8、100.64/10、127/8、172.16/12、192.168/16） |

转换脚本：[`convert.py`](./convert.py)。手工重新生成：`python3 convert.py`。
