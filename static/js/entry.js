async function like(e, pid) {
    let like_icon = e.querySelector('.material-symbols-outlined')
    let like_count = e.parentNode.children[1].querySelector('.like_count')
    let like_label = e.parentNode.children[1].querySelector('.like_label')
    // request for like
    let req = await fetch("/api/entry/like?pid=" + pid, {method: 'PATCH'})
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
    }
}

async function archive(pid) {
    let req = await fetch("/api/entry/archive?pid=" + pid, {method: 'PATCH'})
    if (req.status === 200) {
        location.reload()
    }
}

async function delete_post(pid) {
    let req = await fetch("/api/entry?pid=" + pid, {method: 'DELETE'})

    location.reload()
    toastEl = `<div class="toast align-items-center" role="alert" aria-live="assertive" aria-atomic="true">
  <div class="d-flex">
    <div class="toast-body">
    Hello, world! This is a toast message.
   </div>
    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
  </div>
</div>`
    const toast = new bootstrap.Toast(toastEl)
    toast.show()

}

function showCreatePost(t, c, pid = null, content = null) {
    const submit_btn = document.getElementById('sb-btn')
    const edit_btn = document.getElementById('edit-btn')
    const label = document.getElementById('newPostLabel')
    const pidc = document.getElementById('pid')
    const editor = document.getElementById('wmd-input')
    if (c === 'c') {
        // for create function
        label.textContent = 'Create Entry'

        edit_btn.style.display = 'none'
        submit_btn.style.display = 'block'
    } else if (c === 'e') {
        // for edit button
        label.textContent = 'Edit Entry'
        editor.value = content
        pidc.setAttribute('value', pid)
        edit_btn.style.display = 'block'
        submit_btn.style.display = 'none'
    }
    document.getElementById('shadow').style.display = t
    document.getElementById('frame2').style.display = t
}

async function uploadFile(e) {
    const toUpload = e.files[0]
    let data = new FormData();
    data.append('file', toUpload)


    let res = await fetch(`/api/entry/upload`, {
        method: 'POST', body: data
    }).then((response) => response.json()).then((data) => data)


    const myValue = `![enter image description here](${res})`
    const myField = document.getElementById('wmd-input')
    const pos = myField.selectionStart
    if (pos || pos === '0') {
        var endPos = myField.selectionEnd;
        myField.value = myField.value.substring(0, pos) + myValue + myField.value.substring(endPos, myField.value.length);
        myField.selectionStart = pos + myValue.length;
        myField.selectionEnd = pos + myValue.length;
    } else {
        myField.value += myValue;
    }


}

async function edit_post(el) {
    el = el.parentNode.parentNode.children
    pid = el[0].value
    content = el[2].querySelector('#wmd-input').value
    var url = new URL("http://127.0.0.1:5000/api/entry")
    url.searchParams.append('pid', pid)
    url.searchParams.append('content', content)
    response = await fetch(url.toString(), {
        method: 'PUT', credentials: 'include'
    }).then((res) => {
        if (res.ok) {
            location.reload()
        }
    })
}

async function create_post(e) {
    el = e.parentNode.parentNode.children
    content = el[2].querySelector('#wmd-input').value
    var url = new URL("http://127.0.0.1:5000/api/entry")
    url.searchParams.append('content', content)
    response = await fetch(url.toString(), {
        method: 'POST', credentials: 'include'
    }).then((res) => {
        if (res.ok) {
            location.reload()
        } else {
            e.parentNode.parentNode.insertAdjacentHTML('beforebegin', `<div class="alert alert-danger" role="alert">
  Some thing went wrong. Are you logged in?
</div>`)
        }
    })
}
