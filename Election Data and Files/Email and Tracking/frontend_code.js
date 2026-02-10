/**
 * Frontend JavaScript for Email Subscription
 * Replace the subscribeEmail() function in election-map.html with this code
 */

// IMPORTANT: Replace with your actual API Gateway URL after deployment
const EMAIL_API_ENDPOINT = 'https://niexv1rw75.execute-api.us-east-1.amazonaws.com';

async function subscribeEmail() {
    const emailInput = document.getElementById('email-input');
    const firstNameInput = document.getElementById('first-name-input');
    const lastNameInput = document.getElementById('last-name-input');
    
    const email = emailInput.value.trim();
    const firstName = firstNameInput ? firstNameInput.value.trim() : '';
    const lastName = lastNameInput ? lastNameInput.value.trim() : '';

    // Validate email format
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert('Please enter a valid email address.');
        return;
    }
    
    // Validate first name
    if (!firstName) {
        alert('Please enter your first name.');
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
            body: JSON.stringify({ 
                email: email,
                first_name: firstName,
                last_name: lastName
            })
        });

        const data = await response.json();

        if (response.ok) {
            const banner = document.getElementById('email-capture-banner');
            
            // Check if already subscribed
            if (data.message === 'already_subscribed') {
                banner.innerHTML = `
                    <div class="text-center py-3">
                        <h5 class="text-info mb-2">✓ Already Subscribed!</h5>
                        <p class="mb-0">
                            <strong>${email}</strong> is already on our mailing list.
                        </p>
                        <small class="text-muted">
                            You'll continue receiving election updates and voter guides.
                        </small>
                    </div>
                `;
            } else if (data.message === 'confirmation_resent') {
                banner.innerHTML = `
                    <div class="text-center py-3">
                        <h5 class="text-info mb-2">✓ Confirmation Email Resent!</h5>
                        <p class="mb-0">
                            Check your inbox at <strong>${email}</strong>
                        </p>
                        <small class="text-muted">
                            Please click the confirmation link to complete your subscription.
                        </small>
                    </div>
                `;
            } else if (data.message === 'resubscribed') {
                banner.innerHTML = `
                    <div class="text-center py-3">
                        <h5 class="text-success mb-2">✓ Welcome Back!</h5>
                        <p class="mb-0">
                            You've been resubscribed! Confirmation email sent to <strong>${email}</strong>
                        </p>
                        <small class="text-muted">
                            Check your inbox (and spam folder) for your welcome email.
                        </small>
                    </div>
                `;
            } else {
                // New subscription - pending confirmation
                banner.innerHTML = `
                    <div class="text-center py-3">
                        <h5 class="text-success mb-2">✓ Almost Done!</h5>
                        <p class="mb-0">
                            Confirmation email sent to <strong>${email}</strong>
                        </p>
                        <small class="text-muted">
                            Please check your inbox and click the confirmation link to complete your subscription.
                        </small>
                    </div>
                `;
            }

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
