const loginModal = document.getElementById('loginModal')
if (loginModal)
    loginModal.addEventListener('show.bs.modal', event => {
        console.log('clear')
        retLoginModal()
    })



const modal = document.getElementById('modalSize')
const content = document.getElementById('register')
const login = document.getElementById('login')
const logiBtn = document.getElementById('logiBtn')
const regiBtn = document.getElementById('regiBtn')
const regiModal = document.getElementById('regiModal')
const backLogin = document.getElementById('backLogin')
const btnDismiss = document.getElementById('btnDismiss')
const loginModalLabel = document.getElementById('loginModalLabel')
function registerModal(){
    login_form.reset()
    modal.setAttribute('class', 'modal-dialog modal-xl')
    content.setAttribute('style', 'display: block;')
    login.setAttribute('style', 'display: none;')
    logiBtn.setAttribute('style', 'display: none;')
    regiBtn.setAttribute('style', 'display: block;')
    regiModal.setAttribute('style', 'display: none;')
    backLogin.setAttribute('style', 'display: block;')
    btnDismiss.setAttribute('style', 'display: none;')
    loginModalLabel.innerHTML = 'Регистрация'
    $('.password1').html('')
}

function retLoginModal(){
    register_form.reset()
    modal.setAttribute('class', 'modal-dialog')
    content.setAttribute('style', 'display: none;')
    login.setAttribute('style', 'display: block;')
    logiBtn.setAttribute('style', 'display: block;')
    regiBtn.setAttribute('style', 'display: none;')
    regiModal.setAttribute('style', 'display: flex; justify-content: flex-end;')
    backLogin.setAttribute('style', 'display: none;')
    btnDismiss.setAttribute('style', 'display: block;')
    loginModalLabel.innerHTML = 'Вход в аккаунт'
    $('.name').html('')
    $('.email').html('')
    $('.password2').html('')
    $('.password1').html('')

}


function changeSize(){
    var header = document.getElementById('header')
    var footer = document.getElementById('footer')

    header.setAttribute('class', 'row')
    header.setAttribute('style', 'margin-left: auto; margin-right: auto; background-color: #343a40; width: 90%')

    footer.setAttribute('class', 'row')
    footer.setAttribute('style', 'margin-left: auto; margin-right: auto; background-color: #343a40; width: 90%')
}


function create_film_info(seance){
    var empty_form = document.getElementById('empty_form').cloneNode(true)
    var film_inf = document.getElementById("film_inf")

    empty_form.setAttribute('id', seance.seance)
    empty_form.setAttribute('onclick', "window.location.href='/schedule/booking/"+seance.seance+"'")
    empty_form.classList.add(seance.type)
    empty_form.classList.add(Date.parse(seance.date))
    film_inf.append(empty_form)

    var type = $("#"+seance.seance+"").find(".type")[0]
    type.innerHTML = seance.type

    var time = $("#"+seance.seance+"").find(".time")[0]
    time.innerHTML = seance.time

    var hall = $("#"+seance.seance+"").find(".hall")[0]
    hall.innerHTML = seance.hall

    var price = $("#"+seance.seance+"").find(".price")[0]
    price.innerHTML = seance.price
}

function get_type(type){
    if(arguments[1]){

        type = Date.parse(type)
        console.log(type)
    }
    var card_type = document.getElementById('card_type')
    var card_inf = document.getElementById("card_inf")
    var film_type = document.getElementById('film_type')
    var film_inf = document.getElementById("film_inf")
    card_inf.setAttribute('style', 'display: none;')
    film_type.innerHTML = ''
    var elems = $('#film_inf').find("."+type+"")
    for(var x = 0; x<elems.length; x++){
        var elem = elems[x].cloneNode(true)
        film_type.append(elem)
    }
    card_type.setAttribute('style', 'display: block;')


}

function get_all_type(){
    var card_type = document.getElementById('card_type')
    var card_inf = document.getElementById("card_inf")
//    var seance_date = document.getElementById('seance_date')
//    var seance_date_type = document.getElementById('seance_date_type')
//    seance_date_type.style.display = 'none'
//    seance_date.style.display = 'flex'
    card_type.setAttribute('style', 'display: none;')
    card_inf.setAttribute('style', 'display: block;')
}

function show_hall(cinema){
    var select_hall=document.getElementById("select_hall");
    if (cinema == 'all'){
        select_hall.style.display = 'none'
        $(select_hall).find($('.hall_all'))[0].selected = true
    } else {
        select_hall.style.display = 'block'
        $(select_hall).find($('.cinema_hall')).css('display', 'none')
        $(select_hall).find($('.'+cinema+'')).css('display', 'block')
        if(arguments[1])
            $(select_hall).find($('.hall_'+arguments[1]+''))[0].selected = true
        else
            $(select_hall).find($('.hall_all'))[0].selected = true
    }
}

function get_select_value(){
    var select_cinema=document.getElementById("select_cinema");
    var select_film=document.getElementById("select_film");
    var select_hall=document.getElementById("select_hall");

    var select_cinema_val=select_cinema.options[select_cinema.selectedIndex].value;
    var select_film_val=select_film.options[select_film.selectedIndex].value;
    var select_hall_val=select_hall.options[select_hall.selectedIndex].value;


    show_hall(select_cinema_val, select_hall_val)

    showSeance(select_cinema_val, select_film_val, select_hall_val)
}

function hide_table(){
    $.each($('.table_body'), (index, value) => {
        var day_table = $(value).parent().parent().parent()
        if (value.children.length == 0){
            day_table.css('display', 'none')
        } else {
            day_table.css('display', 'block')
        }
    })
}

const hall = [12,14,15,13,13,13,13,13,13,20]

