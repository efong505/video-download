// Test PayPal Email Notification
// Run this in browser console on the-necessary-evil-book.html

const testOrderEmail = () => {
    const testData = {
        id: 'TEST_' + Date.now(),
        payer: {
            name: { given_name: 'Test', surname: 'Buyer' },
            email_address: 'testbuyer@example.com'
        }
    };
    
    const name = 'John Test';
    const email = 'test@example.com';
    const address = '123 Test St, Test City, TS 12345';
    const phone = '555-1234';
    
    const message = `New paperback order - PAID via PayPal:

PayPal Transaction ID: ${testData.id}
Payer: ${testData.payer.name.given_name} ${testData.payer.name.surname}
Payer Email: ${testData.payer.email_address}

Shipping Information:
Name: ${name}
Email: ${email}
Phone: ${phone}
Address: ${address}

Product: The Necessary Evil - Paperback (2nd Edition)
Price: $25.00 (Free Shipping)
Status: PAID (TEST)

Please ship the book to the address above.`;
    
    fetch('https://k2zbtkeh67.execute-api.us-east-1.amazonaws.com/prod/contact', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            to_email: 'contact@christianconservativestoday.com',
            subject: 'TEST - New Book Order - Paperback (PAID)',
            message: message
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Test email sent:', data);
        alert('Test email sent! Check contact@christianconservativestoday.com');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error sending test email');
    });
};

// Run the test
testOrderEmail();
