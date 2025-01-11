import streamlit as st
import math

# Initialize session state for the expression
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Callback function to clear input
def clear_input():
    st.session_state.expression = ""  # Reset session state

# Title
st.title("Scientific Calculator")

# Input Section
st.subheader("Enter your mathematical expression:")
expression = st.text_input(
    "Expression",
    value=st.session_state.expression,
    placeholder="e.g., sin(30) + log(10)",
    key="expression",
)

# Math Context
MATH_CONTEXT = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,  # Base-10 logarithm
    "ln": math.log,     # Natural logarithm
    "sqrt": math.sqrt,
    "pow": math.pow,
    "pi": math.pi,
    "e": math.e,
    "factorial": math.factorial,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
}

# Helper function for evaluating math expressions
def evaluate_expression(expr):
    try:
        # Safe evaluation of expressions
        result = eval(expr, {"__builtins__": None}, MATH_CONTEXT)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Buttons
if st.button("Evaluate"):
    result = evaluate_expression(expression)
    st.markdown(f"### Result: `{result}`")

# Clear Button
st.button("Clear", on_click=clear_input)

# Advanced Features
with st.expander("Supported Functions"):
    st.markdown("""
    - **Basic Operators**: `+`, `-`, `*`, `/`
    - **Trigonometric Functions**: `sin(x)`, `cos(x)`, `tan(x)` (input in radians)
    - **Logarithmic Functions**: `log(x)` (base 10), `ln(x)` (natural log)
    - **Square Root**: `sqrt(x)`
    - **Exponentiation**: `pow(x, y)` or `x**y`
    - **Factorial**: `factorial(x)`
    - **Hyperbolic Functions**: `sinh(x)`, `cosh(x)`, `tanh(x)`
    - **Constants**: `pi`, `e`
    """)
