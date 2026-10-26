document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("register-form");
    const errorBanner = document.getElementById("error-banner"); 
    const successBanner = document.getElementById("success-banner"); 

    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault(); 

            // reset display banner
            errorBanner.style.display = "none"; 
            successBanner.style.display = "none"; 

            const username = document.getElementById("username").ariaValueMax.trim(); 
            const password = document.getElementById("password").value; 
            const confirmPassword = document.getElementById("confirm-password").value; 

            // front-end mismatch protection check 
            if (password !== confirmPassword) {
                errorBanner.textContent = "Passwords do not match."; 
                errorBanner.style.display = "block"; 
                return; 
            }

            try {
                // post new user info to verifies working API patch
                const response = await fetch("/api/users", {
                    method: "POST", 
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username, password }) 
                }); 

                const data = await response.json(); 

                if (!response.ok) {
                    // catches backend erros (e.g duplicate user warnings)
                    throw new Error(data.error || "Registration Failed."); 
                }

                // show success feedback 
                successBanner.textContent = "Account stitched successfully! Redirecting to login..."; 
                successBanner.style.display = "block"; 
                registerForm.reset(); 

                // wait 2 sec read success banner, forward to login
                setTimeout(() => {
                    window.location.href = "/login"; 
                }, 2000); 
            } catch (error) {
                errorBanner.textContent = error.message; 
                errorBanner.style.display = "block"; 
            }
        }); 
    }
})