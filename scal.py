import streamlit as st
import math

def scientific_calculator():
    # Initialize session state for the calculator
    if 'expression' not in st.session_state:
        st.session_state.expression = ''
    if 'display_expression' not in st.session_state:
        st.session_state.display_expression = ''
    if 'angle_mode' not in st.session_state:
        st.session_state.angle_mode = 'Degree'

    st.title("🔢 Scientific Calculator")

    # Display the current expression or result
    st.text_input("Display", value=st.session_state.display_expression, key='display', disabled=True)

    # Function to update the expression
    def add_to_expression(symbol, display_symbol=None):
        if symbol == 'pi' or symbol == 'e':
            if st.session_state.expression and (st.session_state.expression[-1].isdigit() or st.session_state.expression[-1] == ')'):
                st.session_state.expression += '*'
                st.session_state.display_expression += '×'
        elif symbol == '(':
            if st.session_state.expression and (st.session_state.expression[-1].isdigit() or st.session_state.expression[-1] == ')'):
                st.session_state.expression += '*'
                st.session_state.display_expression += '×'
        st.session_state.expression += str(symbol)
        st.session_state.display_expression += str(display_symbol if display_symbol is not None else symbol)

    # Function to clear the expression
    def clear_expression():
        st.session_state.expression = ''
        st.session_state.display_expression = ''

    # Function to delete the last character
    def delete_last():
        st.session_state.expression = st.session_state.expression[:-1]
        st.session_state.display_expression = st.session_state.display_expression[:-1]

    # Function to toggle angle mode
    def toggle_angle_mode():
        if st.session_state.angle_mode == 'Degree':
            st.session_state.angle_mode = 'Radian'
        else:
            st.session_state.angle_mode = 'Degree'

    # Custom trigonometric functions that check the mode
    def sin_calc(x):
        if st.session_state.angle_mode == 'Degree':
            return math.sin(math.radians(x))
        else:
            return math.sin(x)

    def cos_calc(x):
        if st.session_state.angle_mode == 'Degree':
            return math.cos(math.radians(x))
        else:
            return math.cos(x)

    def tan_calc(x):
        if st.session_state.angle_mode == 'Degree':
            return math.tan(math.radians(x))
        else:
            return math.tan(x)

    # Function to evaluate the expression
    def calculate_expression():
        try:
            safe_dict = {'sin': sin_calc, 'cos': cos_calc, 'tan': tan_calc, 'pi': math.pi, 'e': math.e}
            safe_dict.update(vars(math))
            result = eval(st.session_state.expression, {"__builtins__": None}, safe_dict)
            st.session_state.expression = str(result)
            st.session_state.display_expression = str(result)
        except Exception:
            st.session_state.expression = ''
            st.session_state.display_expression = 'Error'

    func_mappings = {
        'sin': ('sin(', 'sin('),
        'cos': ('cos(', 'cos('),
        'tan': ('tan(', 'tan('),
        '√': ('math.sqrt(', '√('),
        'log': ('math.log10(', 'log('),
        'ln': ('math.log(', 'ln('),
        'exp': ('math.exp(', 'exp('),
        '^': ('**', '^'),
        '×': ('*', '×'),
        '÷': ('/', '÷'),
        '+': ('+', '+'),
        '-': ('-', '-'),
        'π': ('pi', 'π'),
        'e': ('e', 'e'),
    }

    cols_mode = st.columns([1, 2])
    with cols_mode[0]:
        st.button('Mode', on_click=toggle_angle_mode)
    with cols_mode[1]:
        st.write(f"**Angle Mode:** {st.session_state.angle_mode}")

    buttons = [
        ['AC', 'DC', '(', ')'],
        ['7', '8', '9', '÷'],
        ['4', '5', '6', '×'],
        ['1', '2', '3', '-'],
        ['0', '.', '^', '+'],
        ['sin', 'cos', 'tan', 'π'],
        ['log', 'ln', 'exp', '='],
    ]

    button_counter = 0
    for row in buttons:
        cols = st.columns(4)
        for i, label in enumerate(row):
            if label:
                key = f"button_{button_counter}"
                button_counter += 1
                if label == 'AC':
                    cols[i].button(label, on_click=clear_expression, key=key)
                elif label == 'DC':
                    cols[i].button(label, on_click=delete_last, key=key)
                elif label == '=':
                    cols[i].button(label, on_click=calculate_expression, key=key)
                else:
                    symbol, display_symbol = func_mappings.get(label, (label, label))
                    cols[i].button(label, on_click=add_to_expression, args=(symbol, display_symbol), key=key)
