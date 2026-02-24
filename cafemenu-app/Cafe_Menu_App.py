import streamlit as st
import time  # <--- To handle the time delay

# --- CUSTOM CSS FOR THEME ---
st.markdown(
    """
    <style>
        /* 1. Progress Bar Color */
        div[data-baseweb="progress-bar"] > div > div {
            background-color: #FFBD45 !important;
        }

        /* 2. Button Hover Effect */
        div.stButton > button:hover {
            border-color: #FFBD45 !important;
            color: #FFBD45 !important;
            background-color: rgba(255, 189, 69, 0.1) !important;
        }

        /* 3. Primary Button (Checkout) specifically */
        div.stButton > button {
            border-radius: 8px;
            transition: all 0.3s ease;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --- Classes ---
class Tea:
    def __init__(self, name, price, img):
        self.name = name
        self.price = price
        self.img = img


class Order:
    def __init__(self):
        self.items = []

    def add_items(self, tea):
        self.items.append(tea)

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)

    def total(self):
        return sum(item.price for item in self.items)


# --- Menu Data ---
menu = [
    Tea("Tea", 10, "https://images.pexels.com/photos/5071493/pexels-photo-5071493.jpeg"),
    Tea("Masala Tea", 15, "https://images.pexels.com/photos/9228428/pexels-photo-9228428.jpeg"),
    Tea("Ginger Tea", 12, "https://images.pexels.com/photos/33489605/pexels-photo-33489605.jpeg"),
    Tea("Lemon Tea", 15, "https://images.pexels.com/photos/28944482/pexels-photo-28944482.jpeg"),
    Tea("Black Tea", 8, "https://images.pexels.com/photos/15661867/pexels-photo-15661867.jpeg"),
    Tea("Green Tea", 20, "https://images.pexels.com/photos/34694990/pexels-photo-34694990.jpeg"),
    Tea("Biscuits", 5, "https://images.pexels.com/photos/5599487/pexels-photo-5599487.jpeg")
]

# --- App Logic ---

# Initialize order in session state
if "order" not in st.session_state:
    st.session_state.order = Order()

st.title("My Cafe Menu ☕")

# Display Menu
for i, tea in enumerate(menu):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(tea.img, width=200)
        st.write(f"**{tea.name}** — ₹{tea.price}")
    with col2:
        if st.button("Add", key=f"add_{i}"):
            st.session_state.order.add_items(tea)
            st.rerun()

st.divider()
st.subheader("Cart 🛒")

# Display Cart
if not st.session_state.order.items:
    st.info("Cart is empty.")
else:
    for i, item in enumerate(st.session_state.order.items):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{item.name} — ₹{item.price}")
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.order.remove_item(i)
                st.rerun()

    st.write("---")
    st.write(f"### Total: ₹{st.session_state.order.total()}")

    # --- FIXED CHECKOUT LOGIC ---
    if st.button("Checkout"):
        # Finalizing phase (3 seconds)
        progress_text = "Finalizing your order..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.03)
            my_bar.progress(percent_complete + 1, text=progress_text)

        my_bar.empty()
        st.success("Order placed 🤗")
        st.balloons()

        st.session_state.order.items.clear()

        # Balloon travel phase
        time.sleep(5)
        st.rerun()