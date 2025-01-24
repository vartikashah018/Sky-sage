import streamlit as st
from interface.inference import get_answer
from interface.get_answer_horoscope import get_answer_horoscope
import sys
import os
import random
import streamlit.components.v1 as components

sys.path.insert(1, os.getcwd())

# App title
st.set_page_config(page_title="🔮💬Astrology Bot: AI Clairvoyant")


st.title('🔮💬Astrology Bot: AI Clairvoyant')
st.caption("🚀 A streamlit chatbot powered by Llama-2-7b")


menu = ["Home", "Horoscope","Tarot"]

choice = st.sidebar.selectbox("Menu", menu)
if choice == "Home":
    st.subheader("Home")
    st.write("This is the home page.")
    st.write("You can choose horoscope or tarot on the LFS.")
elif choice == "Horoscope":
    st.image('https://github.com/nogibjj/astrology-bot/raw/main/images/astrology-horoscope-circle.jpg.webp', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":  "AI Clairvoyant", "content": "Greetings, dear seeker. I am Estelle, the clairvoyant, and your cosmic guide. What do they call you and what is your question? For example: What is the work horoscope for Aquiarius today?"}]
        
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt_horoscope := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt_horoscope})
        st.chat_message("user").write(prompt_horoscope)
        answer_horoscope = get_answer_horoscope(question = prompt_horoscope)
        msg_horoscope = answer_horoscope
        st.session_state.messages.append({"role":  "AI Clairvoyant", "content": msg_horoscope})
        st.chat_message("AI Clairvoyant").write(msg_horoscope)

elif choice == "Tarot":
    
    # st.image('images/tarot.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":  "AI Clairvoyant", "content": "Greetings, dear seeker. I am Estelle, the clairvoyant, and your cosmic guide. What do they call you and what is your question? Please select 3-5 cards below and tell me the question you want to ask. For example, Crystal, 25 year-old, single, who just left a company. She wanted to ask a question what she should do for her next job?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


    content = """<head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Tarot Reading</title>
                    <style>
                    .container {
                        text-align: center;
                        margin-top: 50px;
                        }

                        .cards-container {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: center;
                        }

                        .card {
                        position: relative;
                        width: 100px;
                        height: 150px;
                        margin: 5px;
                        cursor: pointer;
                        perspective: 1000px; /* Enable 3D effects */
                        }

                        .card img {
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        backface-visibility: hidden;
                        transition: transform 0.5s;
                        }

                        .card .back {
                        z-index: 1; /* Ensure the back image is above the front image */
                        }

                        .card .front {
                        z-index: 2; /* Ensure the front image is above the back image */
                        transform: rotateY(180deg); /* Initially rotated to hide the front image */
                        }

                        .card .reversed-front {
                        z-index: 2; /* Ensure the reversed front image is above the back image */
                        transform: rotateY(0deg); /* Initially rotated to hide the reversed front image */
                        }

                        .card.flipped .front {
                        transform: rotateY(0deg); /* Rotate the front image to reveal it when flipped */
                        }

                        .card.flipped .reversed-front {
                        transform: rotateY(180deg); /* Rotate the reversed front image to reveal it when flipped */
                        }

                </style>
                </head>
                <body>
                <div class="container">
                    <h1>Tarot Reading</h1>
                    <div class="cards-container" id="cardsContainer">
                    <!-- Card elements will be added here dynamically -->
                    </div>
                    <button id="sendButton">Send Cards</button>
                </div>

                <script>
                // Sample card data
                const cards = [
                'fool', 'magician', 'high priestess', 'empress', 'emperor', 'hierophant', 'lovers', 
                'chariot', 'strength', 'hermit', 'wheel of fortune', 'justice', 'hanged-man', 'death',
                'temperance', 'devil', 'tower', 'star', 'moon', 'sun', 'judgement', 'world',
                'ace-of-cups', 'two-of-cups', 'three-of-cups', 'four-of-cups', 'five-of-cups',
                'six-of-cups', 'seven-of-cups', 'eight-of-cups', 'nine-of-cups', 'ten-of-cups',
                'page-of-cups', 'knight-of-cups', 'queen-of-cups', 'king-of-cups',
                'ace-of-pentacles', 'two-of-pentacles', 'three-of-pentacles', 'four-of-pentacles',
                'five-of-pentacles', 'six-of-pentacles', 'seven-of-pentacles', 'eight-of-pentacles',
                'nine-of-pentacles', 'ten-of-pentacles', 'page-of-pentacles', 'knight-of-pentacles',
                'queen-of-pentacles', 'king-of-pentacles',
                'ace-of-swords', 'two-of-swords', 'three-of-swords', 'four-of-swords', 'five-of-swords',
                'six-of-swords', 'seven-of-swords', 'eight-of-swords', 'nine-of-swords', 'ten-of-swords',
                'page-of-swords', 'knight-of-swords', 'queen-of-swords', 'king-of-swords',
                'ace-of-wands', 'two-of-wands', 'three-of-wands', 'four-of-wands', 'five-of-wands',
                'six-of-wands', 'seven-of-wands', 'eight-of-wands', 'nine-of-wands', 'ten-of-wands',
                'page-of-wands', 'knight-of-wands', 'queen-of-wands', 'king-of-wands'
                ];

                // Function to shuffle the cards list
                function shuffleCards() {
                for (let i = cards.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [cards[i], cards[j]] = [cards[j], cards[i]];
                }
                }

                // Function to generate card elements
                function generateCards() {
                const container = document.getElementById("cardsContainer");
                shuffleCards();
                for (let i = 0; i < 78; i++) {
                    const card = cards[i];
                    const cardElement = document.createElement("div");
                    cardElement.classList.add("card");
                    cardElement.dataset.cardName = card;
                    
                    // Generate a random number to determine whether to use regular or reversed image
                    const randomNumber = Math.random();
                    let imgSrc;
                    if (randomNumber < 0.5) {
                        imgSrc = 'https://github.com/nogibjj/astrology-bot/blob/main/data/tarot_img/'+card+'.jpg?raw=true';
                    } else {
                        imgSrc = 'https://github.com/nogibjj/astrology-bot/blob/main/data/tarot_img/reversed_'+card+'.jpg?raw=true';
                    }
                    
                    cardElement.innerHTML = `
                    <img class="back" src="https://github.com/nogibjj/astrology-bot/blob/main/data/tarot_img/card_back.jpg?raw=true">
                    <img class="front" src="${imgSrc}">
                    `;
                    cardElement.addEventListener("click", () => toggleCard(cardElement));
                    container.appendChild(cardElement);
                }
                }

                // Function to toggle card visibility and orientation
                function toggleCard(cardElement) {
                cardElement.classList.toggle("flipped");
                }

                // Generate initial set of cards
                generateCards();


                document.getElementById('sendButton').addEventListener('click', function() {
                    // Retrieve all cards with class "card flipped"
                    var flippedCards = document.querySelectorAll('.card.flipped');
                    
                    // Extract content after src="tarot_img/ and before .jpg" from each flipped card
                    var cardNames = Array.from(flippedCards).map(function(card) {
                        var src = card.querySelector('.front').getAttribute('src');
                        var fileName = src.match(/tarot_img\/(.*?)\.jpg/)[1];
                        return fileName;
                    });

                    // Send the card names to the API
                    sendDataToAPI(cardNames);
                });

                function sendDataToAPI(data) {
                    var jsonData = JSON.stringify(data);
                    console.log(jsonData);
                    return jsonData;
                }
                </script>
                </body>
        """
    
    components.html(content, height=2500)

    all_cards = ['fool', 'magician', 'high priestess', 'empress', 'emperor', 'hierophant', 'lovers', 
                'chariot', 'strength', 'hermit', 'wheel of fortune', 'justice', 'hanged-man', 'death',
                'temperance', 'devil', 'tower', 'star', 'moon', 'sun', 'judgement', 'world',
                'ace-of-pentacles', 'two-of-pentacles', 'three-of-pentacles', 'four-of-pentacles',
                                        'five-of-pentacles', 'six-of-pentacles', 'seven-of-pentacles', 'eight-of-pentacles',
                                        'nine-of-pentacles', 'ten-of-pentacles', 'page-of-pentacles', 'knight-of-pentacles',
                                        'queen-of-pentacles', 'king-of-pentacles',
            'ace-of-swords', 'two-of-swords', 'three-of-swords', 'four-of-swords', 'five-of-swords',
                                    'six-of-swords', 'seven-of-swords', 'eight-of-swords', 'nine-of-swords', 'ten-of-swords',
                                    'page-of-swords', 'knight-of-swords', 'queen-of-swords', 'king-of-swords',
            'ace-of-wands', 'two-of-wands', 'three-of-wands', 'four-of-wands', 'five-of-wands',
                                'six-of-wands', 'seven-of-wands', 'eight-of-wands', 'nine-of-wands', 'ten-of-wands',
                                'page-of-wands', 'knight-of-wands', 'queen-of-wands', 'king-of-wands',
            'ace-of-cups', 'two-of-cups', 'three-of-cups', 'four-of-cups', 'five-of-cups',
                                'six-of-cups', 'seven-of-cups', 'eight-of-cups', 'nine-of-cups', 'ten-of-cups',
                                'page-of-cups', 'knight-of-cups', 'queen-of-cups', 'king-of-cups']
    
    all_cards = [c+'_'+'upright' for c in all_cards] + [c+'_'+'reversed' for c in all_cards]
    cards_final = st.multiselect("Tell me the cards you have drawn with corresponding positions", all_cards, placeholder="Type in the card you just draw or select", key="cards")

    if prompt_tarot := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt_tarot})
        st.chat_message("user").write(prompt_tarot)
        answer, context = get_answer(question = prompt_tarot, cards = cards_final)
        msg1 = answer[0].split('\",')[0].strip('\"')
        st.session_state.messages.append({"role":  "AI Clairvoyant", "content": msg1})
        st.chat_message("AI Clairvoyant").write(msg1)
        msg2 = f"I generated the response based on the following context from Tarot.com: {context}"
        st.session_state.messages.append({"role":  "AI Clairvoyant", "content": msg2})
        st.chat_message("AI Clairvoyant").write(msg2)
