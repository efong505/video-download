/**
 * Frontend JavaScript for Email Subscription
 * Replace the subscribeEmail() function in election-map.html with this code
 */

// IMPORTANT: Replace with your actual API Gateway URL after deployment
const EMAIL_API_ENDPOINT = 'https://niexv1rw75.execute-api.us-east-1.amazonaws.com';

async function subscribeEmail() {
    const emailInput = document.getElementById('email-input');
    const email = emailInput.value.trim();

    // Validate email format
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    // Disable button during submission
    const submitButton = event.target;
    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = 'Subscribing...';

    try {
        const response = await fetch(EMAIL_API_ENDPOINT + '/subscribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email })
        });

        const data = await response.json();

        if (response.ok) {
            // Show success message
            const banner = document.getElementById('email-capture-banner');
            banner.innerHTML = `
                <div class="text-center py-3">
                    <h5 class="text-success mb-2">✓ Thank You for Subscribing!</h5>
                    <p class="mb-0">
                        Confirmation email sent to <strong>${email}</strong>
                    </p>
                    <small class="text-muted">
                        Check your inbox (and spam folder) for your welcome email.
                    </small>
                </div>
            `;

            // Track subscription in Google Analytics (if available)
            if (typeof gtag !== 'undefined') {
                gtag('event', 'email_subscription', {
                    'event_category': 'engagement',
                    'event_label': 'election_map'
                });
            }
        } else {
            // Show error message
            alert(data.error || 'Subscription failed. Please try again.');
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    } catch (error) {
        console.error('Subscription error:', error);
        alert('There was an error subscribing. Please check your internet connection and try again.');
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }
}

// Allow Enter key to submit email
document.addEventListener('DOMContentLoaded', () => {
    const emailInput = document.getElementById('email-input');
    if (emailInput) {
        emailInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                subscribeEmail();
            }
        });
    }
});
