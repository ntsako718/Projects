// Function to handle celebration effects
function triggerCelebration() {
    // Check if confetti is available
    if (typeof confetti !== 'function') {
        console.error('Confetti library not loaded');
        return;
    }
    
    // Create multiple bursts of confetti
    const duration = 3000;
    const end = Date.now() + duration;
    
    // Create an intense burst at the center
    confetti({
        particleCount: 150,
        spread: 100,
        origin: { y: 0.6 }
    });
    
    // Create smaller bursts from the sides
    setTimeout(() => {
        confetti({
            particleCount: 50,
            angle: 60,
            spread: 55,
            origin: { x: 0 }
        });
        
        confetti({
            particleCount: 50,
            angle: 120,
            spread: 55,
            origin: { x: 1 }
        });
    }, 250);
}

// Initialize all celebration buttons when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing celebration buttons...');
    
    // Get all celebrate buttons
    const celebrateButtons = document.querySelectorAll('.celebrate-btn');
    console.log('Found ' + celebrateButtons.length + ' celebration buttons');
    
    // Add click event listener to each button
    celebrateButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            console.log('Celebrate button clicked!');
            
            // Trigger the celebration
            triggerCelebration();
            
            // Button animation
            this.classList.add('button-active');
            setTimeout(() => {
                this.classList.remove('button-active');
            }, 300);
            
            // Add vibration if available
            if (navigator.vibrate) {
                navigator.vibrate([100, 50, 100]);
            }
            
            // Prevent default action and stop propagation
            e.preventDefault();
            e.stopPropagation();
        });
    });
    
    // Test function accessible from console for debugging
    window.testConfetti = triggerCelebration;
});