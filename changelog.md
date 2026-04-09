# v0.9.3

* Performance improvements for complex UI applications such as VS Code.
* Add throttling to core cycle mouse object updates (100ms minimum interval).
* Add coordinate-based cache and proper MTA thread synchronization to UIA element queries.
* Filter mouse hook forwarding to wheel events only.
* Cache window class name lookups and optimize overlay class checks.

# v0.9.2

* Implement Tauri UIA redirection support in mouse tracking
