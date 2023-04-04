async function list_users(func, email) {
    let children = document.getElementById('user_list_children');
    let container = document.getElementById('userlist');
    let label = document.getElementById('userlistLabel')
    let loaded = '';
    let follower_list = await fetch('/api/user/' + func + '?email=' + email, {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
    for (c in follower_list) {
        let is_Following = await fetch('/api/user/' + 'is_following' + '?email=' + follower_list[c]['email'], {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
        loaded += `
            <div class="me-2 d-flex justify-content-between align-items-center">
            <div class="d-flex flex-start align-items-center">
                                <img class="rounded-circle shadow-1-strong me-3"
                                     src="${follower_list[c]['profile_pic']}"
                                     alt="avatar" width="60"
                                     height="60"/>
                                <div>
                                  
                                    <h6 onclick="location.href='/user/${follower_list[c]['username']}'" class="fw-bold text-primary mb-1">${follower_list[c]['name']}</h6>
                                    <p class="text-muted small mb-0">
                                        ${follower_list[c]['username']} - ${follower_list[c]['email']}
                                    </p>
                                </div></div>
                                <div onclick="follow(this,'${follower_list[c]['email']}')" class="btn btn-secondary ">${is_Following ? "Unfollow" : "Follow"}</div>
                                
                            </div>
                            
         `
        if (c + 1 < follower_list.length) {
            loaded += `<hr>`;
        }
    }
    children.innerHTML = loaded;
    if (func === 'followers') {
        label.textContent = 'Followers';
    } else if (func === 'followings') {
        label.textContent = 'Followings';
    }
    const modal = new bootstrap.Modal(container)
    modal.show()


}

async function list_doers(func, pid) {
    let children = document.getElementById('user_list_children');
    let container = document.getElementById('userlist');
    let label = document.getElementById('userlistLabel')
    let loaded = '';
    let follower_list = await fetch('/api/entry/' + func + '?pid=' + pid, {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
    for (c in follower_list) {
        let is_Following = await fetch('/api/user/' + 'is_following' + '?email=' + follower_list[c]['email'], {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
        loaded += `
            <div class="me-2 d-flex justify-content-between align-items-center">
            <div class="d-flex flex-start align-items-center">
                                <img class="rounded-circle shadow-1-strong me-3"
                                     src="${follower_list[c]['profile_pic']}"
                                     alt="avatar" width="60"
                                     height="60"/>
                                <div>
                                  
                                    <h6 onclick="location.href='/user/${follower_list[c]['username']}'" class="fw-bold text-primary mb-1">${follower_list[c]['name']}</h6>
                                    <p class="text-muted small mb-0">
                                        ${follower_list[c]['username']} - ${follower_list[c]['email']}
                                    </p>
                                </div></div>
                                <div onclick="follow(this,'${follower_list[c]['email']}')" class="btn btn-secondary ">${is_Following ? "Unfollow" : "Follow"}</div>
                                
                            </div>
                            
         `
        if (c + 1 < follower_list.length) {
            loaded += `<hr>`;
        }
    }
    children.innerHTML = loaded;
    if (func === 'likes') {
        label.textContent = 'Likes';
    } else if (func === 'shares') {
        label.textContent = 'Shares';
    }
    const modal = new bootstrap.Modal(container)
    modal.show()


}

async function search_users() {
    let children = document.getElementById('search_list_children');
    let term = document.getElementById('search_term').value
    let loaded = ``;

    const users_list = await fetch('/api/user/search?term=' + term, {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
    for (c in users_list) {
        let is_Following = await fetch('/api/user/is_following?email=' + users_list[c]['email'], {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
        loaded += `
            <div class="me-2 d-flex justify-content-between align-items-center">
            <div class="d-flex flex-start align-items-center">
                                <img class="rounded-circle shadow-1-strong me-3"
                                     src="${users_list[c]['profile_pic']}"
                                     alt="avatar" width="60"
                                     height="60"/>
                                <div>
                                  
                                    <h6 onclick="location.href='/user/${users_list[c]['username']}'" class="fw-bold text-primary mb-1">${users_list[c]['name']}</h6>
                                    <p class="text-muted small mb-0">
                                        ${users_list[c]['username']} - ${users_list[c]['email']}
                                    </p>
                                </div></div>
                                <div onclick="follow(this,'${users_list[c]['email']}')" class="btn btn-secondary ">${is_Following ? "Unfollow" : "Follow"}</div>
                                
                            </div>
                            
         `
        if (c < users_list.length - 1) {
            loaded += `<hr>`;
        }
    }
    children.innerHTML = loaded;
    if (!term) {
        children.innerHTML = loaded;
    }
    // children.insertAdjacentHTML( 'beforeend', loaded );
}

async function is_user(username) {
    let req = await fetch("/api/user/is_available?username=" + username, {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
    if (req === 'Username is available') {
        return true

    }
    return false
}

async function validate_username(original) {

    let parent = document.querySelector('#username_inputfield')
    const input = parent.children[1].children[0]
    const username = input.value
    const test = await is_user(username).then((res) => res).then(res => res)
    const label = parent.children[0]
    if (username && (username === original || test) && /^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$/.test(username)) {
        input.classList.remove('is-invalid')
        label.classList.remove('validationError')
        input.classList.remove('text-danger')
        input.classList.add('is-valid')
        label.classList.add('validationSuccess')
        input.classList.add('text-success')
    } else {
        input.classList.remove('is-valid')
        label.classList.remove('validationSuccess')
        input.classList.remove('text-success')
        input.classList.add('is-invalid')
        label.classList.add('validationError')
        input.classList.add('text-danger')
    }
}

async function update_user() {
    const forms = document.querySelectorAll('.form_field')
    const profile_pic = forms[1].files[0]
    const name_ = forms[2].value
    const username = forms[3].value
    const bio = forms[4].value

    let data = new FormData();
    data.append('profile_pic', profile_pic)

    let response = await fetch(`/api/user?username=${username}&bio=${bio}&name=${name_}`, {
        method: 'PUT', body: data
    })
    if (response.status === 200) {
        location.reload()
    } else if (response.status === 405) {
        forms[0].parentNode.insertAdjacentHTML('beforebegin', `<div class="alert alert-danger" role="alert">
  Some thing went wrong. Are you logged in?
</div>`)
    }

}

async function follow(element, email) {
    req = await fetch("/api/user/follow?email=" + email, {method: 'PATCH'})
    if (req.status === 200) {
        element.textContent = "Unfollow";
    } else if (req.status === 417) {
        element.textContent = "Follow";
    }
}

async function delete_user(e, username) {
    req = await fetch("/api/user?username=" + username, {method: 'DELETE'})
    if (req.status === 200) {
        location.reload()
    } else {
        e.parentNode.insertAdjacentHTML('beforebegin', `<div class="alert alert-danger" role="alert">
  Some thing went wrong. Please try again later.
</div>`)
    }
}





