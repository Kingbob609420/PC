import turtle

# Set up the screen
win = turtle.Screen()
win.title("Pong")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=6, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=6, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(1)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.2
ball.dy = 0.2

# Score
score_a = 0
score_b = 0

# Score display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Function to update score display
def update_score():
    score_display.clear()
    score_display.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

# Paddle speed
paddle_speed = 5

# Smooth movement
paddle_a_dy = 0
paddle_b_dy = 0

# Function to set paddle A's vertical movement
def paddle_a_up_press():
    global paddle_a_dy
    paddle_a_dy = paddle_speed

def paddle_a_down_press():
    global paddle_a_dy
    paddle_a_dy = -paddle_speed

def paddle_a_release():
    global paddle_a_dy
    paddle_a_dy = 0

# Function to set paddle B's vertical movement
def paddle_b_up_press():
    global paddle_b_dy
    paddle_b_dy = paddle_speed

def paddle_b_down_press():
    global paddle_b_dy
    paddle_b_dy = -paddle_speed

def paddle_b_release():
    global paddle_b_dy
    paddle_b_dy = 0

# Keyboard bindings
win.listen()
win.onkeypress(paddle_a_up_press, "w")
win.onkeypress(paddle_a_down_press, "s")
win.onkeyrelease(paddle_a_release, "w")
win.onkeyrelease(paddle_a_release, "s")
win.onkeypress(paddle_b_up_press, "Up")
win.onkeypress(paddle_b_down_press, "Down")
win.onkeyrelease(paddle_b_release, "Up")
win.onkeyrelease(paddle_b_release, "Down")

# Main game loop
while True:
    win.update()

    # Smoothly move paddles
    paddle_a.sety(paddle_a.ycor() + paddle_a_dy)
    paddle_b.sety(paddle_b.ycor() + paddle_b_dy)

    # Ensure paddles stay within bounds
    if paddle_a.ycor() > 250:
        paddle_a.sety(250)
    elif paddle_a.ycor() < -240:
        paddle_a.sety(-240)

    if paddle_b.ycor() > 250:
        paddle_b.sety(250)
    elif paddle_b.ycor() < -240:
        paddle_b.sety(-240)

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border collision
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        update_score()

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        update_score()

    # Paddle collision
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1

    if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1

