document.addEventListener("DOMContentLoaded", function(){

    const calendarEl = document.getElementById("calendar")

    const calendar = new FullCalendar.Calendar(calendarEl, {

        initialView:"dayGridMonth",

        height:650,

        headerToolbar:{
            left:"prev,next today",
            center:"title",
            right:"dayGridMonth,timeGridWeek,timeGridDay"
        },

        events:{
            url:"/c/attendance-events/",
            method:"GET"
        },

        eventDisplay:"block"

    })

    calendar.render()

})