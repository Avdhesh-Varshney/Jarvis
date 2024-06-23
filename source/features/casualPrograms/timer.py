import time

def timer():
    while True:
        try:
            user_input = input("Enter the time in hh:mm:ss format: ")
            h, m, s = map(int, user_input.split(':'))
            if h < 0 or m < 0 or s < 0:
                raise ValueError("Please enter non-negative integers.")
            countdown_time = h * 3600 + m * 60 + s
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

    print(f"Timer set for {h} hours, {m} minutes, and {s} seconds.")
    
    while countdown_time:
        mins, secs = divmod(countdown_time, 60)
        hours, mins = divmod(mins, 60)
        timer_format = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        print(timer_format, end='\r')
        time.sleep(1)
        countdown_time -= 1
    
    print("Time's up!")

if __name__ == "__main__":
    timer()
