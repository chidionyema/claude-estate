"""The executor's memory across sessions (crew#513).

Founder, 2026-08-27: "every ticket it tackles it needs to improve its problem solving and
knowledge of the stack ... and retain it thru sessions". Before this file, every lesson lived
in the coordinator's head and was re-typed at the top of each plan by hand; a fresh session
started the executor from zero. Now pi_execute prepends mcp/executor-primer.md to every plan and
`lesson` appends one dated line to it after the run, so job N+1 starts with what job N learned.

Run: python3 ~/.claude/mcp/test_pi_bridge_primer.py     (or: pytest that path)
"""
import importlib.util
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location("pi_bridge", os.path.join(HERE, "pi_bridge.py"))
pb = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(pb)


def test_primer_is_tracked_beside_the_bridge_and_has_a_lessons_section():
    text = pb.load_primer()
    assert text, "mcp/executor-primer.md is missing or empty"
    assert pb.LESSONS_HEADING in text
    assert "bin/idp-cloud" in text and "dirname" in text, "the primer must carry the two lessons that cost CI runs"
    assert len(text.encode()) < 6 * 1024, "a primer nobody reads is not a primer: keep it under 6 KB"


def test_every_plan_carries_the_primer_before_the_plan():
    out = pb.compose_prompt("do the thing", "PRIMER TEXT")
    assert out.index("=== ESTATE PRIMER") < out.index("=== PLAN ===")
    assert "PRIMER TEXT" in out and out.endswith("=== PLAN ===\ndo the thing")
    assert "=== ESTATE PRIMER" not in pb.compose_prompt("do the thing", "")


def test_a_lesson_is_appended_once_and_only_under_a_lessons_heading():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "primer.md")
        with open(p, "w") as f:
            f.write("# primer\n\n## Lessons\n")
        assert pb.add_lesson("never `pytest tests` unqualified", p, day="2026-08-27") is True
        assert pb.add_lesson("never   `pytest tests`  unqualified", p, day="2026-08-27") is False, "same lesson twice is one line"
        assert pb.add_lesson("   ", p) is False
        text = open(p).read()
        assert text.endswith("## Lessons\n- 2026-08-27 never `pytest tests` unqualified\n")
        with open(p, "w") as f:
            f.write("# no lessons section\n")
        assert pb.add_lesson("x", p) is False and open(p).read() == "# no lessons section\n"


def test_pi_execute_schema_exposes_lesson_and_no_primer():
    src = open(os.path.join(HERE, "pi_bridge.py")).read()
    assert '"lesson": {"type": "string"' in src and '"no_primer": {"type": "boolean"' in src


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print("PASS", name)
            except AssertionError as e:
                fails += 1; print("FAIL", name, e)
    sys.exit(1 if fails else 0)
