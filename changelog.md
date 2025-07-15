# v0.7.1

* Auto Update Mouse Object: Improved stability when automatically updating mouse objects while scrolling the mouse wheel.
* Forward mouse messages received by the NVDA mouse hook to the `pre_handleWindowMessage` extension point. (Exclude the wParam and lParam parameters, which should be set to `None`.)
