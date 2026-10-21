document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("Login-form"); 
    const errorBanner = document.getElementById("error-banner"); 

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault(); // prevent page reloading

            // clear prior error state 
            errorBanner.style.display = "none"; 
            errorBanner.textContent = ""; 

            // gather inputs 
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value; 
            
            try {
                // post credentials -> backend API
                const response = await fetch("/api/login", {
                    method: "POST", 
                    headers: {
                        "Content-Type": "application/json"
                    }, 
                    body: JSON.stringify({ username, password })
                }); 

                const data = await response.json(); 

                if (!response.ok) {
                    // display backend validation failures
                    throw new Error(data.error || "Failed to log in.")
                }

                // login success: redirect to dashboard
                window.location.href = "/"; 
            } catch (error) {
                // surface errors dunamically in banner 
                errorBanner.textContent = error.message; 
                errorBanner.style.display = "block"; 
            }

        });
    }
}); 