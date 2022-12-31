function hide_comments() {
    let comms = document.querySelectorAll("#commentx");
    comms.forEach(function (d, i) {
        d.style.display = "none";
    });
}

async function comments_hider(el, pid) {
    hide_comments()
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
                                <button type="button" onclick="hide_comments()" class="btn btn-outline-primary btn-sm">Cancel</button>
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

async function followers(func, email) {
    let children = document.getElementById('user_list_children');
    let container = document.getElementById('userlist');
    let label = document.getElementById('userlistLabel')
    let loaded = '';
    let follower_list = await fetch('http://127.0.0.1:5000/api/user?func='+func+'&email=' + email, {method: 'GET'}).then((response) => response.json()).then((data) => data)
    for (f in follower_list) {
        loaded += `
            <div class="d-flex flex-start align-items-center">
                                <img class="rounded-circle shadow-1-strong me-3"
                                     src="${c['profile_pic']}"
                                     alt="avatar" width="60"
                                     height="60"/>
                                <div>
                                    ${follower_list}
                                    <h6 onclick="location.href='/user/{{ p.username }}'"
                                        class="fw-bold text-primary mb-1">${c['name']}</h6>
                                    <p class="text-muted small mb-0">
                                        ${c['username']} - ${c['email']}
                                    </p>
                                </div>
                            </div>
         `
    }
    children.innerHTML = loaded;
    if (func == 'followers'){
        label.textContent='Followers';
    }else if (func == 'followings'){
        label.textContent='Following';
    }
    const modal =  new bootstrap.Modal(container)
    modal.show()


}