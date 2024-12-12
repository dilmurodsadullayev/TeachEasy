let infoOfTeacher = {
  nameofTeacher: document.querySelector('.name-of-teacher'),
  imgUrl: document.querySelector('.img-url'),
  nameofJob: document.querySelector('.name-of-job')
},
  listOfTeacher = document.querySelector('.list-of-teacher')




function create() {
  let div = document.createElement('div')
  div.classList.add('col-md-6')
  div.classList.add('col-lg-3')
  div.classList.add('text-center')
  div.classList.add('team')
  div.classList.add('mb-5')
  div.innerHTML = `
    <div class="position-relative overflow-hidden mb-4" style="border-radius: 100%;">
        <img class="img-fluid w-100" src="${infoOfTeacher.imgUrl.value}" alt="">
        <div
            class="team-social d-flex align-items-center justify-content-center w-100 h-100 position-absolute">
            <a class="btn btn-outline-light text-center mr-2 px-0" style="width: 38px; height: 38px;"
                href="#"><i class="fab fa-twitter"></i></a>
            <a class="btn btn-outline-light text-center mr-2 px-0" style="width: 38px; height: 38px;"
                href="#"><i class="fab fa-facebook-f"></i></a>
            <a class="btn btn-outline-light text-center px-0" style="width: 38px; height: 38px;" href="#"><i
                    class="fab fa-linkedin-in"></i></a>
        </div>
    </div>
    <h4>${infoOfTeacher.nameofTeacher.value}</h4>
    <i>${infoOfTeacher.nameofJob.value}</i>
  `


  listOfTeacher.append(div)
}