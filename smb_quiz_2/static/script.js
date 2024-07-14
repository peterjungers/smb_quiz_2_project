/*
JavaScript for 8-Bit Super Mario Bros. Quiz
Author: Peter Jungers
Date: January/February 2023 (v.1); Spring/Summer 2024 (v.2)
*/



// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
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


/*
(The following function is for quiz page images only.)
Because img divs are included programmatically for each quiz question,
and page design-wise not all questions should be followed by an image,
the following is necessary:
*/
function showOrHideImages(images) {
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



// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Three functions for showing correct level and quiz button:


function determineLevel(levelID) {
    const levelIDs = document.querySelectorAll(".level-id");
    const question = document.querySelectorAll(".question");
    const scoreNeeded = document.querySelector("#score-counter-bottom-needed")

    // Shows or hides questions with levelID:
    for (let i = 0; i < levelIDs.length; i++) {
        if (levelIDs[i].innerText === levelID) {
            question[i].style.display = "block";
        }
        else {
            question[i].style.display = "none"
        }
    }
    // Sets next levelID:
    if (levelID === "1") {
        setNextLevelBtn("2");
        scoreNeeded.innerText = "3500";
    }
    else if (levelID === "2") {
        setNextLevelBtn("3");
        scoreNeeded.innerText = "20000";
    }
    else if (levelID === "3") {
        scoreNeeded.innerText = "60000";
    }
}


function setNextLevelBtn(level) {
    /*
    This function can only be invoked when user has met criteria to advance to
    next level (the "level" value will then be used to show and hide
    appropriate buttons).
    */

    const resetQuizBtn = document.querySelector("#reset-quiz-btn");
    const nextLevelBtn = document.querySelector("#next-level-btn");
    const message = document.querySelector("#message");

    nextLevelBtn.addEventListener("click", () => {
        resetQuizBtn.style.display = "block";
        nextLevelBtn.style.display = "none";
        message.innerText = "";
        determineLevel(level);
    });
}


function determineQuizOutcome(levelScore) {
    const message = document.querySelector("#message");
    const resetQuizBtn = document.querySelector("#reset-quiz-btn");
    const nextLevelBtn = document.querySelector("#next-level-btn");
    let level = levelScore[0];
    let score = levelScore[1];

    if (level === "1" && score >= 3500) {
        message.innerText = "Congratulations!";
        resetQuizBtn.style.display = "none";
        nextLevelBtn.style.display = "block";
    }
    else if (level === "2" && score >= 20000) {
        message.innerText = "Congratulations!";
        resetQuizBtn.style.display = "none";
        nextLevelBtn.style.display = "block";
    }
    else if (level === "3" && score >= 60000) {
        message.innerText = "You beat the game!";
        resetQuizBtn.innerText = "Home";
        resetQuizBtn.href = "index";
    }
    // Level not passed:
    else {
        message.innerText = "Sorry, try again.";
    }
}


// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// The remaining three functions are for handling of quiz questions and score:


function decodeAnswers() {
    const codedAnswers = array;
    let correctAnswers = [];

    codedAnswers.forEach(answer => {
        let decodedAnswer = "";
        let key = "";
        let codedAnswer = "";

        key = parseInt(answer.substring(0, 200).slice(-2));
        codedAnswer = answer.substring(0, 198).slice(-key);

        for (let i = 0; i < codedAnswer.length; i++) {
            let letter = String.fromCharCode(codedAnswer[i].charCodeAt(0) - 5);
            decodedAnswer += letter;
        }
        correctAnswers.push(decodedAnswer);
    });
    checkBtnAnswer(correctAnswers);
}


function checkBtnAnswer(correctAnswers) {
    const optionBtns = document.querySelectorAll(".option button");
    const levelIDs = document.querySelectorAll(".level-id");
    let counterCorrectAnswers = 0;
    let counterAllQuestions = 0;
    let totalScore;

    optionBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            for (let i = 0; i <= optionBtns.length; i ++) {
                // Match index number to actual btn number, hence i + 1
                if (btn.classList.contains(`btn-${i + 1}`)) {
                    let allOptions = btn.parentElement.parentElement.children;
                    let message = document.querySelector(`#message-${i + 1}`);

                    btn.classList.add("btn-circle-fill");
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
                        totalScore = increaseScore(levelIDs[i]);
                    } else {
                        for (let i = 0; i < allOptions.length; i++) {
                            allOptions[i].style.opacity = .5;
                        }
                        message.innerText = "Sorry, incorrect.";
                        counterAllQuestions += 1;
                    }
                    // Disable question options for click or
                    // focus Enter keydown:
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

            // Check to see if all visible questions have been answered:
            let visibleQuestions = 0;
            let level;
            for (let i = 0; i < levelIDs.length; i++) {
                // "display" property is set on "question" class div
                if (levelIDs[i].parentElement.style.display === "block") {
                    visibleQuestions += 1;
                    level = levelIDs[i].innerText; // Same for all
                    // visible levelIDs
                }
            }
            let levelScore = [level, totalScore];
            if (counterAllQuestions === visibleQuestions) {
                determineQuizOutcome(levelScore);
                // Reset counter for next levelID:
                counterAllQuestions = 0;
            }
        });
    });
}


function increaseScore(levelID) {
    const scoreCounterTop = document.querySelector("#score-counter-top");
    const scoreCounterBottom = document.querySelector("#score-counter-bottom");
    let score = parseInt(document.querySelector("#score-counter-top").innerText);
    let totalScore;

    if (levelID.innerText === "1") {
        score += 500;
    } else if (levelID.innerText === "2") {
        score += 1000;
    } else if (levelID.innerText === "3") {
        score += 5000;
    }

    scoreCounterTop.innerText = score.toString().padStart(6, "0");
    scoreCounterBottom.innerText = score;

    totalScore = score;
    return totalScore;
}


// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// On page loads:


// Images sitewide:
window.addEventListener("DOMContentLoaded", randomizeImages);

// Quiz page questions and scoring:
if (document.getElementById("array")) {
    window.addEventListener("DOMContentLoaded", () => {
        determineLevel("1");
    });
    window.addEventListener("DOMContentLoaded", decodeAnswers);
}
