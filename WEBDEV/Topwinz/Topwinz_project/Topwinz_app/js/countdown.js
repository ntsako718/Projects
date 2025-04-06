const raffleId = 1;  // Replace this with the dynamic raffle ID
const countdownElement = document.getElementById('raffle-timer');
const raffleStatusElement = document.getElementById('raffle-status');

// Poll the backend API every 5 seconds
setInterval(function() {
    fetch(`/api/raffle/status/${raffleId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // If the raffle has ended or no longer active, show an error or hide the timer
                raffleStatusElement.innerText = "Raffle ended or not active.";
                countdownElement.innerText = "";
            } else {
                // Display countdown or other status
                raffleStatusElement.innerText = `Raffle: ${data.raffle_name}`;
                if (data.raffle_started) {
                    countdownElement.innerText = `Time Left: ${formatTime(data.countdown)}`;
                } else {
                    countdownElement.innerText = "Waiting for raffle to start...";
                }
            }
        })
        .catch(error => console.error("Error fetching raffle status:", error));
}, 5000);  // 5000ms = 5 seconds

// Helper function to format time in seconds to mm:ss
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
}
