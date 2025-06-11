/**
 * This script handles the AJAX request for the door button
 */
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".door-button").forEach(function(button) {
        button.addEventListener("click", function() {
            event.preventDefault(); // Prevent default button action

            //Prompt user for a PIN
            const pinValue = window.prompt("Enter your PIN to activate the door:", "");
            if (pinValue === null || pinValue.trim() === "") {
                // User cancelled or entered nothing
                return;
            }

            //Relay value
            const relayValue = button.getAttribute("data-relay");

            //Response div and span for displaying the response message
            const responseDiv = document.getElementById("door-button-response");
            const responseSpan = responseDiv ? responseDiv.querySelector("span") : null;
            if (responseDiv && responseSpan) {
                responseDiv.style.display = "flex";
                responseSpan.textContent = "Loading";
            }

            // Disable the button until a response is provided
            button.disabled = true;

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
                    responseSpan.textContent = data === true ? "Completed" : "Error, please check relay and/or PIN value";
                }

                button.disabled = false;

                // Hide the response div after 3 seconds
                if (responseDiv) {
                    setTimeout(() => {
                        responseDiv.style.display = "none";
                    }, 3000);
                }
            })
            .catch(error => {
                //Set response text based on the returned data
                if (responseSpan) {
                    responseSpan.textContent = "Error, please try again";
                }

                button.disabled = false;
                
                // Hide the response div after 3 seconds
                if (responseDiv) {
                    setTimeout(() => {
                        responseDiv.style.display = "none";
                    }, 3000);
                }
                console.error("Error:", error);
            });
        });
    });
});