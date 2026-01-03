import re
import os
import glob
import csv
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Optional, Tuple

RESULTS_DIR = "results"
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
SUMMARY_CSV = os.path.join(RESULTS_DIR, "metrics_summary.csv")


PROGRESS_RE = re.compile(
    r"progress:\s*(?P<sec>[\d\.]+)\s*s,\s*(?P<tps>[\d\.]+)\s*tps,\s*lat\s*(?P<lat>[\d\.]+)\s*ms\s*stddev\s*(?P<std>[\d\.]+)\s*ms",
    re.IGNORECASE
)


TPS_SUMMARY_RE = re.compile(r"tps\s*=\s*(?P<tps>[\d\.]+)", re.IGNORECASE)
LAT_SUMMARY_RE = re.compile(r"latency average\s*=\s*(?P<lat>[\d\.]+)\s*ms", re.IGNORECASE)

@dataclass
class RunMetrics:
    mode: str          
    scenario: str      
    tps_avg: Optional[float]
    latency_avg_ms: Optional[float]

def parse_progress_lines(text: str) -> pd.DataFrame:
    rows = []
    for line in text.splitlines():
        m = PROGRESS_RE.search(line)
        if m:
            rows.append({
                "sec": float(m.group("sec")),
                "tps": float(m.group("tps")),
                "lat_ms": float(m.group("lat")),
                "std_ms": float(m.group("std")),
            })
    return pd.DataFrame(rows)

def parse_summary(text: str) -> Tuple[Optional[float], Optional[float]]:
    tps_val = None
    lat_val = None


    for m in TPS_SUMMARY_RE.finditer(text):
        tps_val = float(m.group("tps"))

    mlat = LAT_SUMMARY_RE.search(text)
    if mlat:
        lat_val = float(mlat.group("lat"))

    return tps_val, lat_val

def detect_mode_scenario(filename: str) -> Tuple[str, str]:
    base = os.path.basename(filename).lower()
    mode = "sync" if base.startswith("sync_") else "async" if base.startswith("async_") else "unknown"

    if "read_only" in base:
        scenario = "read_only"
    elif "mixed_rw" in base:
        scenario = "mixed_rw"
    else:
        scenario = "unknown"

    return mode, scenario

def save_lineplot(df: pd.DataFrame, title: str, outpath: str, ycol: str, ylabel: str):
    if df.empty:
        return
    plt.figure()
    plt.plot(df["sec"], df[ycol])
    plt.title(title)
    plt.xlabel("Waktu (detik)")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()

def main():
    os.makedirs(PLOTS_DIR, exist_ok=True)

    txt_files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.txt")))
    if not txt_files:
        print("Tidak ada file results/*.txt. Jalankan benchmark dulu.")
        return

    metrics: List[RunMetrics] = []


    for fpath in txt_files:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        mode, scenario = detect_mode_scenario(fpath)


        df = parse_progress_lines(content)
        if not df.empty:
            out_tps = os.path.join(PLOTS_DIR, f"tps_line_{mode}_{scenario}.png")
            out_lat = os.path.join(PLOTS_DIR, f"lat_line_{mode}_{scenario}.png")
            save_lineplot(df, f"TPS vs Waktu ({mode} - {scenario})", out_tps, "tps", "TPS")
            save_lineplot(df, f"Latency vs Waktu ({mode} - {scenario})", out_lat, "lat_ms", "Latency (ms)")


        tps_avg, lat_avg = parse_summary(content)
        metrics.append(RunMetrics(mode=mode, scenario=scenario, tps_avg=tps_avg, latency_avg_ms=lat_avg))


    with open(SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["mode", "scenario", "tps_avg", "latency_avg_ms"])
        for m in metrics:
            w.writerow([m.mode, m.scenario, m.tps_avg, m.latency_avg_ms])


    dfm = pd.DataFrame([m.__dict__ for m in metrics])
    dfm = dfm[dfm["mode"].isin(["sync", "async"]) & dfm["scenario"].isin(["read_only", "mixed_rw"])]

    if not dfm.empty:

        pivot_tps = dfm.pivot(index="scenario", columns="mode", values="tps_avg")
        plt.figure()
        pivot_tps.plot(kind="bar")
        plt.title("Perbandingan TPS (Sync vs Async)")
        plt.xlabel("Skenario")
        plt.ylabel("TPS (avg)")
        plt.grid(True, axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "compare_tps_bar.png"), dpi=150)
        plt.close()

        pivot_lat = dfm.pivot(index="scenario", columns="mode", values="latency_avg_ms")
        plt.figure()
        pivot_lat.plot(kind="bar")
        plt.title("Perbandingan Latency (Sync vs Async)")
        plt.xlabel("Skenario")
        plt.ylabel("Latency avg (ms)")
        plt.grid(True, axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "compare_latency_bar.png"), dpi=150)
        plt.close()

    print(f"Selesai. Grafik ada di: {PLOTS_DIR}")
    print(f"Ringkasan metrics: {SUMMARY_CSV}")


if __name__ == "__main__":
    main()
