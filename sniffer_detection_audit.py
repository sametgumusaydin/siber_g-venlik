#!/usr/bin/env python3
"""Linux yerel arayüzlerinde PROMISC bayrağını salt okunur denetler."""
import json, subprocess, time

result = subprocess.run(["ip", "-j", "-details", "link", "show"], capture_output=True, text=True, check=True)
interfaces = json.loads(result.stdout)
print("Kontrol zamanı:", time.strftime("%Y-%m-%d %H:%M:%S"))
for item in interfaces:
    flags = set(item.get("flags", []))
    state = item.get("operstate", "UNKNOWN")
    promisc = "PROMISC" in flags or int(item.get("promiscuity", 0)) > 0
    print(f"{item['ifname']:<16} state={state:<8} promisc={promisc}")
print("Not: PROMISC meşru analiz araçları tarafından da kullanılabilir; süreç ve yetki kayıtlarını doğrulayın.")
