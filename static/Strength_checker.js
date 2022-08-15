    // timeout before a callback is called

    let timeout;

    // traversing the DOM and getting the input and span using their IDs

    let password = document.getElementById('password')
    let confirm_passowrd = document.getElementById('confirm_password')
    let strengthBadge = document.getElementById('StrengthDisp')

  
    // The strong and weak password Regex pattern checker

    let strongPassword = new RegExp('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{16,})')
    let mediumPassword = new RegExp('((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{12,}))|((?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])(?=.{8,}))')
    
    function StrengthChecker(PasswordParameter){
        // We then change the badge's color and text based on the password strength
        // if (password != confirm_password){
        //     strengthBadge.style.backgroundColor = "red"
        //     strengthBadge.textContent = "Passwords don't match!"
        // }
        // else if (password == confirm_password){
        //     strengthBadge.style.backgroundColor = "green"
        //     strengthBadge.textContent = "Passwords match!"
        // }
        if(strongPassword.test(PasswordParameter)) {
            strengthBadge.style.backgroundColor = "green"
            strengthBadge.textContent = 'Strong Password, good job!'
        } else if(mediumPassword.test(PasswordParameter)){
            strengthBadge.style.backgroundColor = 'blue'
            strengthBadge.textContent = 'Password is ok, can be better'
        } else{
            strengthBadge.style.backgroundColor = 'red'
            strengthBadge.textContent = 'Password is too Weak!'
        }
        


    }
    

    // Adding an input event listener when a user types to the  password input 
    console.log(password)
    password.addEventListener("input", () => {

        //The badge is hidden by default, so we show it

        strengthBadge.style.display= 'block'
        clearTimeout(timeout);

        //We then call the StrengChecker function as a callback then pass the typed password to it

        timeout = setTimeout(() => StrengthChecker(password.value), 500);

        //Incase a user clears the text, the badge is hidden again

        if(password.value.length !== 0){
            strengthBadge.style.display != 'block'
        } else{
            strengthBadge.style.display = 'none'
        }
    });