$(document).ready(function () {
    var crs_id = $('#cname').attr('data-course-id');
    var book_sec = $('#book-section');
    var book_sec_head = $('#book-sec-head');
    var book_title = $('#book-title');
    var book_text = $('#book-text');
    var book_link = $('#book-link');
    var book_read = $('#book-read');

    if (crs_id) {
        book_sec_head.html('Required Books for this Course');
        book_link.html('Download');
        book_read.html('Open & Read');
        book_link.addClass('btn btn-outline-secondary');
        book_read.addClass('btn btn-outline-secondary');
    }

    if (crs_id == 1) {
        book_title.html("Introduction to Computer Programming with Python");
        book_text.html("This book is required for the above mentioned course. At first you will learn python and its basics then we'll go forward and learn data sciences.");
        book_link.attr("href", "#");
        book_read.attr("href", "#");
    }
    else if (crs_id == 2) {
        book_title.html("Introduction to Computer Programming with C++");
        book_text.html("This book is required for the course you are enrolled in. It contains all data type, syntax, built-in function and much more with at least one example. It will help you a lot through out the course.");
        book_link.attr("href", "#");
        book_read.attr("href", "#");
    }
    else if (crs_id == 3) {
        book_title.html("MATLAB Programming");
        book_text.html("In this course you will learn mathematical computation using MATLAB. MATLAB is not a programming language but there are some function you can use to solve your problem. This book is preferred for this course");
        book_link.attr("href", "#");
        book_read.attr("href", "#");
    }
    else if (crs_id == 4) {
        book_title.html("Front-End Web Development");
        book_text.html("This course is completely designed for the beginners. In this course you will learn how to design a front-end website using HTML, CSS, JavaScript. For this course this book is highly recommended.");
        book_link.attr("href", "#");
        book_read.attr("href", "#");
    }
    else {
        book_sec_head.html('No Books Avaliable!');
        book_sec.html('<h3 class="text-muted">Please select a course first!</h3>');
    }
});

// Date according to months
function numOfDaysAccToMonth(days) {
    var newOpt = document.createElement('option');
    newOpt.value = days;
    newOpt.innerHTML = days;
    date.options.add(newOpt);
}

function selectDate(month) {
    var date = document.getElementById('date');
    if (month == 'Jan' || month == 'Mar' || month == 'May' || month == 'Jul' || month == 'Aug' || month == 'Oct' || month == 'Dec') {
        date.innerHTML = "";
        for (i = 1; i <= 31; i++) {
            numOfDaysAccToMonth(i);
        }
    }
    else if (month == 'Feb') {
        date.innerHTML = "";
        for (i = 1; i <= 28; i++) {
            numOfDaysAccToMonth(i);
        }
    }
    else {
        date.innerHTML = "";
        for (i = 1; i <= 30; i++) {
            numOfDaysAccToMonth(i);
        }
    }
}
