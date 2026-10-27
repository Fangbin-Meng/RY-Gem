# Eclipse geometry of a circumprimary H-alpha region

An interactive sky-plane diagram of the primary, donor, and circumprimary
H-alpha-emitting region. The preset stellar and orbital parameters are from
the RY Gem WD solution; edit the `System` values in the script for another
binary. Requires Python 3.9+, NumPy, and Matplotlib.

## Run

```powershell
python ry_gem_eclipse_geometry.py
python ry_gem_eclipse_geometry.py --phase 0.880 --export
python ry_gem_eclipse_geometry.py --phase 0.880 --output ry_gem_contact_088 --export
```

`--phase` sets the pre-primary midline-contact phase. Its default is 0.900;
replace it with the phase appropriate to the system being studied. The script
computes the corresponding radius, prints it in solar radii, and labels it
in the diagram. Without `--export`, the slider changes the contact phase and
recomputes the radius at every step. `--export` saves a vector PDF and a
600-dpi PNG without opening the interactive window. The default output prefix is
`ry_gem_eclipse_geometry`.

The calculation uses

\[
R_{\rm d}=|a\sin(2\pi\phi_{\rm c})|
-\sqrt{R_2^2-a^2\cos^2i\cos^2(2\pi\phi_{\rm c})}.
\]

The calculated radius depends on the supplied phase and the adopted midline
geometry.

## Figure caption template

Sky-plane projection of a semidetached binary at the selected pre-eclipse
midline-contact phase \(\phi_{\rm c}\). The primary and donor are shown with
the adopted stellar radii. The shaded ellipse represents a coplanar
H-alpha-emitting region with radius \(R_{\rm d}\) calculated from
\(\phi_{\rm c}\). The donor center has projected coordinates
\(x=a\sin(2\pi\phi)\) and \(y=a\cos i\cos(2\pi\phi)\). Its half-chord along
the projected disk midline is \(w=\sqrt{R_2^2-b^2}\), where \(b=|y|\). The
configuration shown satisfies the midline-contact condition
\(|x|=R_{\rm d}+w\).
