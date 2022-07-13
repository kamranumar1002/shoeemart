var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        
        console.log('productId: ', productId, ' action: ', action)
        console.log("USER:", user)
        if (user=="AnonymousUser"){
            Swal.fire({
                title: 'You need to Login first',
                // text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Login'
              }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = "/login";
                }
              })
        }else{
            updateUserOrder(productId, action)
        }
    })
}
function updateUserOrder(productId, action){
    console.log('user is logged in')
    var url = "/update_item/";
    fetch(url,{
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) =>{
        if (!response.ok) {
            // error processing
            throw 'Error';
        }
        return response.json()
    })
    .then((data) =>{
        console.log('data', data)
        location.reload()
    })
}
