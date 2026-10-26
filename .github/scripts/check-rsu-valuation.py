#!/usr/bin/env python3
"""Compare the published engine's Overlay valuation with Python exact rationals.

Run after fetch-iris.sh. All 81 supported price/FX precision pairs exercise
both rounding modes. The oracle uses Fraction, never the CEL divmod algorithm.
"""
from fractions import Fraction
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    engine = shutil.which("iris")
    if not engine:
        raise SystemExit("Install the verified published engine pin before valuation tests")
    version = next(line.split()[1] for line in (ROOT / ".github/engine.txt").read_text().splitlines()
                   if line.startswith("version "))
    randomizer = random.Random(20261026)
    cases = []
    for price_scale in range(9):
        for fx_scale in range(9):
            quantity = randomizer.randint(1, 1000000)
            price = randomizer.randint(1, 1000000 * 10 ** price_scale)
            fx = randomizer.randint(1, 1000000 * 10 ** fx_scale)
            denominator = 10 ** (price_scale + fx_scale)
            numerator = quantity * price * fx
            exact = Fraction(numerator, denominator)
            whole = exact.numerator // exact.denominator
            remainder = numerator % denominator
            for rounding in ("truncate", "half-up"):
                # Round the independently computed rational only once.
                rounded = exact if rounding == "truncate" else exact + Fraction(1, 2)
                gross = rounded.numerator // rounded.denominator
                case = {"name": f"rational oracle scales {price_scale}/{fx_scale}, {rounding}",
                        "recipe": {"id": "jp-rsu.vesting-value", "params": {
                            "scope_confirmed": True, "quantity": quantity,
                            "price_coefficient": price, "price_scale": price_scale,
                            "fx_coefficient": fx, "fx_scale": fx_scale, "rounding": rounding}}}
                if gross > 0:
                    case["figures"] = {"gross_jpy": gross, "unrounded_floor_jpy": whole,
                                       "fraction_numerator": remainder, "fraction_denominator": denominator}
                else:
                    case["error"] = "rounds to zero"
                cases.append(case)
    book = {"schema_version": 1, "region": "JP", "currency": "JPY", "scale": 0,
            "fiscal_year": 2026, "fiscal_start_month": 1,
            "jp_rsu": {"scope_confirmed": True, "included_in_salary_statement": False,
                       "japan_withholding": False, "tax_funding": "self-assessment",
                       "income_account": "Income:RSU", "share_account": "Assets:AMZN", "share_unit": "AMZN"}}
    with tempfile.TemporaryDirectory(prefix="iris-rsu-oracle-") as temporary:
        directory = Path(temporary)
        package = directory / "jp-rsu"
        shutil.copytree(ROOT / "JP/jp-rsu", package)
        (package / "tests/rational-oracle.yaml").write_text(json.dumps({"book": book, "cases": cases}))
        home = directory / "home"
        home.mkdir()
        env = {"PATH": os.environ["PATH"], "HOME": str(home), "XDG_CONFIG_HOME": str(home / "config")}
        if "SYSTEMROOT" in os.environ:
            env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
        reported = subprocess.check_output([engine, "version"], env=env, text=True).strip()
        if reported != f"iris {version}":
            raise SystemExit(f"Oracle requires published pin {version}; got {reported}")
        result = subprocess.run([engine, "overlay", "test", "--dir", str(package)],
                                env=env, capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise SystemExit(result.stdout + result.stderr)
    print(f"{len(cases)} exact-rational valuation comparisons passed with {version}")


if __name__ == "__main__":
    main()
