# RY Gem eclipse geometry

An interactive sky-plane diagram of the primary, donor, and circumprimary
H-alpha-emitting region. The stellar and orbital parameters are from the WD
solution. Requires Python 3.9+, NumPy, and Matplotlib.

## Run

```powershell
python ry_gem_eclipse_geometry.py
python ry_gem_eclipse_geometry.py --phase 0.895 --export
python ry_gem_eclipse_geometry.py --disk-radius 11.0 --export
```

The commands above open the phase slider, export a specified phase, and export
the calculated midline-contact phase for a specified radius, respectively.
Drag the slider to change phase. `--phase` selects the displayed phase;
`--disk-radius` sets the adopted radius in solar radii (default: 11).
Without `--phase`, the script displays the first midline-contact phase for
that radius. `--export` saves a vector PDF and a 600-dpi PNG without controls.

## Figure caption

Sky-plane projection of RY Gem at orbital phase \(\phi=0.8925\). The primary
and donor are shown with radii from the WD solution. The shaded ellipse
represents a coplanar H-alpha-emitting region with adopted radius
\(R_{\rm d}=11\,R_\odot\). The donor center has projected coordinates
\(x=a\sin(2\pi\phi)\) and \(y=a\cos i\cos(2\pi\phi)\). Its half-chord along
the projected disk midline is \(w=\sqrt{R_2^2-b^2}\), where \(b=|y|\). The
configuration shown satisfies the midline-contact condition
\(|x|=R_{\rm d}+w\).

If a contact phase \(\phi_{\rm c}\) is estimated from observations, the same
midline geometry gives an approximate radius
\(R_{\rm d}=|a\sin(2\pi\phi_{\rm c})|-\sqrt{R_2^2-a^2\cos^2i\cos^2(2\pi\phi_{\rm c})}\).
The script does not determine \(\phi_{\rm c}\) from spectra; that value must
be supplied or assessed separately. Update the caption's phase and radius
when exporting a different configuration.
