import streamlit as st
from game_logic import Game

st.set_page_config(page_title="Mine and Dash", layout="wide")
st.title("Mine and Dash")

if "game" not in st.session_state:
    st.session_state.game = Game(num_players=2)

game = st.session_state.game
st.subheader(f"Round {game.round} - Turn {game.turn}")

player_hand = game.get_current_hand()
cols = st.columns(len(player_hand))
selected_card_id = None

for i, card in enumerate(player_hand):
    label = f"{card['name']}"
    if cols[i].button(label, key=f"card_{card['id']}"):
        selected_card_id = card["id"]

if selected_card_id:
    game.play_card(selected_card_id)

st.markdown("### Cave-In Deck")
st.write(f"Cave-in streak: {game.cave_in_streak}")
st.write(f"Cards revealed: {game.cave_in_cards_revealed}")

if game.round_over:
    st.success("Round ended due to cave-in!")
    if st.button("Start next round"):
        game.next_round()

if game.is_game_over():
    st.success("Game Over!")
    st.write("Final Scores:", game.get_final_scores())
    if st.button("Restart Game"):
        del st.session_state["game"]
