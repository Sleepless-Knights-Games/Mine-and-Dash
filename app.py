import streamlit as st
from game_logic import Game
from PIL import Image

st.set_page_config(page_title="Mine and Dash", layout="wide")
st.title("Mine and Dash")

if "game" not in st.session_state:
    st.session_state.game = Game(num_players=2)

game = st.session_state.game

# Show current hand
st.subheader(f"Round {game.round} - Turn {game.turn}")
player_hand = game.get_current_hand()

cols = st.columns(len(player_hand))
selected_card = None
for i, card in enumerate(player_hand):
    if cols[i].button(f"Play: {card}", key=f"play_{i}_{card}_{game.turn}"):
        selected_card = card

if selected_card:
    game.play_card(selected_card)

# Show cave-in deck state
st.markdown("### Cave-In Deck")
st.write(f"Cave-in streak: {game.cave_in_streak}")
st.write(f"Cave-in cards shown: {game.cave_in_cards_revealed}")

if game.round_over:
    st.success("Round over due to cave-in!")
    if st.button("Start Next Round"):
        game.next_round()

if game.is_game_over():
    st.success("Game Over!")
    scores = game.get_final_scores()
    st.write("Final Scores:", scores)
    st.button("Restart Game", on_click=lambda: st.session_state.pop("game"))
