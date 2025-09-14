import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

def parse_sum(stdout: str):
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("SUM="):
            try:
                return int(line.split("=", 1)[1])
            except Exception:
                pass
    return None

def write_junit(report_path: Path, name: str, ok: bool, stdout: str, stderr: str):
    testsuite = Element("testsuite", name=name, tests="1", failures="0" if ok else "1")
    testcase = SubElement(testsuite, "testcase", name=name)
    if not ok:
        failure = SubElement(testcase, "failure", message="Validation failed")
        failure.text = (stderr or "") + "\n" + (stdout or "")
    xml_bytes = tostring(testsuite, encoding="utf-8")
    report_path.write_bytes(xml_bytes)

def main():
    p = argparse.ArgumentParser(description="Python wrapper for C++ tool")
    p.add_argument("--bin", required=True, help="Path to compiled C++ binary")
    p.add_argument("--input", required=True, help="Input file path")
    p.add_argument("--threshold", type=int, required=True, help="Expected minimum sum")
    p.add_argument("--timeout", type=float, default=15.0, help="Seconds before kill")
    p.add_argument("--junit", type=Path, default=None, help="Optional JUnit XML output path")
    args = p.parse_args()

    cmd = [args.bin, "--input", args.input, "--threshold", str(args.threshold)]
    start = time.time()
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=args.timeout
        )
    except subprocess.TimeoutExpired as ex:
        result = {
            "status": "timeout",
            "duration_sec": round(time.time() - start, 3),
            "cmd": cmd,
        }
        print(json.dumps(result, indent=2))
        if args.junit:
            write_junit(args.junit, "cpp_tool", False, "", f"Timeout after {args.timeout}s")
        sys.exit(124)

    stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    total = parse_sum(stdout)
    ok = (rc == 0) and (total is not None) and (total >= args.threshold)

    result = {
        "status": "ok" if ok else "fail",
        "duration_sec": round(time.time() - start, 3),
        "return_code": rc,
        "sum": total,
        "threshold": args.threshold,
        "stdout": stdout,
        "stderr": stderr,
        "cmd": cmd,
    }
    print(json.dumps(result, indent=2))

    if args.junit:
        write_junit(args.junit, "cpp_tool", ok, stdout, stderr)

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
