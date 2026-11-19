"""Flag unsanctioned AI tool usage from proxy/DNS logs."""
import csv, sys
from collections import defaultdict


def load_domains(path="ai_domains.yaml"):
    out = {}
    for line in open(path):
        line = line.split("#")[0].strip()
        if ":" in line:
            d, cat = line.split(":", 1)
            out[d.strip()] = cat.strip()
    return out


def load_sanctioned(path="sanctioned.txt"):
    return {l.strip() for l in open(path) if l.strip() and not l.startswith("#")}


def main(log_path):
    ai, ok = load_domains(), load_sanctioned()
    usage = defaultdict(lambda: [0, 0])
    for row in csv.DictReader(open(log_path)):
        d = row["domain"]
        if d in ai and d not in ok:
            usage[(row["user"], d)][0] += 1
            usage[(row["user"], d)][1] += int(row["bytes_out"])
    print("UNSANCTIONED AI USAGE")
    print(f"{'user':<10}{'domain':<22}{'hits':>5}{'bytes_out':>12}  risk")
    for (user, d), (hits, b) in sorted(usage.items(), key=lambda x: -x[1][1]):
        risk = "HIGH" if b > 100_000 else "MEDIUM"   # big uploads = possible data exfil
        print(f"{user:<10}{d:<22}{hits:>5}{b:>12}  {risk}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sample_data/proxy_logs.csv")
