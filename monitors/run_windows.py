"""Local Windows launcher for the otherwise unchanged Linux benchmark.

Only missing OS process-control calls are adapted. Validator, timing,
checkpoints, anchors and scoring are the original supplied code. This does
not provide Linux privilege/resource isolation and is not for untrusted code.
On Linux use run.py directly.
"""
import os

if os.name == "nt":
    import signal

    def _unsupported(*args):
        raise OSError("Unix process groups are unavailable on Windows")

    os.setsid = _unsupported
    os.getuid = lambda: 1000
    os.killpg = _unsupported
    if not hasattr(signal, "SIGKILL"):
        signal.SIGKILL = 9

if __name__ == "__main__":
    import metrics
    from benchkit.cli import run_main
    raise SystemExit(run_main(metrics.BENCH))
