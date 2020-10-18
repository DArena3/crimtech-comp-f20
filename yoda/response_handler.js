// Declaring variables that you may want to use.
let names = ['cute', 'regular'];
let moods = ['dark', 'force', 'std'];

let dark_quotes = ["Once you start down the dark path, forever will it dominate your destiny, consume you it will.",
"In a dark place we find ourselves, and a little more knowledge lights our way.",
"Fear is the path to the dark side. Fear leads to anger. Anger leads to hate. Hate leads to suffering.",
"Always two there are, no more, no less. A master and an apprentice.",
"In the end, cowards are those who follow the dark side."];
let force_quotes = ["Luminous beings are we, not this crude matter.",
"A Jedi uses the Force for knowledge and defense, never for attack.",
"Clear your mind must be, if you are to find the villains behind this plot.",
"The force. Life creates it, makes it grow. Its energy surrounds us and binds us.",
"My ally is the Force, and a powerful ally it is."];
let std_quotes = ["Patience you must have, my young padawan.",
"When nine hundred years old you reach, look as good you will not.",
"No! Try not! Do or do not, there is no try.",
"Judge me by my size, do you?",
"Difficult to see. Always in motion is the future."
];

document.getElementById("text-input").addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        respond()
    }
});

function respond() {
    var text = document.getElementById("text-input").value

    var name = (text.includes(names[0]) || text.includes("baby")) ? 0:1

    if (text.includes(moods[0]) && text.includes(moods[1])) mood = 0
    else if (text.includes(moods[1])) mood = 1
    else mood = 2

    document.getElementById("yoda-pic").setAttribute("src", `img/${names[name]}-${moods[mood]}.jpg`)

    if (name == 1) {
        switch (mood) {
            case 0: document.getElementById("yoda-text").innerText = dark_quotes[Math.floor(Math.random() * dark_quotes.length)]
                break
            case 1: document.getElementById("yoda-text").innerText = force_quotes[Math.floor(Math.random() * force_quotes.length)]
                break
            default: document.getElementById("yoda-text").innerText = std_quotes[Math.floor(Math.random() * std_quotes.length)]
        }

        document.getElementById("yoda-text").innerText = document.getElementById("yoda-text").innerText + " Yes, h" + "m".repeat(Math.floor(Math.random() * 7) + 2) + "."
    }
    else document.getElementById("yoda-text").innerText = "Yes, h" + "m".repeat(Math.floor(Math.random() * 7) + 2) + "."

    document.getElementById("text-input").value = ""
}