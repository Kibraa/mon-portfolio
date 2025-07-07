const list = document.querySelectorAll('#navMenu li');
let tl = gsap.timeline();
gsap.registerPlugin(ScrollTrigger);

gsap.registerPlugin(Draggable);
const div = document.querySelector("#li");
const largeur = div.offsetWidth;
const burger = document.getElementById('burger');
const burgerMenu = document.getElementById('mainMenu');
const navMenu = document.getElementById('navMenu');
const nav = document.getElementById('nav');
const languageBtn = document.getElementById('languageBtn');
const languageMenu = document.getElementById('languageMenu');
const languageFr = document.getElementById('languageFr');
const languageEn = document.getElementById('languageFr');
const backgroundBlur = document.getElementById('backgroundBlur');
const stylo = window.getComputedStyle(div);
const padding = parseFloat(stylo.paddingLeft)/2;
const noPadding = largeur - padding ;

const firstQuestion = document.getElementById('firstQuestion');
const secondQuestion = document.getElementById('secondQuestion');
const thirdQuestion = document.getElementById('thirdQuestion');
const conversation = document.getElementById('conversation');

const fiveWhysText = "J'utilise la technique des 5 Whys pour identifier et comprendre les causes profondes des problèmes. Cette méthode consiste à poser la question 'Pourquoi ?' de manière répétée (généralement cinq fois) pour aller au-delà des symptômes superficiels et découvrir l'origine réelle de l'obstacle. Grâce à cette approche, je peux m'assurer que les solutions envisagées s'attaquent aux racines du problème, réduisant ainsi le risque de récurrence.";
const Skills = "Je suis une personne communicative, dotée d'un bon esprit d'équipe, et j’aime prendre des initiatives tout en restant autonome. Curieux et polyvalent, je m’adapte rapidement aux situations et je reste réactif face aux défis."
const fiveYears ="Dans cinq ans, je me vois en tant que développeur fullstack au sein d’une grande entreprise innovante, qui partage mes principes et mes valeurs. Mon objectif sera de contribuer au développement d’applications web et mobiles de pointe, ainsi qu’à la création de solutions sur mesure, tout en collaborant avec des équipes dynamiques pour accompagner l’entreprise dans la réalisation de ses projets numériques.";

languageBtn.addEventListener('click', () => {
    languageMenu.classList.toggle('hidden');
    languageMenu.classList.toggle('flex');
});

burger.addEventListener('click', () =>{
    burgerMenu.classList.toggle('hidden');
    burgerMenu.classList.toggle('flex');
    backgroundBlur.classList.toggle('hidden');
});

document.getElementById('closeMenu').addEventListener('click', () =>{
    burgerMenu.classList.toggle('hidden');
    backgroundBlur.classList.toggle('hidden');
})

function afficherHeure() {
    const now = new Date();
    const heures = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const heureActuelle = `${heures}:${minutes}`;
    document.getElementById("hour").textContent = heureActuelle;
}
afficherHeure();
setInterval(afficherHeure, 20000);

function addToConversation(questionText, question) {
    const blueDiv = document.createElement('div');
    blueDiv.classList.add('ml-10', 'flex', 'flex-col','self-end','slide-down');

    const imgBlue = document.createElement('img');
    imgBlue.classList.add('relative', 'size-7', 'self-end', '-mt-7', '-mr-2','scale-x-[-1]');
    imgBlue.setAttribute('src', '/assets/bubble_blue.svg');

    const newItem = document.createElement('li');
    newItem.classList.add('bg-blue-500', 'px-3', 'py-2', 'rounded-[20px]','z-10' ); 
    newItem.textContent = questionText;
    blueDiv.appendChild(newItem);
    blueDiv.appendChild(imgBlue);
    conversation.prepend(blueDiv);

    const img = document.createElement('img');
    img.classList.add('relative', 'size-7', 'left-0', '-mt-7', '-ml-[9px]');
    img.setAttribute('src', '/assets/bubble.svg');

    const greyDiv = document.createElement('div');
    greyDiv.classList.add('mr-10', 'flex', 'flex-col','slide-down'); 
    
    const greyItem = document.createElement('li');
    greyItem.classList.add('bg-zinc-800', 'rounded-[30px]', 'z-10', 'px-4', 'py-3', 'w-full', 'h-full');

    greyDiv.appendChild(greyItem);
    greyDiv.appendChild(img);

    
    setTimeout(() => {
        const vid = document.createElement('iframe');
        vid.setAttribute('src', 'https://lottie.host/embed/822b883a-6daf-4406-95f2-e1a948891620/uTdQiNRaLQ.json');
        vid.classList.add('m-1.5', 'h-2.5','w-10');
        greyItem.appendChild(vid);
        conversation.prepend(greyDiv);
    }, 1000);

    setTimeout(() => {
        greyItem.textContent = question;
    }, 2500);
}


firstQuestion.addEventListener('click', () => {addToConversation(firstQuestion.textContent, fiveWhysText); firstQuestion.remove();});
secondQuestion.addEventListener('click', () => {addToConversation(secondQuestion.textContent, Skills); secondQuestion.remove();});
thirdQuestion.addEventListener('click', () => {addToConversation(thirdQuestion.textContent,fiveYears ); thirdQuestion.remove();});

function checkAndAddMessage() {
    const questionList = document.getElementById('questions');
    setInterval(() => {
      if (questionList.children.length === 0) {
        const message = document.createElement('p');
        message.innerHTML = `D'autres questions ? <a class="text-blue-500 underline cursor-pointer" id="contact_me">Contactez moi !</a>`;
        message.classList.add('flex','grow','items-center','flex-row','justify-center','gap-x-2')
        questionList.appendChild(message);

        const contactLink = document.getElementById('contact_me');
        if (contactLink) {
          contactLink.addEventListener('click', function () {
            document.getElementById('contactPage').scrollIntoView({ behavior: 'smooth' });
          });
        }
      }
    }, 1000);
  }
checkAndAddMessage();

document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', 
    function(event) {
        event.preventDefault();
        const targetId = this.getAttribute('id');
        const targetElement = document.getElementById(`${targetId}Page`);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop,
                behavior: "smooth" 
            });
        }

        burgerMenu.classList.toggle('hidden');
        backgroundBlur.classList.toggle('hidden');
    });
});
document.getElementById('arobase').addEventListener('click', function() {
    document.getElementById('contactPage').scrollIntoView({ behavior: 'smooth' });
});

document.getElementById('arrow_b').addEventListener('click', function() {
    document.getElementById('aboutPage').scrollIntoView({ behavior: 'smooth' });
});
document.querySelectorAll('#nav a').forEach(link => {
    link.addEventListener('click', () => {
        burgerMenu.classList.toggle('hidden');
        backgroundBlur.classList.toggle('hidden');
    });
});

const navStat = document.getElementById('navStat');
const homePage = document.getElementById('homePage');
const aboutPage = document.getElementById('aboutPage');
const workPage = document.getElementById('workPage');
const contactPage = document.getElementById('contactPage');

let distance = 0
let lastLoggedValue = null;

function moveSpan() {
    const rect = homePage.getBoundingClientRect();
    const totalHeight = homePage.offsetHeight;
    distance = Math.ceil((rect.bottom / totalHeight) * 100);

    if (distance !== lastLoggedValue && distance <= 100 && distance >= 0) {
        lastLoggedValue = distance;
        const moveX = (1 - distance / 100) * noPadding;
        navStat.style.transform = `translateX(${moveX}px)`;
    }
}
window.addEventListener("scroll", moveSpan);



tl.from(nav, {
    y: "150px",
    duration: 0.5,
    ease: "back.out(4)"
})

tl.from(nav, {
    height: "56px",
    width: "56px",
    duration: 0.5,
},"-=.1");

tl.to(navStat, {
    width: noPadding,
    duration: 0.1,
    ease: "expo.out"
},"<")

tl.from(list, {
    y: -60,
    stagger: 0.1,
    duration: 0.5,
    ease: "back.out(2)",
},"-=.1")

function playSound() {
    const sound = document.getElementById("clickSound");
    sound.currentTime = 0;
    sound.play();
}

let cursor = document.getElementById('cursor');
document.addEventListener('DOMContentLoaded',function(){
    document.addEventListener('mousemove', function(e) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });
    
})

const draggableElement = document.getElementById("draggable");
const draggerElement = document.getElementById("dragger");
const submitButton = document.querySelector("button[type='submit']");

Draggable.create(draggableElement, {
    type: "x",
    bounds: draggerElement,
    onDrag: function() {
        const draggerWidth = draggableElement.parentElement.offsetWidth;
        const currentPosition = this.x;

        let percentage = Math.round(currentPosition / draggerWidth*10)/10;

        let r = 59 + (percentage * (9 - 59));
        let g = 130 + (percentage * (264 - 130));
        let b = 246 + (percentage * (- 304));
        
        draggableElement.style.backgroundColor = `rgba(${r}, ${g}, ${b}, 1)`;
        if (percentage === 0.5) {
            submitButton.click();
        }
    }
  });