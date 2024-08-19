document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const response = await fetch('http://localhost:5000/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
    });
    const result = await response.json();
    document.getElementById('result').innerHTML = `Your position in the waitlist: ${result.position}<br>Your referral code: ${result.referralCode}`;
});
