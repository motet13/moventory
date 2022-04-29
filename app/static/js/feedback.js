// const postWrapper = document.querySelector('#post_wrapper');
// const totalPosts = document.querySelector('#total-posts');
// const formPost = document.querySelector('form');
// const invalidPost = document.querySelector('.invalid-feedback');

// totalPosts.innerHTML = `Total Posts: ${res_post.length}`;

// res_post.forEach(post => {
//     let datePosted = new Date(post.timestamp);
//     let formattedDate = datePosted.toDateString();

//     postWrapper.innerHTML += `
//         <div class="d-flex justify-content-between p-2 border border-bottom-0 rounded-top bg-light">
//             <div><a class="text-primary text-decoration-none" href="/profile/${post.user_id}">${post.author}</a></div> 
//             <div class="text-muted">${formattedDate}</div>
//         </div>
//         <div id="message" class="p-2 mb-3 border border-top-0 bg-white"><p>${post.body}</p></div>
//     `
// });


// // View the data in HTML
// const viewDataToHTML = (data) => {

//     let datePosted = new Date(data.timestamp);
//     let formattedDate = datePosted.toDateString();

//     res_post.push({ 
//         id: data.id,
//         body: data.body,
//         timestamp: data.timestamp,
//         user_id: data.user_id,
//         author: data.author
//     });
    
//     let pushPostInnerHTML = `
//         <div class="d-flex justify-content-between p-2 border border-bottom-0 rounded-top bg-light">
//             <div><a class="text-primary text-decoration-none" href="/profile/${data.user_id}">${data.author}</a></div> 
//             <div class="text-muted">${formattedDate}</div>
//         </div>
//         <div id="message" class="p-2 mb-3 border border-top-0 bg-white"><p>${data.body}</p></div>
//     `

//     postWrapper.insertAdjacentHTML('afterbegin', pushPostInnerHTML);
//     totalPosts.innerHTML = `Total Posts: ${res_post.length}`;
//     formPost.reset();
// }


// //  send post when button is pressed.
// formPost.addEventListener('submit', e => {
//     e.preventDefault();

//     let entry = { postContent: formPost.content.value.trim() };

//     // validation
//     const postPattern = /<[a-zA-Z0-9]>|<[/a-zA-Z0-9>]{1,}>|<|>|\?>/;

//     if (!postPattern.test(entry.postContent)) {
//         // feedback good info
//         // feedback.textContent = post;
//         const sendPost = async () => {
//             const response = await fetch(`${window.origin}/post-entry`, {
//                 method: "POST",
//                 credentials: "include",
//                 body: JSON.stringify(entry),
//                 cache: "no-cache",
//                 headers: new Headers ({
//                 "content-type": "application/json"
//                 })
//             });
    
//             if (response.status !== 200) { throw new Error('Cannot fetch the data'); }
            
//             const data = await response.json();
    
//             return data;
//         }
//         // viewDataToHTML(data)
//         sendPost()
//             .then(data => viewDataToHTML(data),
//                 formPost.classList.add('was-validated'))
//             .catch(err => console.log('rejected', err.message));
//     } else {
//         // feedback help info
//         console.log(e.target.children[1]);
//         e.target.children[1].classList.add('has-validation');
//         throw new Error("Sorry, cannot accept this post.");

//     }
// });