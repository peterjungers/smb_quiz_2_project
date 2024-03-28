/*
JavaScript for Super Mario Bros. quiz
Author: Peter Jungers
Date: January/February 2023
*/


// Two functions pertaining to images throughout site:


/*
Help with the image randomizing function from
https://www.peachpit.com/articles/article.aspx?p=2239154&seqNum=10
*/
function randomizeImages() {
    const imageDivs = document.querySelectorAll(".sprite");
    let images;
    // index.html has only two images that always appear:
    if (imageDivs.length === 2) {
        images = imageDivs;
    } else {  // For quiz.html (more info at showOrHideImages function):
        showOrHideImages(imageDivs);
        images = [
            document.querySelector("#header-sprite"),
            document.querySelector("#image-2"),
            document.querySelector("#image-5"),
            document.querySelector("#image-7")
        ];
    }

    /*
    Images in static/images directory are numbered beginning with 1.
    Amount of numbered images in directory is 12.
    */
    let randomNumberArray = []
    while (randomNumberArray.length < images.length) {
        let randomNumber = Math.floor((Math.random() * 12) + 1);
        /* No repeated numbers allowed in randomNumberArray
        so no images get repeated: */
        if (!randomNumberArray.includes(randomNumber)) {
            randomNumberArray.push(randomNumber);
        }
    }
    for (let i = 0; i < randomNumberArray.length; i++) {
        images[i].src = `/static/images/${randomNumberArray[i]}.png`;
    }
}


// For quiz page images only:
function showOrHideImages(images) {
    /*
    Because img divs are included programmatically for each quiz question,
    and page design-wise not all questions should be followed by an image,
    the following is necessary (note: div id "score-sprite" is not part of
    images array):
    */
    images.forEach(image => {
        if (image.id === "header-sprite"
            || image.id === "image-2"
            || image.id === "image-5"
            || image.id === "image-7") {
            image.style.display = "block";
        } else {
            image.style.display = "none";
        }
    });
}


// The remaining four functions are for handling of quiz questions and score:


function decodeAnswers() {
    const codedAnswers =
        JSON.parse(document.querySelector("#array").textContent);
    let correctAnswers = [];

    codedAnswers.forEach(answer => {
        let decodedAnswer = "";
        for (let i = 0; i < answer.length; i++) {
            let letter = String.fromCharCode(answer[i].charCodeAt(0) - 5);
            decodedAnswer += letter;
        }
        correctAnswers.push(decodedAnswer);
    });
    checkBtnAnswer(correctAnswers);
}


function checkBtnAnswer(correctAnswers) {
    const optionBtns = document.querySelectorAll(".option button");
    let counterCorrectAnswers = 0;
    let counterAllQuestions = 0;

    optionBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            for (let i = 0; i <= optionBtns.length; i ++) {
                // Match index number to actual btn number, hence i + 1
                if (btn.classList.contains(`btn-${i + 1}`)) {
                    let allOptions = btn.parentElement.parentElement.children;
                    let message = document.querySelector(`#message-${i + 1}`);

                    btn.style.backgroundColor = "#f1f1f1";
                    btn.style.color = "#292929";
                    if (btn.nextElementSibling.innerText
                            === correctAnswers[i]) {
                        for (let i = 0; i < allOptions.length; i++) {
                            if (allOptions[i] !== btn.parentElement) {
                                allOptions[i].style.opacity = .5;
                            }
                        }
                        message.style.opacity = 1;
                        message.innerText = "Correct!";
                        counterCorrectAnswers += 1;
                        counterAllQuestions += 1;
                    } else {
                        for (let i = 0; i < allOptions.length; i++) {
                            allOptions[i].style.opacity = .5;
                        }
                        message.innerText = "Sorry, incorrect.";
                        counterAllQuestions += 1;
                    }
                    /* Disable question options for click
                    or focus Enter keydown: */
                    for (let i = 0; i < allOptions.length; i++) {
                        // Each option button:
                        if (allOptions[i].children[0]) {
                            allOptions[i].children[0].style.pointerEvents
                                = "none";
                            allOptions[i].children[0].disabled = true;
                        }
                    }
                }
            }
            if (counterAllQuestions === correctAnswers.length) {
                const score = document.querySelector("#score-container");
                score.scrollIntoView({behavior: "smooth", block: "start"});
                showCalculating(counterCorrectAnswers, counterAllQuestions);
            }
        });
    });
}


function showCalculating(counterCorrectAnswers, counterAllQuestions) {
    const scoreSprite = document.querySelector("#score-sprite");
    const calculatingScore = document.querySelector("#calculating-score");
    const dotsSpan = document.querySelector("#dots");

    scoreSprite.style.display = "none";

    setTimeout(() => {
        calculatingScore.style.display = "block";
        const addDots = setInterval(() => {
            dotsSpan.innerText += " .";
            if (dotsSpan.innerText.length === 8) {  // 4 spaces, 4 dots
                clearInterval(addDots);
                showFinalScore(counterCorrectAnswers, counterAllQuestions);
            }
        }, 1000);
    }, 1000);
}


function showFinalScore(counterCorrectAnswers, counterAllQuestions) {
    // calculatingScore contains calculating score message:
    const calculatingScore = document.querySelector("#calculating-score");
    // scoreResults contains score-circle and score-message elements:
    const scoreResults = document.querySelector("#score-results");
    const scoreCircleText = document.querySelector("#score-circle p");
    const scoreMessage = document.querySelector("#score-message");

    calculatingScore.style.display = "none";
    scoreResults.style.display = "flex";
    scoreCircleText.innerText = `${counterCorrectAnswers}/${counterAllQuestions}`;

    if (counterCorrectAnswers / counterAllQuestions === 1) {
        scoreMessage.innerText = "Excellent!";
    } else if (counterCorrectAnswers / counterAllQuestions >= .8) {
        scoreMessage.innerText = "Great job!";
    } else if (counterCorrectAnswers / counterAllQuestions >= .6) {
        scoreMessage.innerText = "Pretty good!";
    } else {
        scoreMessage.innerText = "You'll do better next time!";
    }
}


// Images sitewide:
window.addEventListener("DOMContentLoaded", randomizeImages);

// Quiz page questions and scoring:
if (document.querySelector("#array")) {
    window.addEventListener("DOMContentLoaded", decodeAnswers);
}
