# vpn-latency-checker

Measure repeated TCP connect latency to a host and port and give a good/fair/poor verdict (useful for VPN gateway checks).

## How to run

```sh
python3 main.py example.com 443 --count 5
```

## Example output

```
example.com:443: good (avg 24.3ms, 0 failed of 5)
```

Standard library only. Run the tests with `python3 -m unittest discover`.
