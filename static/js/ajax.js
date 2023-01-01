function hide_all_comments() {
    let comms = document.querySelectorAll("#commentx");
    comms.forEach(function (d, i) {
        d.style.display = "none";
    });
}

async function comments_hider(el, pid) {
    hide_all_comments()
    let count = 1;
    let comment_elements = el.parentNode.parentNode.parentNode.querySelector('#commentx')


    // #get comments
    let loaded_comments = "";
    let comment_list = await fetch('http://127.0.0.1:5000/api/comment?pid=' + pid, {method: 'GET'}).then((response) => response.json()).then((data) => data)
    for (c in comment_list) {
        loaded_comments += `<div class="card-footer py-3 border-0" style="background-color: #f8f9fa;">
                        <div class="d-flex flex-start w-100">
                            <img class="rounded-circle shadow-1-strong me-3"
                                 src="${comment_list[c]['profile_pic']}" alt="avatar"
                                 width="40"
                                 height="40"/>
                            <div class="d-flex flex-start flex-column form-outline w-100">
                                <small class="text-primary">${comment_list[c]['username']}</small>
                                <small class="text-secondary">${comment_list[c]['timestamp']}</small>
                                <small>${comment_list[c]['content']}</small>

                            </div>
                            <button onclick=""
                                    class=" btn btn-sm d-flex align-items-center me-1">

                                <span class="like reshare_icon material-symbols-outlined me-2">delete</span>
                            </button>
                        </div>
                    </div>`
    }
    comment_elements.innerHTML = loaded_comments;
    comment_elements.innerHTML += `<div class="card-footer py-3 border-0" style="background-color: #f8f9fa;">

                            <div id="cl1" class="d-flex flex-start w-100">
<!--                                    <img class="rounded-circle shadow-1-strong me-3"-->
<!--                                         src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(19).webp" alt="avatar"-->
<!--                                         width="40"-->
<!--                                         height="40"/>-->
                                <div id="cl2" class="form-outline w-100">
            <input class="form-control NewComment" id="NewComment" type="text" 
                      style="background: #fff;word-break: break-word;"></input>
                                </div>
                            </div>
                            <div class="float-end mt-2 pt-1">
                                <button type="button" onclick="post_comment(this,'${pid}')" class="btn btn-primary btn-sm">Post comment</button>
                                <button type="button" onclick="hide_all_comments()" class="btn btn-outline-primary btn-sm">Cancel</button>
                            </div>
                        </div>`
    // #show comments section
    if (comment_elements.style.display === 'none') {
        comment_elements.style.display = 'block'
    } else {
        comment_elements.style.display = 'none';
    }

}

async function post_comment(inx, pid) {
    inx.disabled = true;
    content = inx.parentElement.parentElement.querySelector('#NewComment').value;
    response = await fetch('http://127.0.0.1:5000/api/comment?pid=' + pid + '&content=' + content, {
        method: 'POST',
        credentials: 'include'
    }).then((res) => {
        if (res.ok) {
            inx.disabled = false
        }
    })
    comments_hider(inx.closest('section'), pid)
}

async function like(e, pid) {
    let like_icon = e.querySelector('.material-symbols-outlined')
    let like_count = e.querySelector('.like_count')
    let like_label = e.querySelector('.like_label')
    // request for like
    let req = await fetch("/api/entry?func=like&pid=" + pid, {method: 'PATCH'})
    // update icon and likecount
    if (req.status === 200) {
        like_icon.classList.add('liked');
        like_count.textContent = parseInt(like_count.textContent || 0) + 1
    } else if (req.status === 417) {
        like_icon.classList.remove('liked');
        like_count.textContent = like_count.textContent - 1
    }
    // update the likeslabel
    if (like_count.textContent > 1) {
        like_label.textContent = 'Likes'
    } else if (like_count.textContent == 1) {
        like_label.textContent = 'Like'
    } else {
        like_count.textContent = ''
        like_label.textContent = ''
    }
}

async function repost(e, pid) {
    let repost_icon = e.querySelector('.repost_icon')
    let repost_count = e.querySelector('.repost_count')
    req = await fetch("/api/entry?func=share&pid=" + pid, {method: 'PATCH'})
    if (req.status === 200) {
        repost_icon.classList.add('text-primary');
        repost_count.textContent = parseInt(repost_count.textContent || 0) + 1

    } else if (req.status === 417) {
        repost_icon.classList.remove('liked');
        repost_count.textContent = repost_count.textContent - 1

    }

}

async function archive(pid) {
    let req = await fetch("/api/entry?func=archive&pid=" + pid, {method: 'PATCH'})
    if (req.status === 200) {
        location.reload()
    }
}

async function delete_post(pid) {
    let req = await fetch("/api/entry?pid=" + pid, {method: 'DELETE'})
    if (req.status === 200) {
        location.reload()
    }
}

async function list_users(func, email) {
    let children = document.getElementById('user_list_children');
    let container = document.getElementById('userlist');
    let label = document.getElementById('userlistLabel')
    let loaded = '';
    let follower_list = await fetch('http://127.0.0.1:5000/api/user?func=' + func + '&email=' + email, {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
    for (c in follower_list) {
        let is_Following = await fetch('http://127.0.0.1:5000/api/user?func=' + 'is_following' + '&email=' + follower_list[c]['email'], {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
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
    if (func == 'followers') {
        label.textContent = 'Followers';
    } else if (func == 'followings') {
        label.textContent = 'Followings';
    }
    const modal = new bootstrap.Modal(container)
    modal.show()


}


async function search_users() {
    let children = document.getElementById('search_list_children');
    let term = document.getElementById('search_term').value
    let loaded = ``;

    const users_list = await fetch('http://127.0.0.1:5000/api/user?func=search&term=' + term, {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
    for (c in users_list) {
        let is_Following = await fetch('http://127.0.0.1:5000/api/user?func=' + 'is_following' + '&email=' + users_list[c]['email'], {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
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
        if (c  < users_list.length-1) {
            loaded += `<hr>`;
        }
    }
    children.innerHTML = loaded;
    if (!term) {
        children.innerHTML = loaded;
    }
    // children.insertAdjacentHTML( 'beforeend', loaded );
    console.log(children)
}

async function is_user(username) {
    let req = await fetch("http://127.0.0.1:5000/api/user?func=is_available&username=" + username, {method: 'PATCH'}).then((response) => response.json()).then((data) => data)
    return !!req[0];
}

async function validate_username(original) {

    let parent = document.querySelector('#username_inputfield')
    const input = parent.children[1].children[0]
    const username = input.value
    const test = await is_user(username).then((res) => res).then(res => res)
    const label = parent.children[0]
    if (username && (username === original || !test)) {
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
    const name_ = forms[0].value
    const username = forms[1].value
    const bio = forms[2].value

    let response = await fetch(`http://127.0.0.1:5000/api/user?username=${username}&bio=${bio}&name=${name_}`, {method: 'PUT'})
    if (response.status === 200) {
        location.reload()
    }else if (response.status === 405){
        console.log(document.querySelector('#current_username').textContent)
    }

}

async function follow(element, email){
    req = await fetch("http://127.0.0.1:5000/api/user?func=follow&email=" + email, {method: 'PATCH'})
    if (req.status === 200) {
        element.textContent = "Unfollow";
    } else if (req.status === 417) {
        element.textContent = "Follow";
    }
}