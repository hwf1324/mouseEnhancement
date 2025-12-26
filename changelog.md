# v0.9.0

* Refactored Electron UIA-related components:
  * Utilized the `IUIAutomation.ElementFromPointBuildCache` method to retrieve UIA elements from coordinates for creating redirected mouse objects.
  * Simultaneously employed `IUIAutomationCondition` to exclude UIA elements with an empty `Name` attribute, resolving certain issues encountered during mouse navigation in VS Code.
    * For example it is now possible to read the text on the hover panel.
* Add a mouse move event delay parameter when mouse objects are automatically updated only during core cycles, as an experimental implementation of <https://github.com/nvaccess/nvda/issues/19372>.
* Report information on the Tree Style Tab extension tab when the mouse moves.
