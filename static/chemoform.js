let date1 = document.getElementById('id_chemodate');id_d1dose
let d1_dose = document.getElementById('id_d1dose');
let d2_dose = document.getElementById('id_d2dose');
let d3_dose = document.getElementById('id_d3dose');
let d4_dose = document.getElementById('id_d4dose');
let d5_dose = document.getElementById('id_d5dose');

let s_date1 = document.getElementById('id_sdate1');
let f_date1 = document.getElementById('id_fdate1');
let s_date2 = document.getElementById('id_sdate2');
let f_date2 = document.getElementById('id_fdate2');
let s_date3 = document.getElementById('id_sdate3');
let f_date3 = document.getElementById('id_fdate3');
let s_date4 = document.getElementById('id_sdate4');
let f_date4 = document.getElementById('id_fdate4');
let s_date5 = document.getElementById('id_sdate5');
let f_date5 = document.getElementById('id_fdate5');

d1_dose.addEventListener('focusout', () => {
    s_date1.value = date1.value
    f_date1.value = date1.value
})

d2_dose.addEventListener('focusout', () => {
    s_date2.value = s_date1.value
    f_date2.value = f_date1.value
})

d3_dose.addEventListener('focusout', () => {
    s_date3.value = s_date2.value
    f_date3.value = f_date2.value
})

d4_dose.addEventListener('focusout', () => {
    s_date4.value = s_date3.value
    f_date4.value = f_date3.value
})

d5_dose.addEventListener('focusout', () => {
    s_date5.value = s_date4.value
    f_date5.value = f_date4.value
})

