var ct = 0
var ct_promo = 0
function upload(){
    var input_id = 'inputfile'
    var imgtag_id = 'mainImg'

    if(arguments[0] == 'inputbanner'){
        input_id = 'inputbanner'
        imgtag_id = 'mainBanner'
    }

    var input = document.getElementById(input_id)
    input.addEventListener('change', function(event){
        var selectedFile = event.target.files[0];
        var reader = new FileReader();

        var imgtag = document.getElementById(imgtag_id);
        imgtag.title = selectedFile.name;

        reader.onload = function(){
            imgtag.src = reader.result
        }
        reader.readAsDataURL(selectedFile)
        imgtag.class = 'active'
    })
    input.click()
}


function remove(){
    var input_id = 'inputfile'
    var img_id = 'mainImg'

    if(arguments[0] == 'inputbanner'){
        input_id = 'inputbanner'
        img_id = 'mainBanner'
    }

    var img = document.getElementById(img_id)
        img.src = '/static/admin_app/image/add_img.png'
        img.class = null
        img.title = 'add'

    var input = document.getElementById(input_id)
    input.value = ''
}


const addButton = document.getElementById('addForm')
var gallery = document.getElementById('imgGallery')
var totalNewForms = document.getElementById('id_gallery_formset-TOTAL_FORMS')
if(addButton){
    addButton.addEventListener('click', add_new_form)
}
function add_new_form(event){
    if (event){
        event.preventDefault()
    }
    const currentFormCount = gallery.children.length
    const formCopyTarget = document.getElementById('imgGallery')
    const copyEmptyFormEl = document.getElementById('empty-form').cloneNode(true)
    copyEmptyFormEl.setAttribute('style', 'display: ;')
    copyEmptyFormEl.setAttribute('id', 'form-' + ct)
    const regex = new RegExp('__prefix__', 'g')
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1)
    formCopyTarget.append(copyEmptyFormEl)
    ct++
}

var cinemaSet = document.getElementById('cinemaSet')
var totalCinemaForms = document.getElementById('id_cinema_contact_formset-TOTAL_FORMS')
function addForm(){
    const currentCinemaForm = cinemaSet.children.length
    const copyCinemaTarget = cinemaSet
    const copyEmptyCinema = document.getElementById('empty-form').cloneNode(true)
    copyEmptyCinema.style = "border-color:black; border: solid 1px; margin: 2rem; padding: 2rem; border-radius: 30px;"
    copyEmptyCinema.setAttribute('id', 'form-' + ct)
    const prefix = new RegExp('__prefix__', 'g')
    copyEmptyCinema.innerHTML = copyEmptyCinema.innerHTML.replace(prefix, currentCinemaForm)
    totalCinemaForms.setAttribute('value', currentCinemaForm + 1)
    copyCinemaTarget.append(copyEmptyCinema)
    ct++
}

const addHomeBannerButton = document.getElementById('addHomeBannerForm')
var home_banner = document.getElementById('homeBannerSet')
const totalNewHomeBannerForms = document.getElementById('id_home_banner_formset-TOTAL_FORMS')
if(addHomeBannerButton){
    addHomeBannerButton.addEventListener('click', add_home_banner_form)
}
function add_home_banner_form(event){
    if (event){
        event.preventDefault()
    }
    const currentBannerFormCount = home_banner.children.length
    const bannerCopyTarget = document.getElementById('homeBannerSet')
    const copyEmptyBanner = document.getElementById('empty-form').cloneNode(true)
    copyEmptyBanner.setAttribute('style', 'display: block;')
    copyEmptyBanner.setAttribute('style', 'margin: 1rem;')
    copyEmptyBanner.setAttribute('id', 'form-' + ct)
    const regi = new RegExp('__prefix__', 'g')
    copyEmptyBanner.innerHTML = copyEmptyBanner.innerHTML.replace(regi, currentBannerFormCount)
    totalNewHomeBannerForms.setAttribute('value', currentBannerFormCount + 1)
    bannerCopyTarget.append(copyEmptyBanner)
    ct++

}


const addPromoBannerButton = document.getElementById('addPromoBannerSet')
const totalNewPromoBannerForms = document.getElementById('id_promo_banner_formset-TOTAL_FORMS')
var promoBannerSet = document.getElementById('promoBannerSet')
if(promoBannerSet){
    addPromoBannerButton.addEventListener('click', add_promo_banner_form)
}
function add_promo_banner_form(event){
    if (event){
        event.preventDefault()
    }
    const currentPromoCount = promoBannerSet.children.length
    const promoCopyTarget = document.getElementById('promoBannerSet')
    const copyEmptyPromoEl = document.getElementById('empty-form-promo').cloneNode(true)
    copyEmptyPromoEl.setAttribute('style', 'display: block;')
    copyEmptyPromoEl.setAttribute('style', 'margin: 1rem;')
    copyEmptyPromoEl.setAttribute('id', 'pr-form-' + ct_promo)
    const regeix = new RegExp('__prefix__', 'g')
    copyEmptyPromoEl.innerHTML = copyEmptyPromoEl.innerHTML.replace(regeix, currentPromoCount)
    totalNewPromoBannerForms.setAttribute('value', currentPromoCount + 1)
    promoCopyTarget.append(copyEmptyPromoEl)
    ct_promo++
}


function addImage(par){
    var input = $(par).parent('div').find('.imageInput')[0]

    var img = $(par).parent('div').find('.imgIn')[0]
    input.addEventListener('change', function(event){
        var selectedFile = event.target.files[0];
        var reader = new FileReader();
        var imgtag = img
        imgtag.title = selectedFile.name;
        reader.readAsDataURL(selectedFile)
        reader.onload = function(){
            imgtag.src = reader.result
        }
    })
    input.click()
}


function remImg(child){
    var parent = document.getElementById('imgGallery')
    var rem_child = document.getElementById($(child).parent().parent().attr("id"))
    parent.removeChild(rem_child)

}

function remForm(child){
    var rem_elem = $(child).parent().parent().find('.delete_form')[0]
    rem_elem.checked = true
    var rem_child = document.getElementById($(child).parent().parent().attr("id"))
    console.log(rem_child)
    rem_child.style.display = 'none'

}

function delForm(child, type){
    var parent = document.getElementById(type+'BannerSet')
    var rem_child = document.getElementById($(child).parent().parent().attr("id"))
    parent.removeChild(rem_child)
}

function deleteForm(child){
    var parent = document.getElementById('cinemaSet')
    var rem_child = document.getElementById($(child).parent().parent().attr("id"))
    parent.removeChild(rem_child)
}

function switchMailing(ch_box){
    var choose_model = document.getElementById('choose_model')

    if(ch_box.id == 'all_users'){
        document.getElementById('ch_users').checked = false
        document.getElementById('all_users').value = 'on'
        choose_model.style.display = 'none'
    } else {
        document.getElementById('all_users').checked = false
        document.getElementById('all_users').value = 'off'
        choose_model.style.display = 'block'
    }

}

function concreteFile(name){
    var concreteLabel = document.getElementById('concreteLabel')
    var concrete_temp = document.getElementById('concrete_temp')
    concreteLabel.innerHTML = name
    concrete_temp.setAttribute('value', name)
}

var name = ''
function uploadFile(){
    var input_id = 'html_template'
    var input_label = 'fileLabel'
    var load_temp = document.getElementById('load_temp')
    var input = document.getElementById(input_id)
    input.addEventListener('change', function(event){
        var selectedFile = event.target.files[0];
        var input_tag = document.getElementById(input_label);
        input_tag.innerHTML = selectedFile.name;
        load_temp.setAttribute('value', selectedFile.name)
        name = selectedFile.name;
        concreteFile(name)
    })

    if(name != ''){
        concreteFile(name)
    }
    input.click()
}

function delTemp(temp_id){
    $.ajax({
        url: 'template_delete/'+temp_id,
        type: "GET",
        success: function(response){
            var template = document.getElementById(temp_id+'_template')
            var concreteLabel = document.getElementById('concreteLabel').innerHTML
            var templateLabel = document.getElementById(temp_id).innerHTML.trim()
            if (concreteLabel == templateLabel){
                document.getElementById('concreteLabel').innerHTML = ''
                document.getElementById('concrete_temp').removeAttribute('value')
            }
            template.remove()
        }
    })
}

var switcher = {
    ru:'uk',
    uk:'ru'
}
function choose_lan(lan){
    var set_lan = document.getElementById('set_'+lan);
    var rem_lan = document.getElementById('set_'+switcher[lan]);
    set_lan.setAttribute('style', 'background-color: #5f86ad;')
    rem_lan.setAttribute('style', '')
    $('.lan_'+lan+'').css('display', 'block');
    $('.lan_'+switcher[lan]+'').css('display', 'none');

}