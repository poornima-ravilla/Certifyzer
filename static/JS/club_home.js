const profileImage = document.getElementById("profileImage");
const imageUpload = document.getElementById("imageUpload");

profileImage.addEventListener("click", () => {
    imageUpload.click(); 
});

imageUpload.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            profileImage.src = e.target.result; 
        };
        reader.readAsDataURL(file); 
    }        
});



let evedet=document.getElementById("rightbelow2");
let clubdet=document.getElementById("rightbelow");
let clubedit=document.getElementById("rightbelow3");

evedet.style.display = 'none';
function EventsView(eventName, eventDate, eventPoints, eventDesc){
    document.getElementById('eventName').innerHTML = eventName;
    document.getElementById('eventDate').innerHTML = eventDate;
    document.getElementById('eventPoints').innerHTML = eventPoints;
    document.getElementById('eventDesc').innerHTML = eventDesc;
    clubdet.style.display = 'none';
    clubedit.style.display='none';
    evedet.style.display = 'block';
    
}
let evedet2=document.getElementById("rightbelow3");
evedet2.style.display = 'none';

function editclub(faculty,president,email,contact){
    document.querySelector("input[name='faculty']").value = faculty;
    document.querySelector('input[name="president"]').value = president;
    document.querySelector('input[name="email"]').value = email;
    document.querySelector('input[name="contact"]').value = contact;
   

    clubdet.style.display = 'none';
    evedet2.style.display = 'block';
}
let close=document.getElementById("close");
let closeclub=document.getElementById("closeclub");
let closeadd=document.getElementById("closeadd");
let closeedit=document.getElementById("closeedit");
let closeedit2=document.getElementById("closeedit2");

close.addEventListener("click", function () {
    console.log("clicked");
    evedet.style.display = 'none';
    clubdet.style.display = 'block';
});

closeclub.addEventListener("click", function () {
    console.log("clicked");
    clubedit.style.display = 'none';
    clubdet.style.display = 'block';
});

closeadd.addEventListener("click", function () {
    console.log("clicked");
    layer2.style.display = 'none';
    layer1.style.display = 'flex';
    logoutbtn.classList.remove('disabled');

});
closeedit.addEventListener("click", function () {
    console.log("clicked");
    layer3.style.display = 'none';
    layer1.style.display = 'flex';
    logoutbtn.classList.remove('disabled');

});
let body=document.getElementById("body");
let inneradd=document.getElementById("inneradd");
closeedit2.addEventListener("click", function () {
    console.log("clicked");
    layer4.style.display = 'none';
    body.classList.remove('disabled');
    inneradd.classList.remove('disabled');
    layer3.classList.remove('disabled');

   
});
let layer2=document.getElementById("layer2");
let layer1=document.getElementById("layer1");
layer2.style.display="none";
layer4.style.display="none";
layer3.style.display="none";


function addeve(){
    layer1.style.display="none";
    layer2.style.display="block";
    logoutbtn.classList.add('disabled');

}
closeadd.addEventListener("click",function(){
    layer2.style.display="none";
    layer1.style.display="flex";

});
function editeve(){
    
    layer1.style.display="none";
    layer3.style.display="block";
    logoutbtn.classList.add('disabled');

}
let logoutbtn=document.getElementById("logoutbtn");
function Eventsedit(id,evename, date, points, desc,list){
    document.querySelector('.clubbname').textContent = evename;
    console.log(evename);  

    document.querySelector("input[name='eventId']").value = id;
    document.querySelector('input[name="evetname"]').value = evename;
    document.querySelector('input[name="evedate"]').value = date;
    document.querySelector('input[name="evepoints"]').value = points;
    document.querySelector('input[name="evedesc"]').value = desc;
    // document.querySelector('input[name="evetfile"]').value = list;
    filename = list.split(/(\\|\/)/g).pop();
    document.getElementById("filu").innerHTML=filename;

    console.log(list);//solve here this error its emplty
    

    layer4.style.display="block";
    logoutbtn.classList.add('disabled');
    inneradd.classList.add('disabled');
    layer3.classList.add('disabled');


}
function backhome(){
    // clubdet.style.display = 'block';
    // evedet2.style.display = 'none';
    // evedet.style.display = 'none';
    // clubedit.style.display = 'none';
    layer2.style.display = 'none';
    
    layer3.style.display = 'none';
    logoutbtn.classList.remove('disabled');
    
    layer4.style.display = 'none';
    layer1.style.display='flex';
    
    
}
function logout() {
        window.location.href = "/logout";
}  
