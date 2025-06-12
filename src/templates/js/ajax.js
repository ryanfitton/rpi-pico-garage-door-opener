/**
 * This script handles the AJAX request for the door button
 */
document.addEventListener("DOMContentLoaded", function() {
    /**
     * Show or hide a response div after a timeout
     * @param {HTMLElement} el - The element to show or hide
     * @param {string} action - "show" to show the element, "hide" to hide it
     * @param {number} timeout - The time in milliseconds to wait before showing or hiding
     */
    function responseElDisplay(el, action="show", timeout=5000) {
        if (el) {
            setTimeout(() => {
                if (action === "show") {
                    el.classList.remove("hidden");
                } else if (action === "hide") {
                    el.classList.add("hidden");
                }
            }, timeout);
        }
    }

    /**
     * Set the button attributes after a timeout
     * @param {HTMLElement} el - The button element to update
     * @param {string} text - The text to set on the button
     * @param {boolean} disabled - Whether the button should be disabled
     * @param {number} timeout - The time in milliseconds to wait before updating the button
     */
    function buttonAttributes(el, text, disabled=false, timeout=0) {
        if (el) {
            setTimeout(() => {
                el.textContent = text;
                el.disabled = disabled;
            }, timeout);
        }
    }
    
    /**
     * Run the AJAX request when a door button is clicked
     */
    document.querySelectorAll(".door-button").forEach(function(button) {
        button.addEventListener("click", function(event) {
            //Prevent default button action
            event.preventDefault();

            //Setup constants for use later
            const responseDiv = document.getElementById("door-button-response");
            const responseSpan = responseDiv ? responseDiv.querySelector("span") : null;
            const relayValue = button.getAttribute("data-relay");
            const buttonDisableTime = button.getAttribute("data-disable-time");
            const buttonOriginalText = button.textContent;

            //Amend the button display attributes
            buttonAttributes(button, "Opening/Closing door, please wait...", true, 0);

            //Response div and span for displaying the response message
            if (responseDiv && responseSpan) {
                responseElDisplay(responseDiv, "show", 0);
                responseSpan.textContent = "Sending request...";
            }

            //Prompt user for a PIN
            const pinValue = window.prompt("Enter your PIN to activate the door:", "");
            if (pinValue === null || pinValue.trim() === "") {
                //User cancelled or entered nothing
                return;
            }

            //Make the AJAX request to the server
            fetch("/api/relay", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ relay: relayValue, pin: pinValue })
            })
            .then(response => response.json())
            .then(data => {
                //Set response text based on the returned data (Should return true)
                if (responseSpan) {
                    responseSpan.textContent = data === true ? "Request sent" : "Error, please check relay and/or PIN value";
                }

                //Hide the response div after 5 seconds
                responseElDisplay(responseDiv, "hide", 5000);

                //Amend the button display attributes
                buttonAttributes(button, buttonOriginalText, false, buttonDisableTime);
            })
            .catch(error => {
                console.error("Error:", error);

                //Set response text based on the returned data
                if (responseSpan) {
                    responseSpan.textContent = "Error, please try again";
                }
                
                //Hide the response div after 5 seconds
                responseElDisplay(responseDiv, "hide", 5000);

                //Amend the button display attributes
                buttonAttributes(button, buttonOriginalText, false, buttonDisableTime);
            });
        });
    });
});