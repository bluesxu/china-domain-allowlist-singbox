#!/usr/bin/env python3
"""Convert pluwen/china-domain-allowlist (SwitchyOmega rules) to a sing-box
source-format rule set, usable by Karing / sing-box / mihomo.

Output: china-domains.json  ->  {"version": 2, "rules": [...]}

Mapping:
  *.example.com   -> domain_suffix "example.com"
  example.com     -> domain "example.com"          (exact host)
  *.foo.*         -> domain_keyword "foo."
  10.*.*.*        -> ip_cidr 10.0.0.0/8            (and 4 other private ranges)
"""

import json
import sys
import urllib.request

SRC = "https://raw.githubusercontent.com/pluwen/china-domain-allowlist/main/allow-list.sorl"
OUT = "china-domains.json"

IP_WILDCARDS = {
    "10.*.*.*": "10.0.0.0/8",
    "100.64.*.*": "100.64.0.0/10",
    "127.*.*.*": "127.0.0.0/8",
    "172.16.*.*": "172.16.0.0/12",
    "192.168.*.*": "192.168.0.0/16",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "china-domain-allowlist-singbox"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8-sig")


def main() -> int:
    text = fetch(SRC)
    domains, suffixes, keywords, cidrs = set(), set(), set(), set()

    for raw in text.splitlines():
        line = raw.strip().lower()
        if not line or line.startswith(";") or line.startswith("["):
            continue
        if line in IP_WILDCARDS:
            cidrs.add(IP_WILDCARDS[line])
        elif line.startswith("*.") and line.endswith(".*"):
            keywords.add(line[2:-2] + ".")
        elif line.startswith("*.") and "*" not in line[2:]:
            suffixes.add(line[2:])
        elif "*" in line:
            print(f"skip (unsupported wildcard): {line}", file=sys.stderr)
        else:
            domains.add(line)

    rules = []
    if domains:
        rules.append({"domain": sorted(domains)})
    if suffixes:
        rules.append({"domain_suffix": sorted(suffixes)})
    if keywords:
        rules.append({"domain_keyword": sorted(keywords)})
    if cidrs:
        rules.append({"ip_cidr": sorted(cidrs)})

    out = {"version": 2, "rules": rules}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(
        f"domains={len(domains)} suffixes={len(suffixes)} "
        f"keywords={len(keywords)} cidrs={len(cidrs)} "
        f"total={len(domains) + len(suffixes) + len(keywords) + len(cidrs)}"
    )

    if len(suffixes) < 500:
        print("ERROR: too few suffixes, source likely broken", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
