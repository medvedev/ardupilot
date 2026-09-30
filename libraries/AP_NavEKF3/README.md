# Custom no-aiding measurement-noise ceiling

`EK3_NOAID_M_NSE_MAX` is a build-time ceiling for the armed, tilt-aligned
EKF3 no-aiding observation noise. It defaults to **50 m**, preserving the
existing stock firmware behavior. The runtime `EK3_NOAID_M_NSE` parameter
still defaults to **10 m**. The build-time ceiling must be between **0.5 m
and 10,000 m**, inclusive; an invalid value fails compilation.

To raise the ceiling in a custom build, create an extra hardware-definition
file containing:

```text
define EK3_NOAID_M_NSE_MAX 1000.0f
```

Then configure and build, for example:

```sh
./waf configure --board sitl --extra-hwdef=extra-noaid.hwdef
./waf copter
```

The runtime parameter still selects the observation noise; rebuilding with
a larger ceiling does not set the parameter to that ceiling. Values above
the compiled ceiling remain clamped. Stationary zero-velocity fusion,
initial alignment and aided observation-noise paths are unchanged.

Generated parameter documentation retains the standard-build range of
0.5–50 m. The parameter description identifies the custom-build override;
custom-build users should consult their build definition for its ceiling.

Higher values weaken the synthetic no-aiding constraint, reducing its
influence during maneuvers but increasing sensitivity to IMU errors and
drift. They do not provide external aiding or guarantee attitude accuracy.
An existing stored value above 50 m becomes effective if a custom build
raises the ceiling sufficiently.
