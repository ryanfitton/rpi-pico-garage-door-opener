/**
 * This script handles the Add to Home Screen functionality from https://github.com/philfung/add-to-homescreen
 */
document.addEventListener("DOMContentLoaded", function() {
    window.AddToHomeScreenInstance = window.AddToHomeScreen({
        appName: 'Garage Door Opener',                          // Name of the app.
                                                                // Required.
        appNameDisplay: 'standalone',                           // If set to 'standalone' (the default), the app name will be diplayed
                                                                // on it's own, beneath the "Install App" header. If set to 'inline', the
                                                                // app name will be displayed on a single line like "Install MyApp"
                                                                // Optional. Default 'standalone'
        appIconUrl: 'data:image/png;base64,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',                     // App icon link (square, at least 40 x 40 pixels).
                                                                // Required.
        assetUrl: 'https://raw.githubusercontent.com/philfung/add-to-homescreen/refs/heads/main/dist/assets/img/',                                         // Link to directory of library image assets.

        maxModalDisplayCount: 1,                                // If set, the modal will only show this many times.
                                                                // [Optional] Default: -1 (no limit).  (Debugging: Use this.clearModalDisplayCount() to reset the count)
        displayOptions:{ showMobile: true, showDesktop: true }, // show on mobile/desktop [Optional] Default: show everywhere
        allowClose: true, // allow the user to close the modal by tapping outside of it [Optional. Default: true]
        showArrow: true, // show the bouncing arrow on the modal [Optional. Default: true] (highly recommend leaving at true as drastically affects install rates)
    });

    ret = window.AddToHomeScreenInstance.show('en');        // show "add-to-homescreen" instructions to user, or do nothing if already added to homescreen
                                                            // [optional] language.  If left blank, then language is auto-decided from (1) URL param locale='..' (e.g. /?locale=es) (2) Browser language settings
});
