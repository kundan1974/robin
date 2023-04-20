let d1 = document.getElementById('id_dosephase1');
let f1 = document.getElementById('id_fxphase1');
let d2 = document.getElementById('id_dosephase2')
let f2 = document.getElementById('id_fxphase2')
let d3 = document.getElementById('id_dosephase3')
let f3 = document.getElementById('id_fxphase3')
let d4 = document.getElementById('id_dosephase4')
let f4 = document.getElementById('id_fxphase4')
let td = document.getElementById('id_totaldose')
let tfx = document.getElementById('id_totalfractions')
let donefr = document.getElementById("id_donefr")
d1.addEventListener('focusout', () => {
    td.value = Number(d1.value)
})
f1.addEventListener('focusout', () => {
    tfx.value = Number(f1.value)
})
d2.addEventListener('focusout', () => {
    td.value = Number(d1.value) + Number(d2.value)
})
f2.addEventListener('focusout', () => {
    tfx.value = Number(f1.value) + Number(f2.value)
})
d3.addEventListener('focusout', () => {
    td.value = Number(d1.value) + Number(d2.value) +  Number(d3.value)
})
f3.addEventListener('focusout', () => {
    tfx.value = Number(f1.value) + Number(f2.value) + Number(f3.value)
})
d4.addEventListener('focusout', () => {
    td.value = Number(d1.value) + Number(d2.value) +  Number(d3.value) + Number(d4.value)
})
f4.addEventListener('focusout', () => {
    tfx.value = Number(f1.value) + Number(f2.value) + Number(f3.value) + Number(f4.value)
})
td.addEventListener('focusout', () => {
    td.value = Number(d1.value) + Number(d2.value) + Number(d3.value) + Number(d4.value)
    tfx.value = Number(f1.value) + Number(f2.value) + Number(f3.value) + Number(f4.value)
})

tfx.addEventListener('focusout', () => {
    td.value = Number(d1.value) + Number(d2.value) + Number(d3.value) + Number(d4.value)
    tfx.value = Number(f1.value) + Number(f2.value) + Number(f3.value) + Number(f4.value)
})

// Source: https://stackoverflow.com/questions/40739059/add-working-days-to-a-date-using-javascript
function addWorkDays(startDate, days) {
    if(isNaN(days)) {
        console.log("Value provided for \"days\" was not a number");
        return
    }
    if(!(startDate instanceof Date)) {
        console.log("Value provided for \"startDate\" was not a Date object");
        return
    }
    // Get the day of the week as a number (0 = Sunday, 1 = Monday, .... 6 = Saturday)
    let dow = startDate.getDay();
    let daysToAdd = parseInt(days);
    // If the current day is Sunday add one day
    if (dow === 0)
        daysToAdd++;
    // If the start date plus the additional days falls on or after the closest Saturday calculate weekends
    if (dow + daysToAdd >= 6) {
        //Subtract days in current working week from work days
        let remainingWorkDays = daysToAdd - (5 - dow);
        //Add current working week's weekend
        daysToAdd += 2;
        if (remainingWorkDays > 5) {
            //Add two days for each working week by calculating how many weeks are included
            daysToAdd += 2 * Math.floor(remainingWorkDays / 5);
            //Exclude final weekend if remainingWorkDays resolves to an exact number of weeks
            if (remainingWorkDays % 5 === 0){
                daysToAdd -= 2;
            }
        }
    }
    startDate.setDate(startDate.getDate() + daysToAdd);
    // Converting the date object to date string format so that form can accept the value
    return startDate.toISOString().split('T')[0];
}
tfx.addEventListener('focusout', () => {
    let impdate = document.getElementById('id_impdate');
    let newdate = new Date(impdate.value)
    if (Number(tfx.value) === 1){
        document.getElementById('id_tentativecompletiondate').value = document.getElementById('id_impdate').value
    }else{
        let check_date = addWorkDays(newdate,Number(tfx.value-1))
        document.getElementById('id_tentativecompletiondate').value = check_date
    }
})

document.body.addEventListener('click', () => {
    let impdate = document.getElementById('id_impdate');
    let newdate = new Date(impdate.value)
    if (Number(tfx.value) === 1){
        document.getElementById('id_tentativecompletiondate').value = document.getElementById('id_impdate').value
    }else{
        let check_date = addWorkDays(newdate,Number(tfx.value-1))
        document.getElementById('id_tentativecompletiondate').value = check_date
    }
});

//https://stackoverflow.com/questions/37069186/calculate-working-days-between-two-dates-in-javascript-excepts-holidays
let workingDaysBetweenDates = (d0, d1) => {
  /* Two working days and an sunday (not working day) */
  let holidays = ['2022-01-26', '2022-03-18', "2022-08-15", "2022-10-02", "2022-10-05", "2022-10-24", "2022-12-25"];
  let startDate = new Date(d0);
  let endDate = new Date(d1);
  console.log(d1)

// Validate input
  if (endDate <= startDate) {
    return 0;
  }

// Calculate days between dates
  let millisecondsPerDay = 86400 * 1000; // Day in milliseconds
  startDate.setHours(0, 0, 0, 1);  // Start just after midnight
  endDate.setHours(23, 59, 59, 999);  // End just before midnight
  let diff = endDate - startDate;  // Milliseconds between datetime objects
  let days = Math.ceil(diff / millisecondsPerDay);

  // Subtract two weekend days for every week in between
  let weeks = Math.floor(days / 7);
  days -= weeks * 2;

  // Handle special cases
  let startDay = startDate.getDay();
  let endDay = endDate.getDay();

  // Remove weekend not previously removed.
  if (startDay - endDay > 1) {
    days -= 2;
  }
  // Remove start day if span starts on Sunday but ends before Saturday
  if (startDay == 0 && endDay != 6) {
    days--;
  }
  // Remove end day if span ends on Saturday but starts after Sunday
  if (endDay == 6 && startDay != 0) {
    days--;
  }
  /* Here is the code */
  holidays.forEach(day => {
    if ((day >= d0) && (day <= d1)) {
      /* If it is not saturday (6) or sunday (0), substract it */
      if ((parseDate(day).getDay() % 6) != 0) {
        days--;
      }
    }
  });
  return days;
}

function parseDate(input) {
    // Transform date from text to date
  let parts = input.match(/(\d+)/g);
  // new Date(year, month [, date [, hours[, minutes[, seconds[, ms]]]]])
  return new Date(parts[0], parts[1]-1, parts[2]); // months are 0-based
}
