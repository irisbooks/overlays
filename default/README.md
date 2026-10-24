# Common completion

`default@2026.10.2` requires bindings 5. It adds discoverable journal and inventory tasks to the existing checked completion behavior.

Creation presets explicitly copy and select this package. Existing Books retain their selection; there is no implicit runtime default. Install an exact embedded or signed release version into the Book before selecting it. All execution reads the Book copy.

Run `iris overlay test --dir default` with the candidate engine. This source version is a release candidate until its signed release is published.
