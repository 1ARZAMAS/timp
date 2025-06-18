document.getElementById('registrationForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const messageDiv = document.getElementById('message');
  
  try {
    const response = await fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    
    const data = await response.json();
    messageDiv.textContent = response.ok 
      ? 'Registration successful!' 
      : data.error || 'Registration failed';
    messageDiv.style.color = response.ok ? 'green' : 'red';
    
    if (response.ok) document.getElementById('registrationForm').reset();
  } catch (err) {
    messageDiv.textContent = 'Network error. Please try again.';
    messageDiv.style.color = 'red';
  }
});