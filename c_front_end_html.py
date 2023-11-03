import b_backend
import streamlit as st
from streamlit_chat import message
import streamlit.components.v1 as components

html_code = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body,
    html {
      margin: 0px;
      padding: 0px;
      position: fixed;
      background: black;
    }

    .buymeacoffee {
      text-decoration: none;
      position: fixed;
      right: 2rem;
      bottom: 2rem;
      background: #FFDD00;
      width: 3.5rem;
      height: 3.5rem;
      border-radius: 50%;
      transition: all 0.1s linear;
      box-shadow: 0.2rem 0.2rem 0.5rem rgba(0, 0, 0, 0.2);
      z-index: 1000;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .buymeacoffee:hover {
      width: 4rem;
      height: 4rem;
      line-height: 4rem;
    }
  </style>
</head>

<body>
  <canvas id="canvas"></canvas>

  <a href="https://www.buymeacoffee.com/brusespinal" class="buymeacoffee" target="_blank" rel="noopener noreferrer">
    <svg width="25" height="35" viewBox="0 0 884 1279" fill="none">
      <path d="m791 298-1-1-2-1 3 2Zm13 91h-1 1Zm-13-92v1-1Zm0 1v-1 1Zm3 2-2-2h-1l3 2Zm-364 886-3 2h1l2-2Zm211-41v3-3Zm-22 41-3 2h1l2-2Zm-338 10-3-1 3 1Zm-33-32-1-4 1 4Z" fill="#0D0C22"></path>
      <path class="y-path" d="M473 591c-46 20-98 42-166 42-28 0-56-4-84-12l47 480a80 80 0 0 0 80 74l88 3 96-3a80 80 0 0 0 79-74l50-530c-22-8-44-13-70-13-44 0-79 15-120 33Z" fill="#FFF"></path>
      <path d="M79 386v1h1l-1-1Z" fill="#0D0C22"></path>
      <path d="m880 342-7-36c-7-31-21-62-54-73-10-4-22-5-30-13s-11-19-12-30l-11-61c-3-17-5-37-13-52-10-22-32-34-53-42-11-5-22-8-33-11C613 10 557 5 503 2c-66-4-132-2-198 3-48 5-100 10-146 27Z" fill="#0D0C22"></path>
    </svg>
  </a>

  <script>
    window.requestAnimFrame = function () {
  return (
    window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    function (callback) {
      window.setTimeout(callback);
    }
  );
};

function init(elemid) {
  let canvas = document.getElementById(elemid),
    c = canvas.getContext("2d"),
    w = (canvas.width = window.innerWidth),
    h = (canvas.height = window.innerHeight);
  c.fillStyle = "rgba(30,30,30,1)";
  c.fillRect(0, 0, w, h);
  return { c: c, canvas: canvas };
}

window.onload = function () {
  let c = init("canvas").c,
    canvas = init("canvas").canvas,
    w = (canvas.width = window.innerWidth),
    h = (canvas.height = window.innerHeight),
    mouse = { x: false, y: false },
    last_mouse = {};

  function dist(p1x, p1y, p2x, p2y) {
    return Math.sqrt(Math.pow(p2x - p1x, 2) + Math.pow(p2y - p1y, 2));
  }

  class segment {
    constructor(parent, l, a, first) {
      this.first = first;
      if (first) {
        this.pos = {
          x: parent.x,
          y: parent.y
        };
      } else {
        this.pos = {
          x: parent.nextPos.x,
          y: parent.nextPos.y
        };
      }
      this.l = l;
      this.ang = a;
      this.nextPos = {
        x: this.pos.x + this.l * Math.cos(this.ang),
        y: this.pos.y + this.l * Math.sin(this.ang)
      };
    }
    update(t) {
      this.ang = Math.atan2(t.y - this.pos.y, t.x - this.pos.x);
      this.pos.x = t.x + this.l * Math.cos(this.ang - Math.PI);
      this.pos.y = t.y + this.l * Math.sin(this.ang - Math.PI);
      this.nextPos.x = this.pos.x + this.l * Math.cos(this.ang);
      this.nextPos.y = this.pos.y + this.l * Math.sin(this.ang);
    }
    fallback(t) {
      this.pos.x = t.x;
      this.pos.y = t.y;
      this.nextPos.x = this.pos.x + this.l * Math.cos(this.ang);
      this.nextPos.y = this.pos.y + this.l * Math.sin(this.ang);
    }
    show() {
      c.lineTo(this.nextPos.x, this.nextPos.y);
    }
  }

  class tentacle {
    constructor(x, y, l, n, a) {
      this.x = x;
      this.y = y;
      this.l = l;
      this.n = n;
      this.t = {};
      this.rand = Math.random();
      this.segments = [new segment(this, this.l / this.n, 0, true)];
      for (let i = 1; i < this.n; i++) {
        this.segments.push(
          new segment(this.segments[i - 1], this.l / this.n, 0, false)
        );
      }
    }
    move(last_target, target) {
      this.angle = Math.atan2(target.y - this.y, target.x - this.x);
      this.dt = dist(last_target.x, last_target.y, target.x, target.y) + 5;
      this.t = {
        x: target.x - 0.8 * this.dt * Math.cos(this.angle),
        y: target.y - 0.8 * this.dt * Math.sin(this.angle)
      };
      if (this.t.x) {
        this.segments[this.n - 1].update(this.t);
      } else {
        this.segments[this.n - 1].update(target);
      }
      for (let i = this.n - 2; i >= 0; i--) {
        this.segments[i].update(this.segments[i + 1].pos);
      }
      if (
        dist(this.x, this.y, target.x, target.y) <=
        this.l + dist(last_target.x, last_target.y, target.x, target.y)
      ) {
        this.segments[0].fallback({ x: this.x, y: this.y });
        for (let i = 1; i < this.n; i++) {
          this.segments[i].fallback(this.segments[i - 1].nextPos);
        }
      }
    }
    show(target) {
      if (dist(this.x, this.y, target.x, target.y) <= this.l) {
        c.globalCompositeOperation = "lighter";
        c.beginPath();
        c.lineTo(this.x, this.y);
        for (let i = 0; i < this.n; i++) {
          this.segments[i].show();
        }
        c.strokeStyle =
          "hsl(" +
          (this.rand * 60 + 180) +
          ",100%," +
          (this.rand * 60 + 25) +
          "%)";
        c.lineWidth = this.rand * 2;
        c.lineCap = "round";
        c.lineJoin = "round";
        c.stroke();
        c.globalCompositeOperation = "source-over";
      }
    }
    show2(target) {
      c.beginPath();
      if (dist(this.x, this.y, target.x, target.y) <= this.l) {
        c.arc(this.x, this.y, 2 * this.rand + 1, 0, 2 * Math.PI);
        c.fillStyle = "white";
      } else {
        c.arc(this.x, this.y, this.rand * 2, 0, 2 * Math.PI);
        c.fillStyle = "darkcyan";
      }
      c.fill();
    }
  }

  let maxl = 300,
    minl = 50,
    n = 30,
    numt = 500,
    tent = [],
    clicked = false,
    target = { x: 0, y: 0 },
    last_target = {},
    t = 0,
    q = 10;

  for (let i = 0; i < numt; i++) {
    tent.push(
      new tentacle(
        Math.random() * w,
        Math.random() * h,
        Math.random() * (maxl - minl) + minl,
        n,
        Math.random() * 2 * Math.PI
      )
    );
  }
  function draw() {
    if (mouse.x) {
      target.errx = mouse.x - target.x;
      target.erry = mouse.y - target.y;
    } else {
      target.errx =
        w / 2 +
        ((h / 2 - q) * Math.sqrt(2) * Math.cos(t)) /
          (Math.pow(Math.sin(t), 2) + 1) -
        target.x;
      target.erry =
        h / 2 +
        ((h / 2 - q) * Math.sqrt(2) * Math.cos(t) * Math.sin(t)) /
          (Math.pow(Math.sin(t), 2) + 1) -
        target.y;
    }

    target.x += target.errx / 10;
    target.y += target.erry / 10;

    t += 0.01;

    c.beginPath();
    c.arc(
      target.x,
      target.y,
      dist(last_target.x, last_target.y, target.x, target.y) + 5,
      0,
      2 * Math.PI
    );
    c.fillStyle = "hsl(210,100%,80%)";
    c.fill();

    for (i = 0; i < numt; i++) {
      tent[i].move(last_target, target);
      tent[i].show2(target);
    }
    for (i = 0; i < numt; i++) {
      tent[i].show(target);
    }
    last_target.x = target.x;
    last_target.y = target.y;
  }

  canvas.addEventListener(
    "mousemove",
    function (e) {
      last_mouse.x = mouse.x;
      last_mouse.y = mouse.y;

      mouse.x = e.pageX - this.offsetLeft;
      mouse.y = e.pageY - this.offsetTop;
    },
    false
  );

  canvas.addEventListener("mouseleave", function (e) {
    mouse.x = false;
    mouse.y = false;
  });

  canvas.addEventListener(
    "mousedown",
    function (e) {
      clicked = true;
    },
    false
  );

  canvas.addEventListener(
    "mouseup",
    function (e) {
      clicked = false;
    },
    false
  );

  function loop() {
    window.requestAnimFrame(loop);
    c.clearRect(0, 0, w, h);
    draw();
  }

  window.addEventListener("resize", function () {
    (w = canvas.width = window.innerWidth),
      (h = canvas.height = window.innerHeight);
    loop();
  });

  loop();
  setInterval(loop, 1000 / 60);
};

  </script>
</body>

</html>

"""
st.set_page_config(page_title="Dashboard",page_icon=" ",layout="wide")

total1,total2 = st.columns([20,25])
with total2:
  st.title("CHATBOT")
  st.write("CONSULTA LA DISPONIBILIDAD DE MEDICAMENTOS AQUI!!!")

  if 'preguntas' not in st.session_state:
      st.session_state.preguntas = []
  if 'respuestas' not in st.session_state:
      st.session_state.respuestas = []

  def click():
      if st.session_state.user != '':
         pregunta = st.session_state.user
         respuesta = b_backend.consulta(pregunta)

         st.session_state.preguntas.append(pregunta)
         st.session_state.respuestas.append(respuesta)

         # Limpiar el input de usuario después de enviar la pregunta
         st.session_state.user = ''


  with st.form('my-form'):
    query = st.text_input('¿En qué te puedo ayudar?:', key='user', help='Pulsa Enviar para hacer la pregunta')
    submit_button = st.form_submit_button('Enviar', on_click=click)

  if st.session_state.preguntas:
      for i in range(len(st.session_state.respuestas)-1, -1, -1):
          message(st.session_state.respuestas[i], key=str(i))

    # Opción para continuar la conversación
      continuar_conversacion = st.checkbox('¿Quieres hacer otra pregunta?')
      if not continuar_conversacion:
         st.session_state.preguntas = []
         st.session_state.respuestas = []

# Agregar el código HTML a la aplicación Streamlit
with total1 :
  components.html(html_code, height=850, width=1750)

