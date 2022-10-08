/*Sticky Header*/
window.addEventListener("scroll",function(){
  if(this.scrollY > 60){
    document.querySelector(".header").classList.add("sticky");
  } else {
    document.querySelector(".header").classList.remove("sticky");
  }
});