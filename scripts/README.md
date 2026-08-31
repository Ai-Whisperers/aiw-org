# AIW Scripts

All scripts for the AI Whisperers agent org.

## Usage

Each script supports `--help`:

```bash
python3 scripts/<subdir>/<name>.py --help
```

## Conventions

- Python 3.13+
- Shebang on line 1
- Module docstring (triple quotes)
- `if __name__ == "__main__":` block
- `--help` via argparse
- Atomic writes (tmp + replace)
- Logging to stderr, results to stdout

## Layout

- `whatsapp/` - WhatsApp human-in-loop
- `webhook/` - Webhook triggers (Factor 11)
- `state/` - Unified state + git versioning
- `cost/` - LLM cost monitoring
- `errors/` - Error compacting
- `context/` - Per-agent context windows
- `observability/` - Eval-gate, tracing, trending
- `dashboard/` - Org dashboard
- `deprecation/` - Skill deprecation workflow

## Tests

Run all tests:

```bash
bash tests/run-all.sh
```

44 tests, ~1 second runtime.

