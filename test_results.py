import json
import re
import statistics
from collections import Counter
from datetime import datetime


def extract_keywords(text, top_n=10):
    """Return top frequent keywords (simple heuristic)."""
    stop = {"the", "is", "in", "and", "to", "of", "a", "for", "on", "with", "as", "by", "an", "are"}
    words = re.findall(r"\w+", text.lower())
    freq = Counter(w for w in words if w not in stop and len(w) > 3)
    return [w for w, _ in freq.most_common(top_n)]


def keyword_accuracy(predicted, reference):
    """Percent overlap between predicted and reference keywords."""
    d, e = set(map(str.lower, predicted)), set(map(str.lower, reference))
    return round(len(d & e) / len(d) * 100, 2) if d else 0.0


def keyword_enforcement(text, required):
    """Percent of required keywords present in text."""
    if not required:
        return 100.0
    missing = [k for k in required if k.lower() not in text.lower()]
    return round((len(required) - len(missing)) / len(required) * 100, 2)


def length_metrics(requested, text):
    """Return length and uniqueness metrics for generated text."""
    words = text.split()
    actual = len(words)
    unique = len(set(w.lower() for w in words)) if actual > 0 else 0
    accuracy = round(actual / requested * 100, 2) if requested > 0 else 0.0
    return {
        "requested": requested,
        "actual": actual,
        "accuracy%": accuracy,
        "unique%": round(unique / actual * 100, 2) if actual > 0 else 0.0,
        "target_met": 90 <= accuracy <= 110
    }


def analyze_generation(prompt, generated_text, response_time_s, requested_words):
    """Analyze a single generation and return metrics dict."""
    p_kw = extract_keywords(prompt)
    g_kw = extract_keywords(generated_text)
    return {
        "timestamp": datetime.now().isoformat(),
        "prompt_keywords": p_kw,
        "generated_keywords": g_kw,
        "keyword_accuracy%": keyword_accuracy(p_kw, g_kw),
        "keyword_enforcement%": keyword_enforcement(generated_text, p_kw),
        "response_time_s": round(response_time_s, 2),
        "length_metrics": length_metrics(requested_words, generated_text)
    }


def log_generation(data, path="generation_logs.json"):
    """Append analysis result to a JSON log safely."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
            except json.JSONDecodeError:
                logs = []
    except FileNotFoundError:
        logs = []

    logs.append(data)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

    print(f"✓ Logged generation ({len(logs)} total)")


def aggregate_metrics(path="generation_logs.json"):
    """Compute averages across all logged generations."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except Exception:
        return {"error": "No logs found."}

    if not logs:
        return {"error": "Empty log file."}

    avg = lambda k: round(statistics.mean(k), 2) if k else 0.0
    rt = [l.get("response_time_s", 0) for l in logs]
    acc = [l.get("keyword_accuracy%", 0) for l in logs]
    enf = [l.get("keyword_enforcement%", 0) for l in logs]
    wc = [l.get("length_metrics", {}).get("accuracy%", 0) for l in logs]
    uniq = [l.get("length_metrics", {}).get("unique%", 0) for l in logs]

    return {
        "total_generations": len(logs),
        "avg_response_time": avg(rt),
        "avg_keyword_accuracy": avg(acc),
        "avg_keyword_enforcement": avg(enf),
        "avg_word_count_accuracy": avg(wc),
        "avg_unique_word_ratio": avg(uniq),
        "targets_met": {
            "response_time": avg(rt) < 10,
            "keyword_accuracy": avg(acc) >= 85,
            "keyword_enforcement": avg(enf) >= 85,
        },
    }


def final_report(path="generation_logs.json"):
    """Print and save an aggregate final report for all generations."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except Exception:
        print("❌ No generation logs found. Generate some texts in Streamlit first.")
        return

    if len(logs) == 0:
        print("⚠️  No generations found in logs.")
        return

    num_gen = len(logs)
    avg = lambda k: round(statistics.mean(k), 2) if k else 0.0

    rt = [l.get("response_time_s", 0) for l in logs]
    acc = [l.get("keyword_accuracy%", 0) for l in logs]
    enf = [l.get("keyword_enforcement%", 0) for l in logs]
    wc = [l.get("length_metrics", {}).get("accuracy%", 0) for l in logs]
    uniq = [l.get("length_metrics", {}).get("unique%", 0) for l in logs]

    print("=" * 80)
    print(f"FINAL METRICS REPORT")
    print("=" * 80)
    print(f"\nTotal Generations Analyzed: {num_gen}")
    print("\n" + "-" * 80)
    print(f"{'Metric':<45} {'Result':<20}")
    print("-" * 80)
    print(f"{'Response Time (Average)':<45} {avg(rt)}s")
    print(f"{'Keyword Accuracy (DCKG)':<45} {avg(acc)}%")
    print(f"{'Keyword Enforcement (DMK)':<45} {avg(enf)}%")
    print(f"{'Word Count Accuracy':<45} {avg(wc)}%")
    print(f"{'Unique Word Ratio (Average)':<45} {avg(uniq)}%")
    print("-" * 80)

    report = {
        "total_generations": num_gen,
        "avg_response_time": avg(rt),
        "avg_keyword_accuracy": avg(acc),
        "avg_keyword_enforcement": avg(enf),
        "avg_word_count_accuracy": avg(wc),
        "avg_unique_word_ratio": avg(uniq),
        "all_values": {
            "response_times": rt,
            "keyword_accuracy": acc,
            "keyword_enforcement": enf,
            "word_count_accuracy": wc,
            "unique_word_ratio": uniq
        }
    }

    with open("final_metrics_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\nFull report saved to: final_metrics_report.json")
    print("=" * 80)


if __name__ == "__main__":
    final_report()
