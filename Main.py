import streamlit as st
import pandas as pd
import altair as alt

st.title('Beacon Chain Penalty and Slashing Simulation')
st.write("""
This app simulates the penalties and slashing conditions on the Ethereum beacon chain following the Altair upgrade.
Users can adjust parameters to see how various actions affect validator rewards and penalties.
""")

with st.sidebar:
    st.header('Simulation Parameters')
    active_validators = st.number_input('Number of Active Validators', min_value=1000, value=10000, step=1000)
    effective_balance = st.number_input('Effective Balance (ETH)', min_value=16.0, value=32.0, step=1.0)
    participation_rate = st.slider('Participation Rate', min_value=0.0, max_value=1.0, value=0.95, step=0.01)
    inactivity_leaks = st.selectbox('Inactivity Leaks', options=['Yes', 'No'])
    slashing = st.selectbox('Slashing Event', options=['Yes', 'No'])

    st.header('Factor Configuration')
    base_reward_factor = st.number_input('Base Reward Factor', value=64, step=1)
    proposer_reward_factor = st.number_input('Proposer Reward Factor', value=8, step=1)
    inactivity_penalty_factor = st.number_input('Inactivity Penalty Factor', value=32, step=1) # BASE_REWARD_FACTOR // 2
    slashing_penalty_factor = st.number_input('Slashing Penalty Factor', value=2, step=1)

def simulate_rewards_and_penalties(active_validators, effective_balance, participation_rate, inactivity_leaks, slashing,
                                   base_reward_factor, proposer_reward_factor, inactivity_penalty_factor, slashing_penalty_factor):
    base_reward = effective_balance * base_reward_factor / 100  # Simplified base reward calculation
    proposer_reward = base_reward * proposer_reward_factor / 100
    inactivity_penalty = 0
    slashing_penalty = 0

    if inactivity_leaks == 'Yes':
        inactivity_penalty = base_reward * inactivity_penalty_factor
    if slashing == 'Yes':
        slashing_penalty = effective_balance * slashing_penalty_factor
    
    adjusted_base_reward = base_reward * participation_rate
    
    return adjusted_base_reward, proposer_reward, inactivity_penalty, slashing_penalty

adjusted_base_reward, proposer_reward, inactivity_penalty, slashing_penalty = simulate_rewards_and_penalties(
    active_validators, effective_balance, participation_rate, inactivity_leaks, slashing,
    base_reward_factor, proposer_reward_factor, inactivity_penalty_factor, slashing_penalty_factor)

st.subheader('Simulation Results')
st.write(f"Adjusted Base Reward (Considering Participation Rate): {adjusted_base_reward:.2f} ETH")
st.write(f"Proposer Reward: {proposer_reward:.2f} ETH")
st.write(f"Inactivity Penalty: {inactivity_penalty:.2f} ETH")
st.write(f"Slashing Penalty: {slashing_penalty:.2f} ETH")


results = pd.DataFrame({
    'Parameter': ['Adjusted Base Reward', 'Proposer Reward', 'Inactivity Penalty', 'Slashing Penalty'],
    'Value': [adjusted_base_reward, proposer_reward, inactivity_penalty, slashing_penalty]
})

c = alt.Chart(results).mark_bar().encode(
    x='Parameter',
    y='Value',
    color=alt.condition(
        alt.datum.Parameter == 'Adjusted Base Reward',
        alt.value('blue'),  # If condition is true
        alt.value('red')  # If condition is false
    )
)

st.altair_chart(c, use_container_width=True)

# Conclusion and Further Information
st.write("""
For more detailed information on the Ethereum beacon chain and the Altair upgrade,
visit the [official Ethereum documentation](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/).
""")
